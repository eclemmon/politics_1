import unittest
from nose2.tools import params
from NLP_Tools.corpus_mean_and_std import *

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


class TestCorpusMeanStd(unittest.TestCase):
    def setUp(self):
        self.corpus_one = CorpusMeanAndStd(2.44, 34.45)
        self.corpus_two = CorpusMeanAndStd(corpus=build_short_corpus(30, tweets))

    def test_corpus_constructed(self):
        self.assertEquals(type(self.corpus_one), type(CorpusMeanAndStd(0.0, 0.0)))
        self.assertEquals(type(self.corpus_two), type(CorpusMeanAndStd(0.0, 0.0)))

    def test_corpus_print(self):
        self.assertEquals(self.corpus_one.__repr__(), "2.44, 34.45")

    def test_mean_and_std_of_corpus(self):
        short_corpus = build_short_corpus(30, tweets)
        self.assertEquals(mean_and_std_of_corpus(short_corpus), (31.90394088669951, 10.28165587459526))


