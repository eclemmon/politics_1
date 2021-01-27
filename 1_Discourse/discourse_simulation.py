import sched
import json
import time
import itertools
from NLP_Tools.message_comparison_toolset import TF_IDF
from NLP_Tools.corpus_mean_and_std import CorpusMeanAndStd
from NLP_Tools.sentiment_analysis_tools import get_sentiment
from pythonosc import udp_client
from pythonosc import osc_message_builder
from Rhythm_Generators import euclidean_rhythm_generator as er_gen
from Harmonic_Graph_Constructors.neo_riemannian_web import NeoriemannianWeb
from Utility_Tools.logistic_function import linear_to_logistic as l2l
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class TweetsIncomingSim:
    def __init__(self, full_corpus, formal_section_length=30, harmonic_rhythm=20, message_comparison=TF_IDF(),
                 web=NeoriemannianWeb(), sentiment_analyzer=SentimentIntensityAnalyzer()):
        # Initialize NLP objects.
        self.time_and_tweets = self.time_and_tweet_gen(full_corpus)
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
        # Initialize OSC client.
        self.client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
        # Initialize scheduler
        self.scheduler = sched.scheduler(time.time, time.sleep)

    @property
    def next(self):
        return next(self.time_and_tweets)

    @staticmethod
    def time_and_tweet_gen(corpus):
        for key in corpus.keys():
            yield key, corpus[key]

    def run(self):
        time_passed = 0
        while True:
            try:
                key, value = self.next
                self.current_partial_corpus[key] = value
                time_passed += float(key)
                if time_passed >= self.formal_section_length:
                    if self.prior_partial_corpus is None:
                        diff = CorpusMeanAndStd(0.0, 0.0)
                        self.prior_partial_corpus = CorpusMeanAndStd(corpus=self.current_partial_corpus)
                        self.harmonic_walk_dummy(3, diff.mean, diff.std, harmonic_graph=self.web)
                        time_passed = 0
                    else:
                        current_corpus_mean_std = CorpusMeanAndStd(corpus=self.current_partial_corpus)
                        diff = self.prior_corpus_mean_std - current_corpus_mean_std
                        self.prior_partial_corpus = self.current_partial_corpus
                        self.current_partial_corpus = {}
                        self.prior_corpus_mean_std = current_corpus_mean_std
                        self.harmonic_walk_dummy(3, diff.mean, diff.std, harmonic_graph=self.web)
                        time_passed = 0
                else:
                    self.trigger_sounds(self.current_partial_corpus[key], time.time() + float(key))
            except StopIteration:
                break
            self.scheduler.run()

    def trigger_sounds(self, data, time_interval):
        # self.scheduler.enterabs(time_interval, 1, print, argument=('Triggered:', data))
        self.generate_rhythm(data)


    def harmonic_walk_dummy(self, multiplier, lev_mean, lev_standard_of_deviation, harmonic_graph):
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

    def generate_rhythm(self, data):
        sentiment = get_sentiment(self.sentiment_analyzer, data)
        print(sentiment)


# noinspection PyShadowingNames
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
    :param time_interval:
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
    print(msg.params)
    client.send(msg)




def random_walk_only_new(num_chords_walked, harmonic_web, client, octave=None, time_interval=None,
                         harmonic_rhythm=None):
    """
    Function that walks randomly through a harmonic web object, selects
    Chord objects that have not been visited yet and sends their pitch materials to SC.
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


if __name__ == '__main__':
    file_path = "/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/Corpora/TwiConv/time_and_tweets.json"

    with open(file_path, 'r') as file:
        tweets = json.load(file)
    # starting_chord = Chord(Note(60), Note(64), Note(67))
    # web = NeoriemannianWeb(starting_chord)
    # web = circle_of_fifths_web.CircleOfFifths(starting_chord)
    # web.build_web()
    # random_walk_only_new(3, web, client, time_interval=1)
    sim = TweetsIncomingSim(tweets, formal_section_length=10, harmonic_rhythm=10)
    sim.run()
