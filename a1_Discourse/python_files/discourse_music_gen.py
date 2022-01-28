import time

from Harmony_Generators.harmonic_walk_functions import random_walk_only_new
from NLP_Tools.message_comparison_toolset import TF_IDF
from NLP_Tools.corpus_mean_and_std import CorpusMeanAndStd
from pythonosc import udp_client
from pythonosc import osc_message_builder
from Rhythm_Generators import euclidean_rhythm_generator as er_gen
from Harmonic_Graph_Constructors.neo_riemannian_web import NeoriemannianWeb
from Harmony_Generators.harmonic_walk_functions import num_chords_walked
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from better_profanity import profanity
from Synthesis_Generators.instrument_key_generator import InstrumentKeyAndNameGenerator
from NLP_Tools.average_sentiment import AverageSentiment
from NLP_Tools import part_of_speech_tools


class DiscourseMusicGen:
    def __init__(self, logger_object, instrument_key_and_name_gen: InstrumentKeyAndNameGenerator,
                 formal_section_length=30, harmonic_rhythm=20, message_comparison=TF_IDF(),
                 web=NeoriemannianWeb(), sentiment_analyzer=SentimentIntensityAnalyzer(), ncw_multiplier=1,
                 profanity_word_list_path=None):
        """
        :param logger_object: Logger from /Utility_Tools/politics_logger.py.
        :param formal_section_length: The length each formal section lasts
        :param harmonic_rhythm: The aggregate timeframe that all chords walk through. So if there are
        :param message_comparison: Defaults to a TF_IDF message comparison object
        :param web: Defaults to a NeoriemannianWeb
        :param sentiment_analyzer: Defaults to NLTK's VADER Sentiment Analyzer
        """
        self.logger_object = logger_object

        # Initialize NLP objects.
        self.current_partial_corpus = {}
        self.prior_partial_corpus = None
        self.prior_corpus_mean_std = CorpusMeanAndStd(0.0, 0.0)
        self.message_comparison_obj = message_comparison
        self.sentiment_analyzer = sentiment_analyzer
        self.average_sent = AverageSentiment()
        self.profanity = profanity

        # Initialize profanity word list based on object run time.
        if profanity_word_list_path is None:
            self.profanity.load_censor_words()
        else:
            self.profanity.load_censor_words_from_file(profanity_word_list_path)

        # Initialize music generators and timing protocols.
        self.web = web
        self.web.build_web()
        self.formal_section_length = formal_section_length
        self.harmonic_rhythm = harmonic_rhythm
        self.osc_func_address = '/pitch_triggers'
        self.num_chords_walked_multiplier = ncw_multiplier
        self.inst_key_name_gen = instrument_key_and_name_gen

        # Initialize OSC clients.
        self.sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
        self.gui_client = udp_client.SimpleUDPClient("127.0.0.1", 12000)

        # Initialize time_passed
        self.starting_time = time.time()

    def trigger_sounds(self, data):
        """
        Triggers sounds and calls a cascading stack of functions and methods to generate music.
        :param data: Currently the message contents of a tweet.
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
            self.send_music_data(data=data['text'])
            # Send GUI Data
            self.send_gui_data(data=data['text'])
        else:
            self.send_music_data(data=data['text'])
            self.send_gui_data(data=data['text'])

    def send_music_data(self, data, time_interval=5):
        # TODO: Add ALL materials
        # TODO: Octave placement Data that determines octave — {Length of message on sigmoid curve. Shorter, higher, longer, lower}
        # TODO: Base Sound Data that determines base sound {sound1: sin, sound2: saw, sound3: noise, sound4: impulse, sound5: square, etc}
        # TODO: Phase Modulation Data that determines Phase Mod [Freq, Amp] {Number of emojis = Freq} {Sentiment of Emojis = Amp}
        # TODO: Rhythmic Materials Data that determines rhythmic materials (impulses and offsets) {No. Tokens : No. discrete POS}
        # TODO: Neighbor Chord Borrowing — Vector distance stuff
        # TODO: Sentiment Value Reverb Data that determines reverb - Distance of text from sentiment value.
        # TODO: Amount of Delay data that determines amount of delay [Feedback Delay Time, Delay Decay] {No of Nouns, No. Verbs}
        rhythm = self.generate_euclidean_rhythm(data)
        msg = osc_message_builder.OscMessageBuilder(address=self.osc_func_address)
        for item in rhythm:
            msg.add_arg(item, arg_type='f')
        msg.add_arg(time_interval, arg_type='f')
        msg = msg.build()
        self.sc_client.send(msg)

    def send_gui_data(self, data):
        # Send Data to GUI
        msg = osc_message_builder.OscMessageBuilder(address=self.osc_func_address)
        display = data['username'] + " said: " + self.profanity.censor(data['text'])
        msg.add_arg(display, arg_type='s')
        msg = msg.build()
        self.gui_client.send(msg)

    def harmonic_walk(self, multiplier, lev_mean, lev_standard_of_deviation, harmonic_graph):
        """
        This will determine the distance that the chord should walk based on the mean and
        standard of deviation
        :param multiplier:
        :param lev_mean:
        :param lev_standard_of_deviation:
        :param harmonic_graph:
        :return:
        """
        num_walked = num_chords_walked(lev_mean, lev_standard_of_deviation) * multiplier
        print("num_chords_walked: ", num_walked)
        if num_walked == 0:
            interval = self.harmonic_rhythm
        else:
            interval = self.harmonic_rhythm / num_walked
        print("interval: ", interval)
        random_walk_only_new(num_walked, harmonic_graph, self.sc_client, time_interval=interval,
                             harmonic_rhythm=self.harmonic_rhythm)

    def compare_tweets(self, data):
        """

        :param tweet:
        :return: Tuple with closest related text and the similarity score.
        """
        return self.message_comparison_obj.new_incoming_tweet(data['text'])

    @staticmethod
    def generate_euclidean_rhythm(data):
        """
        Generates an array of euclidean rhythms as a list of binary 1's and 0's. 1's represent
        the onsets of a musical event. The 0's are then replaced with -1.5 for
        :param data: Dictionary String: String of tweet or text data
        :return: List of 1s and -1.5s e.g. [1, -1.5, -1.5, 1, -1.5]. Done this way for the way trigger works in SC.
        """
        # Builds a dictionary of counts of parts of speech
        pos_count_dict = part_of_speech_tools.build_pos_count_dict(data['text'])
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
        diff = CorpusMeanAndStd(0.0, 0.0)
        self.prior_partial_corpus = CorpusMeanAndStd(corpus=self.current_partial_corpus)
        self.harmonic_walk(3, diff.mean, diff.std, harmonic_graph=self.web)
        self.starting_time = time.time()

    def send_chord_walk(self):
        current_corpus_mean_std = CorpusMeanAndStd(corpus=self.current_partial_corpus)
        diff = self.prior_corpus_mean_std - current_corpus_mean_std
        self.prior_partial_corpus = self.current_partial_corpus
        self.current_partial_corpus = {}
        self.prior_corpus_mean_std = current_corpus_mean_std

        try:
            self.harmonic_walk(self.num_chords_walked_multiplier, diff.mean, diff.std, harmonic_graph=self.web)
        except ValueError:
            self.logger_object.info("Seems like you haven't gotten enough tweets in the previous formal section?")
            diff = CorpusMeanAndStd(0.0, 0.0)
            self.prior_partial_corpus = CorpusMeanAndStd(corpus=self.current_partial_corpus)
            self.harmonic_walk(self.num_chords_walked_multiplier, diff.mean, diff.std, harmonic_graph=self.web)

        self.starting_time = time.time()

    def if_first_chord_walk(self):
        if self.prior_partial_corpus is None:
            self.send_first_chord_walk()
        else:
            self.send_chord_walk()

