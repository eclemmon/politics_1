import numpy
import pandas
import json
from fuzzywuzzy import fuzz
from typing import Union


class CorpusMeanAndStd:
    def __init__(self, mean: Union[float, None] = None, std: Union[float, None] = None,
                 corpus: Union[float, None] = None):
        """
        Constructs an object that helps find a corpus's mean topic value and the standard of deviation from the mean.
        :param mean: float || None
        :param std: float || None
        :param corpus: list || None
        """
        if mean is None or std is None:
            try:
                mean_and_std = mean_and_std_of_corpus(corpus)
                self.mean = mean_and_std[0]
                self.std = mean_and_std[1]
            except RuntimeError:
                print("Something went wrong, you need to include either both a mean and a std value, or a corpus only")
        else:
            # assert (isinstance(mean, float) and isinstance(std, float))
            self.mean = mean
            self.std = std

    def __sub__(self, other):
        """
        Class override function for subtracting one CorpusMeanAndStd from another
        :param other: CorpusMeanAndStd
        :return: CorpusMeanAndStd
        """
        print(self, other)
        new_mean = self.mean - other.mean
        new_std = self.std - other.std
        return CorpusMeanAndStd(new_mean, new_std)

    def __add__(self, other):
        """
        Class override function for adding one CorpusMeanAndStd to another
        :param other: CorpusMeanAndStd
        :return: CorpusMeanAndStd
        """
        new_mean = self.mean + other.mean
        new_std = self.std + other.std
        return CorpusMeanAndStd(new_mean, new_std)

    def __str__(self):
        """
        Class override for string representation of CorpusMeanAndStd
        :return: str
        """
        return "{}, {}".format(self.mean, self.std)

    def __repr__(self):
        """
        Class override for representation of CorpusMeanAndStd
        :return: str
        """
        return '<{0}.{1} object at {2} || {3}>'.format(
            type(self).__module__, type(self).__qualname__, hex(id(self)), self.__str__())

    def average(self, other):
        """
        Function to get the average mean and std of two CorpusMeanAndStds
        :param other: CorpusMeanAndStd
        :return: CorpusMeanAndStd
        """
        new_mean = (self.mean + other.mean) / 2
        new_std = (self.std + other.std) / 2
        return CorpusMeanAndStd(new_mean, new_std)


def mean_and_std_of_corpus(corpus: list):
    """
    Builds mean and standard of deviation after determining levenshtein distance between texts in a corpus.
    :param corpus: list
    :return: tuple
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
    if len(l_tri) <= 0:
        return 0, 0
    else:
        return l_tri.mean(), l_tri.std()


if __name__ == '__main__':
    file_path = "/Users/ericlemmon/Documents/musical_practice/compositions/electronic_works/politics_1/Corpora/TwiConv/time_and_tweets.json"

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

