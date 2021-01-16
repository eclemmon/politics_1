import numpy
import pandas
import json
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


def mean_and_std_of_corpus(corpus):
    """
    Builds mean and std after determining levenshtein distance between two texts in a corpus.
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


if __name__ == '__main__':
    file_path = "/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/Corpora/TwiConv/time_and_tweets.json"

    with open(file_path, 'r') as file:
        tweets = json.load(file)


    def build_short_corpus(timing, test_corpus):
        time = 0
        corpus = {}
        for key in test_corpus.keys():
            time += float(key)
            if time > timing:
                break
            else:
                corpus[key] = tweets[key]
        return corpus

    print(CorpusMeanAndStd(2.44, 34.45))
    print(CorpusMeanAndStd(corpus=build_short_corpus(30, tweets)))  # should be 31.903..., 10.281...
