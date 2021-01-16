import json
import numpy
import pandas
import time
from fuzzywuzzy import fuzz

class CorpusMeanAndStd:
    def __init__(self, mean=None, std=None, corpus=None):
        if mean == None or std == None:
            try:
                mean_and_std = mean_and_std_of_corpus(corpus)
                self.mean = mean_and_std[0]
                self.std = mean_and_std[1]
            except RuntimeError:
                print("Something went wrong, you need to include either both a mean and a std value, or a corpus only")
        else:
            assert isinstance(mean, float) and isinstance(std, float)
            self.mean = mean
            self.std = std

    def __sub__(self, other):
        new_mean = self.mean - other.mean
        new_std = self.std - other.std
        return CorpusMeanAndStd(new_mean, new_std)

    def __add__(self, other):
        new_mean = self.mean + other.mean
        new_std = self.std + other.std
        return CorpusMeanAndStd(new_mean, new_std)

    def __repr__(self):
        return "{}, {}".format(self.mean, self.std)


def build_corpus(timing, test_corpus):
    time = 0
    corpus = {}
    for key in test_corpus.keys():
        time += float(key)
        if time > timing:
            break
        else:
            corpus[key] = tweets[key]
    return corpus

def mean_and_std_of_corpus(corpus):
    """
    Builds mean and std after deterimining levenshtein distance between two texts in a corpus.
    Better way? Also dumb O(n^2) double nested loop.
    :param corpus:
    :return:
    """
    corpus_length = len(corpus)

    similarity = numpy.empty((corpus_length, corpus_length), dtype=float)

    for i, ac in enumerate(corpus.values()):
        for j, bc in enumerate(corpus.values()):
            if i > j:
                continue
            if i == j:
                sim = 100
            else:
                sim = fuzz.ratio(ac, bc)

            similarity[i, j] = sim
            similarity[j, i] = sim

    data_frame_similarity = pandas.DataFrame(similarity, index=corpus, columns=corpus)
    l_tri = numpy.tril(data_frame_similarity.values, -1)
    l_tri = l_tri[numpy.nonzero(l_tri)]
    return l_tri.mean(), l_tri.std()


def trigger_sound(data):
    print("TRIGGERED SOUND")

def neoriemannian_walk_dummy(mean, std):
    print("CALLED THE WALK DUMMY")

class TweetsIncomingSim:
    def __init__(self, time_tweet_corpus, prior_corpus=None, harmonic_rhythm=30):
        if prior_corpus != None:
            self.prior_corpus = prior_corpus
            self.prior_corpus_mean_std = CorpusMeanAndStd(corpus=self.prior_corpus)
        self.current_corpus = build_corpus(harmonic_rhythm, time_tweet_corpus)
        self.harmonic_rhythm = harmonic_rhythm

    def run(self):
        time_passed = 0
        for key in self.current_corpus.keys():
            time_passed += float(key)
            if time_passed > self.harmonic_rhythm:
                if self.prior_corpus == None:
                    return neoriemannian_walk_dummy(0, 0)
                else:
                    current_corpus_mean_std = CorpusMeanAndStd(corpus=self.current_corpus)
                    diff = self.prior_corpus_mean_std - current_corpus_mean_std
                    self.prior_corpus = self.current_corpus
                    self.prior_corpus_mean_std = current_corpus_mean_std
                    return neoriemannian_walk_dummy(diff.mean, diff.std)
            else:
                print("Waiting {}".format(key))
                time.sleep(float(key))
                trigger_sound(self.current_corpus[key])

    def get_and_set_new_corpus(self, time_tweet_corpus):
        self.current_corpus = build_corpus(self.harmonic_rhythm, time_tweet_corpus)


def simulator(time_tweet_corpus, harmonic_rhythm=30):
    time_passed = 0
    corpus = build_corpus(harmonic_rhythm, time_tweet_corpus)




if __name__ == '__main__':
    file_path = "/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/Corpora/TwiConv/time_and_tweets.json"

    with open(file_path, 'r') as file:
        tweets = json.load(file)

    print(CorpusMeanAndStd(2.44, 34.45))
    print(CorpusMeanAndStd(corpus=build_corpus(30, tweets)))

    simulation = TweetsIncomingSim(tweets)
    print(simulation.run())

