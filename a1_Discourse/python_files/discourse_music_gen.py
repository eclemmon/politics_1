import logging
import time
import json
import tweepy

from dotenv import dotenv_values
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from better_profanity import profanity
from Classes.worker_thread import WorkerThread
from Harmonic_Graph_Constructors.harmonic_web import HarmonicWeb
from Utility_Tools.mapping_functions import linear_to_linear
from Utility_Tools.message_response import PoliticsMessageResponder
from Utility_Tools.message_response import generate_discourse_message_response

from NLP_Tools.message_comparison_toolset import TF_IDF
from NLP_Tools.corpus_mean_and_std import CorpusMeanAndStd
from NLP_Tools.sentiment_dictionary import SentimentDict
from NLP_Tools import part_of_speech_tools
from NLP_Tools.sentiment_analysis_tools import get_average_sentiment
from NLP_Tools import emoji_counter

from pythonosc import udp_client
from pythonosc import osc_message_builder

from Rhythm_Generators import euclidean_rhythm_generator as er_gen

from Harmonic_Graph_Constructors.neo_riemannian_web import NeoriemannianWeb
from Harmony_Generators.harmonic_walk_functions import num_chords_walked
from Harmony_Generators import octave_displacement_generator
from Harmony_Generators.neighbor_chord_generator import generate_neighbor_chord_weights
from Harmony_Generators.neighbor_chord_generator import build_weight_and_chord_array

from Synthesis_Generators.instrument_key_generator import InstrumentKeyAndNameGenerator
from Synthesis_Generators.spatialization_values_generator import generate_spatialization_values
from Synthesis_Generators.delay_values_generator import delay_time_and_decay
from Synthesis_Generators.phase_mod_values_generator import phase_mod_values_generator


