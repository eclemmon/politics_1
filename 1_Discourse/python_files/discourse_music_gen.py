import time
import itertools
from NLP_Tools.message_comparison_toolset import TF_IDF
from NLP_Tools.corpus_mean_and_std import CorpusMeanAndStd
from pythonosc import udp_client
from pythonosc import osc_message_builder
from Rhythm_Generators import euclidean_rhythm_generator as er_gen
from Harmonic_Graph_Constructors.neo_riemannian_web import NeoriemannianWeb
from Utility_Tools.logistic_function import linear_to_logistic as l2l
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class DiscourseMusicGen:
    def __init__(self, logger_object, formal_section_length=30, harmonic_rhythm=20, message_comparison=TF_IDF(),
                 web=NeoriemannianWeb(), sentiment_analyzer=SentimentIntensityAnalyzer()):
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

        # Initialize music generators and timing protocols.
        self.web = web
        self.web.build_web()
        self.formal_section_length = formal_section_length
        self.harmonic_rhythm = harmonic_rhythm
        self.osc_func_addresses = ['/pitch_triggers1', '/pitch_triggers2', '/pitch_triggers3', '/pitch_triggers4']
        self.osc_func_index = 0

        # Initialize OSC client.
        self.client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

        # Initialize time_passed
        self.starting_time = time.time()

    def trigger_sounds(self, data):
        """
        Triggers sounds and calls a cascading stack of functions and methods to generate music.
        :param data: Currently the messsage contents of a tweet.
        """
        current_time = time.time()
        time_passed = current_time - self.starting_time
        self.current_partial_corpus[current_time] = data
        if time_passed >= self.formal_section_length:
            self.if_first_chord_walk()
            self.send_rhythm_materials(data=data)
        else:
            self.send_rhythm_materials(data=data)

    def harmonic_walk(self, multiplier, lev_mean, lev_standard_of_deviation, harmonic_graph):
        """
        This will determine the distance that the chord should walk based on the mean and
        standard of deviation of 3
        :param multiplier:
        :param lev_mean:
        :param lev_standard_of_deviation:
        :param harmonic_graph:
        :return:
        """
        num_chords_walked = int(l2l(abs(lev_mean), 0, 100, 0, 10, lev_standard_of_deviation))
        print("num_chords_walked: ", num_chords_walked)
        if num_chords_walked == 0:
            interval = self.harmonic_rhythm
        else:
            interval = self.harmonic_rhythm / num_chords_walked
        print("interval: ", interval)
        random_walk_only_new(num_chords_walked, harmonic_graph, self.client, time_interval=interval,
                             harmonic_rhythm=self.harmonic_rhythm)

    def compare_tweets(self, tweet):
        """

        :param tweet:
        :return: Tuple with closest related text and the similarity score.
        """
        return self.message_comparison_obj.new_incoming_tweet(tweet)

    def generate_euclidean_rhythm(self, data):
        """
        Generates an array of euclidean rhythms as a list of binary 1's and 0's. 1's represent
        the onsets of a musical event. The 0's are then replaced with -1.5 for
        :param data:
        :return:
        """
        data = er_gen.generate_euclidean(4, 6)
        for index, item in enumerate(data):
            if item == 0:
                data[index] = -1.5
        return data

    def send_rhythm_materials(self, data, time_interval=5):
        rhythm = self.generate_euclidean_rhythm(data)
        msg = osc_message_builder.OscMessageBuilder(address=self.osc_func_addresses[self.osc_func_index])
        for item in rhythm:
            msg.add_arg(item, arg_type='f')
        msg.add_arg(time_interval, arg_type='f')
        msg = msg.build()
        self.update_osc_func_index()
        self.client.send(msg)

    def update_osc_func_index(self):
        self.osc_func_index = (self.osc_func_index + 1) % 4

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
            self.harmonic_walk(3, diff.mean, diff.std, harmonic_graph=self.web)
        except ValueError:
            self.logger_object.info("Seems like you haven't gotten enough tweets in the previous formal section?")
            diff = CorpusMeanAndStd(0.0, 0.0)
            self.prior_partial_corpus = CorpusMeanAndStd(corpus=self.current_partial_corpus)
            self.harmonic_walk(3, diff.mean, diff.std, harmonic_graph=self.web)

        self.starting_time = time.time()

    def if_first_chord_walk(self):
        if self.prior_partial_corpus is None:
            self.send_first_chord_walk()
        else:
            self.send_chord_walk()


def generate_pitch_materials(web: NeoriemannianWeb, octave, current_chord):
    """
    This helper functionfunction simply returns an array of midi note numbers according to
    the input chord.
    :param web: neo-Riemannian web object.
    :param octave: Which octave the desired midi note numbers should be transposed to.
    :param current_chord: a major or minor triad as a Chord object.
    :return: Returns an array of midi note numbers.
    """
    chords = [current_chord]
    for chord in web.web[current_chord]:
        chords.append(chord)
    return [[note.midi_note_number + 12 * octave for note in chord.notes] for chord in chords]


def send_chord_materials(notes, client, time_interval, harmonic_rhythm):
    """
    Builds pitch materials into an OSC message, send to SuperCollider.
    :param harmonic_rhythm: The length of the formal structure in time over which the harmonies change.
    :param time_interval: The time interval by which chords advance
    :param notes: Notes array of arrays generated by generate_pitch_materials helper function.
    :param client: OSC client
    :return:
    """
    msg = osc_message_builder.OscMessageBuilder(address='/harmonic_materials')
    pitches = list(itertools.chain(*[note for chord in notes for note in chord]))
    msg.add_arg(harmonic_rhythm, arg_type='f')
    msg.add_arg(time_interval, arg_type='f')
    for pitch in pitches:
        msg.add_arg(pitch, arg_type='i')
    msg = msg.build()
    # print(msg.params)
    client.send(msg)


def random_walk_only_new(num_chords_walked, harmonic_web, client, octave=None, time_interval=None,
                         harmonic_rhythm=None):
    """
    Function that walks randomly through a harmonic web object, selects
    Chord objects that have not been visited yet and sends their pitch materials to SC.
    :param client:
    :param harmonic_rhythm:
    :param num_chords_walked: Number of chords to be passed to SC.
    :param harmonic_web: Harmonic Web object.
    :param octave: The octave to transpose midi note values to.
    :param time_interval: The frequency that send_pitch_materials is called.
    """
    if octave is None:
        octave = 5

    if time_interval is None:
        time_interval = 5

    if harmonic_rhythm is None:
        harmonic_rhythm = 5

    chords = harmonic_web.random_walk_only_new(num_chords_walked)
    schedule_chords(chords, time_interval, harmonic_rhythm, harmonic_web, octave, client)


def schedule_chords(chords, time_interval, harmonic_rhythm, chord_graph, octave, client):
    pitch_materials = []
    for chord in chords:
        pitch_materials.append(generate_pitch_materials(chord_graph, octave, chord))
    send_chord_materials(pitch_materials, client, time_interval, harmonic_rhythm)