class DiscourseMusicGen:
    def __init__(self, logger_object: logging.Logger, instrument_key_and_name_gen: InstrumentKeyAndNameGenerator,
                 formal_section_length: int = 30, harmonic_rhythm: int = 30, message_comparison=TF_IDF(),
                 web: HarmonicWeb = NeoriemannianWeb(), sentiment_analyzer=SentimentIntensityAnalyzer(),
                 ncw_multiplier: float = 1, profanity_word_list_path: str = None, max_time_interval: float = 20,
                 daw: bool = True):
        """
        Initializes DiscourseMusicGen
        :param max_time_interval: float of maximum duration that each resultant musical gesture lasts
        :param daw: Boolean for daw or SC based sound synthesis.
        :param logger_object: Logger, built from Utility_Tools.politics_logger.py
        :param instrument_key_and_name_gen: InstrumentKeyAndNameGenerator object that uses stored memory values
        to generate instrument keys and names agnostically.
        :param formal_section_length: Integer in seconds
        :param harmonic_rhythm: Integer in seconds
        :param message_comparison: Message comparison object. Defaults to term-frequency inverse-document-frequency,
        but will accept any model to compare two texts.
        :param web: HarmonicWeb object. Defaults to Neo-riemannian web. A graph of chords that represent motion
        between Chords.
        :param sentiment_analyzer: SentimentIntensityAnalyzer object. Defaults to my own SentimentIntensityAnalyzer
        but can be any sentiment intensity model that returns {'neg': val, 'neu': val, 'pos': val, 'compound': val}
        :param ncw_multiplier: Integer or float. Multiplier of the number of chords walked to accelerate or decelerate
        the harmonic rhythm.
        :param profanity_word_list_path: String. Path to a profanity word list to alter the list of censored words
        output to the GUI.
        """
        self.logger_object = logger_object

        # Initialize NLP objects.
        self.current_partial_corpus = {}
        self.prior_partial_corpus = None
        self.prior_corpus_mean_std = CorpusMeanAndStd(0.0, 0.0)
        self.message_comparison_obj = message_comparison
        self.sentiment_analyzer = sentiment_analyzer
        self.average_sent = SentimentDict()
        self.profanity = profanity

        # Initialize profanity word list based on object run time.
        if profanity_word_list_path is None:
            self.profanity.load_censor_words()
        else:
            self.profanity.load_censor_words_from_file(profanity_word_list_path)

        # Initialize music generators and timing protocols.
        self.web = web
        self.web.build_web()
        self.worker_thread = None
        self.formal_section_length = formal_section_length
        self.harmonic_rhythm = harmonic_rhythm
        self.synth_osc_address = '/sound_triggers'
        self.gui_osc_address = '/gui_address'
        self.num_chords_walked_multiplier = ncw_multiplier
        self.inst_key_name_gen = instrument_key_and_name_gen
        self.max_time_interval = max_time_interval
        self.daw = daw

        # Initialize OSC clients.
        self.sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
        self.gui_client = udp_client.SimpleUDPClient("127.0.0.1", 12000)

        # Make Message Responder
        config = dotenv_values()

        twitter_path = '/Users/ericlemmon/Documents/PhD/PhD_Project_v2/twitter_credentials.json'
        with open(twitter_path, "r") as file:
            credentials = json.load(file)

        self.twitter_auth = tweepy.OAuth1UserHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'],
                                                     credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
        self.responder = PoliticsMessageResponder(config['TWILIO_ACCOUNT_SID'], config['TWILIO_AUTH_TOKEN'],
                                                  config['TWILIO_PHONE_NUMBER'], self.twitter_auth)

        # Initialize time_passed
        self.starting_time = time.time()

    def trigger_sounds(self, data):
        """
        Triggers sounds and calls a cascading stack of functions and methods to generate music.
        :param data: Dict of data, i.e. {'text': "lorum ipsum", 'username': "Confucius"}
        """
        # Get current time and time elapsed and add text to current partial corpus.
        current_time = time.time()
        time_passed = current_time - self.starting_time
        # Add text to corpus for this formal section
        self.current_partial_corpus[current_time] = data['text']

        # Send Data
        if time_passed >= self.formal_section_length:
            # If formal section length elapsed, chord walk
            self.if_first_chord_walk()
            # Send Music Data
            self.send_music_data(data=data)
            # Send GUI Data
            self.send_gui_data(data=data)
        else:
            self.send_music_data(data=data)
            self.send_gui_data(data=data)

    def send_music_data(self, data):
        """
        This is the big NLP processing and OSC logic function.
        :param data: Dict of data, i.e. {'text': "lorum ipsum", 'username': "Confucius"}
        :return: True
        """
        # Send Data to Super Collider.
        # Build OSC Message Object Constructor
        msg = osc_message_builder.OscMessageBuilder(address=self.synth_osc_address)
        # Builds the time interval data
        time_interval = self.get_time_interval_data(data['text'])
        # Builds a dictionary of counts of parts of speech
        pos_count_dict = part_of_speech_tools.build_pos_count_dict(data['text'])
        # Get sentiment value of text
        sent = get_average_sentiment(self.sentiment_analyzer, data['text'])
        # Get avg sentiment value of emojis
        emojis = emoji_counter.get_emojis(data['text'])
        avg_emoji_sent = emoji_counter.get_average_emoji_sent_from_msg(emojis)
        # Build Sentiment Dictionary
        sent_dict = SentimentDict(sent)

        # Data that determines delay time and decay (Feedback Delay Time, Delay Decay) {No of Nouns, No. Verbs}
        delay_t_a_d = delay_time_and_decay(pos_count_dict)
        # Add delay data to osc message: 2 vals
        for item in delay_t_a_d:
            msg.add_arg(item, arg_type='i')

        # Data that determines reverb values (predelay, reverbtime, lpf, mix) {neg, neu, pos, compound}
        reverb_vals = self.average_sent.abs_difference(sent_dict)
        # Add reverb data to osc message: 4 vals
        for item in list(reverb_vals.sent_dict.values()):
            msg.add_arg(item, arg_type='f')

        # Data that determines spatialization
        # (Time Interval, Start Point, Target) {Msg Len, Compound Sentiment, Inverse Compound Sentiment val}
        spat = generate_spatialization_values(time_interval, sent)
        # Add spatialization data to osc message: 3 vals
        for item in spat:
            msg.add_arg(float(item), arg_type='f')

        # Data that determines amount of Phase Modulation (Freq, Amp) {Number of emojis, Sentiment of Emojis}
        pmod = phase_mod_values_generator(avg_emoji_sent, emojis)
        # Add phase mod data to osc message: 2 vals
        for item in pmod:
            msg.add_arg(float(item), arg_type='f')

        # Data on octave displacement. (Octave) {Length of message on sigmoid curve. Shorter, higher, longer, lower}
        # od = octave_displacement_generator.get_octave_placement_sigmoid(data['text'])
        od = octave_displacement_generator.get_octave_placement_piecewise(data['text'])
        # Add octave displacement to osc message: 1 val
        msg.add_arg(od, arg_type='i')

        # Add time interval data to osc message
        msg.add_arg(time_interval, arg_type='f')

        # Chain of Instruments to synthesize with (List of instrument names) {Hash of sentiment values}
        # Lower octaves == less instruments
        num_insts = int(linear_to_linear(od, 2, 8, 1, self.inst_key_name_gen.max_instruments + 1))
        inst_keys = self.inst_key_name_gen.get_instrument_chain_keys(sent, avg_emoji_sent.sent_dict)
        inst_names = self.inst_key_name_gen.get_n_instrument_chain_names(inst_keys, num_insts)
        # Add instrument names to osc message: var num of vals
        msg.add_arg(len(inst_names), arg_type='i')
        for inst in inst_names:
            if self.daw:
                msg.add_arg(inst, arg_type='i')
            else:
                msg.add_arg(inst, arg_type='s')

        # Neighbor Chord Borrowing Vector distance mapping (Sentiment Values) {Weight of neighbor chords}
        w_c_array = self.get_chord_and_weights(sent)
        # Add neighbor chords to OSC Message: 3 sets of var vals
        for item in w_c_array:
            msg.add_arg(item, arg_type='f')

        # Data that determines rhythmic materials (impulses, offsets) {No. Tokens, No. discrete POS}
        rhythm = self.generate_euclidean_rhythm(pos_count_dict)
        # Add Rhythm Data to osc message: var num of vals
        for item in rhythm:
            msg.add_arg(item, arg_type='f')

        # Send Message Response
        kwargs = {'od': od, 'time_interval': time_interval, 'rhythm': rhythm, 'delay_t_a_d': delay_t_a_d, 'spat': spat,
                  'pmod': pmod}
        generate_discourse_message_response(self.responder, data, kwargs)

        # Build the osc message
        msg = msg.build()
        # Log the message
        self.logger_object.info(data)
        self.logger_object.info(msg.params)
        # Send the message to SuperCollider
        self.sc_client.send(msg)

        # CLEAN UP AND UPDATE ANY VALUES
        # Update average sentiment value
        self.average_sent.add_value_average(sent_dict)

        return True

    def send_gui_data(self, data):
        """
        Sends osc message over to GUI.
        :param data: Dict of data, i.e. {'text': "lorum ipsum", 'username': "Confucius"}
        :return: Boolean True
        """
        # Send Data to GUI
        # Build OSC Message Object Constructor
        msg = osc_message_builder.OscMessageBuilder(address=self.gui_osc_address)
        # Construct text to display and censor any text for profanity.
        if data.get('sms'):
            display = "XXX-XXX-" + data['username'][-4:] + " said: " + self.profanity.censor(data['text'])
        elif data.get('tweet'):
            display = data['username'] + " said: " + self.profanity.censor(data['text'])
        else:
            display = data['username'] + " said: " + self.profanity.censor(data['text'])
        print(display)
        print(data)
        # Add data to the message
        msg.add_arg(display, arg_type='s')
        # Build the message
        msg = msg.build()
        # Send the message to SuperCollider
        self.gui_client.send(msg)

        return True

    def harmonic_walk(self, multiplier, lev_mean, lev_standard_of_deviation, harmonic_graph):
        """
        This will determine the distance that the chord should walk based on the mean and
        standard of deviation of Leventshtein distance between all the texts submitted to the corpus.
        In the future, will be deprecated in favor of an LSA space model based on a large enough corpus of submitted
        texts to the system.
        :param multiplier: A multiplier to increase of decrease the number of chords walked.
        :param lev_mean: The mean value of Leventshtein distance among all the texts in the corpus.
        :param lev_standard_of_deviation: The standard of deviation from the mean of the Levenshtein distance among
        all the texts in the corpus.
        :param harmonic_graph: A HarmonicGraph object.
        :return: None
        """
        num_walked = num_chords_walked(lev_mean, lev_standard_of_deviation) * multiplier
        # print("num_chords_walked: ", num_walked)
        if num_walked == 0:
            interval = self.harmonic_rhythm
        else:
            interval = self.harmonic_rhythm / num_walked
        # print("interval: ", interval)
        self.schedule_random_walk_only_new(num_walked, harmonic_graph, interval,
                                           self.harmonic_rhythm)

    def compare_text(self, data):
        """
        Using the message comparison object steps through all input tweets and gets the closest tweet by comparison
        via the message comparison object's algorithm. Currently, unused in favor of a deterministic algorithm based on
        textual features rather than relationships.
        :param data: Dict of data, i.e. {'text': "lorum ipsum", 'username': "Confucius"}
        :return: Tuple with the closest related text and the similarity score.
        """
        return self.message_comparison_obj.new_incoming_tweet(data['text'])

    @staticmethod
    def generate_euclidean_rhythm(pos_count_dict):
        """
        Generates an array of euclidean rhythms as a list of binary 1's and 0's. 1's represent
        the onsets of a musical event. The 0's are then replaced with -1.5 for
        :param pos_count_dict: Dictionary of parts of speech count
        :return: List of 1s and -1.5s e.g. [1, -1.5, -1.5, 1, -1.5]. Done this way for the way trigger works in SC.
        """
        # Counts the number of discrete POS in the text.
        discrete_pos = part_of_speech_tools.count_discrete_pos(pos_count_dict)
        # Total number of POS in the text len(dict)
        total_pos = part_of_speech_tools.count_total_pos(pos_count_dict)
        # Generates the Euclidean Rhythms based on the ratio
        data = er_gen.generate_euclidean(discrete_pos, total_pos)
        # Preps data for SuperCollider
        for index, item in enumerate(data):
            if item == 0:
                data[index] = -1.5
        return data

    def send_first_chord_walk(self):
        """
        Sends the first chord walk of the piece. Sets the "original" Corpus Mean and Standard of deviation to 0.
        Compares the new corpus to this "original" corpus. Calls self.harmonic_walk function with this data
        and resets the starting time of the section.
        :return: None
        """
        diff = CorpusMeanAndStd(0.0, 0.0)
        self.prior_partial_corpus = CorpusMeanAndStd(corpus=self.current_partial_corpus)
        self.harmonic_walk(self.num_chords_walked_multiplier, diff.mean, diff.std, harmonic_graph=self.web)
        self.starting_time = time.time()

    def send_chord_walk(self):
        """
        Compares the mean and standard of deviation of the prior section's corpus segment to the current sections
        corpus segment. These "partial" corpuses are all the texts that came in during the previous and current
        formal_section_length in seconds. Calls self.harmonic_walk function with this data
        and resets the starting time of the section and the prior and current partial corpus variables.
        If the prior section got 0 incoming texts, the software can throw an error, so in this case, logs the error
        safely and sets the calculated difference to an initial corpus value.
        :return: None
        """
        current_corpus_mean_std = CorpusMeanAndStd(corpus=self.current_partial_corpus)
        diff = self.prior_corpus_mean_std - current_corpus_mean_std
        self.prior_partial_corpus = self.current_partial_corpus
        self.current_partial_corpus = {}
        self.prior_corpus_mean_std = current_corpus_mean_std

        try:
            self.harmonic_walk(self.num_chords_walked_multiplier, diff.mean, diff.std, harmonic_graph=self.web)
        except ValueError:
            self.logger_object.info("Seems like you haven't gotten enough texts in the previous formal "
                                    "section?")
            diff = CorpusMeanAndStd(0.0, 0.0)
            self.prior_partial_corpus = CorpusMeanAndStd(corpus=self.current_partial_corpus)
            self.harmonic_walk(self.num_chords_walked_multiplier, diff.mean, diff.std, harmonic_graph=self.web)

        self.starting_time = time.time()

    def if_first_chord_walk(self):
        """
        Helper function to determine whether the program is running the first formal section of the piece.
        :return: None
        """
        if self.prior_partial_corpus is None:
            self.send_first_chord_walk()
        else:
            self.send_chord_walk()

    def schedule_random_walk_only_new(self, num_chords_walked: int, harmonic_web: HarmonicWeb,
                                      time_interval: float = None):
        """
        Spins off a thread that schedules a random walk through the harmonic web
        :param num_chords_walked: Integer of number of chords walked
        :param harmonic_web: HarmonicWeb subclass representing a graph of potential chords and their iterative
        progressions.
        :param time_interval: Float or Integer of the amount of time in between chord changes
        :return: None
        """
        if time_interval is None:
            time_interval = 5

        chords = harmonic_web.random_walk_only_new(num_chords_walked)
        if self.worker_thread is None:
            self.worker_thread = WorkerThread(target=self.set_output_chord, args=[time_interval, chords])
            self.worker_thread.start()
        else:
            self.worker_thread.stop()
            self.worker_thread.join()
            self.worker_thread = WorkerThread(target=self.set_output_chord, args=[time_interval, chords])
            self.worker_thread.start()

    def set_output_chord(self, time_interval: float, chords: list):
        """
        Operator function that modifies the HarmonicWeb object and sets the output chord on the object for getting
        at a later point.
        :param time_interval: float || int
        :param chords: List of Chords
        :return: None
        """
        for chord in chords:
            if self.worker_thread.stopped():
                break

            self.web.output_chord = chord
            time.sleep(time_interval)

    # TODO: Make this a sliding scale
    def get_time_interval_data(self, data):
        """
        Generates the total duration of a musical gesture based on the length of input text. In the future will be
        modified or refactored at the naming level so that the clumped nature of texts and their average shifts the
        range (the duration) of the function.
        :param data: String
        :return: float || int
        """
        text_length = len(data)
        if text_length > 280:
            return self.max_time_interval
        else:
            return text_length / 280 * self.max_time_interval

    def get_chord_and_weights(self, sent):
        """
        Gets the chord and all neighboring chords. Based on sentiment analysis data this function generates weights to
        select the proportions of notes to select from 'home' chord and neighboring chords. Structured as such
        for easy bundling and sending to SuperCollider.
        :param sent: Dict of sentiment data
        :return: List of data structured [float of weight, int of num_notes in chord, notes, ...]
        """
        neighbor_chords = self.web.get_neighbor_chords()
        current_chord_notes = [note.midi_note_number for note in self.web.output_chord.notes]
        neighbor_notes = [[note.midi_note_number for note in neighbor_chord.notes]
                          for neighbor_chord in neighbor_chords]
        weights = generate_neighbor_chord_weights(sent, len(neighbor_chords))
        return build_weight_and_chord_array(current_chord_notes, neighbor_notes, weights)
