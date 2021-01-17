import time
import json
from NLP_Tools import corpus_mean_and_std


class TweetsIncomingSim:
    def __init__(self, full_corpus, harmonic_rhythm=30):
        self.time_and_tweets = self.time_and_tweet_gen(full_corpus)
        self.harmonic_rhythm = harmonic_rhythm
        self.current_partial_corpus = {}
        self.prior_partial_corpus = None
        self.prior_corpus_mean_std = corpus_mean_and_std.CorpusMeanAndStd(0.0, 0.0)

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
                if time_passed >= self.harmonic_rhythm:
                    if self.prior_partial_corpus is None:
                        neoriemannian_walk_dummy(0, 0)
                        time_passed = 0
                    else:
                        current_corpus_mean_std = corpus_mean_and_std.CorpusMeanAndStd(
                            corpus=self.current_partial_corpus
                        )
                        diff = self.prior_corpus_mean_std - current_corpus_mean_std
                        self.prior_partial_corpus = self.current_partial_corpus
                        self.current_partial_corpus = {}
                        self.prior_corpus_mean_std = current_corpus_mean_std
                        neoriemannian_walk_dummy(diff.mean, diff.std)
                        time_passed = 0
                else:
                    print("Waiting {}".format(key))
                    time.sleep(float(key))
                    trigger_sound(self.current_partial_corpus[key])
            except StopIteration:
                break


def trigger_sound(data):
    pass


def neoriemannian_walk_dummy(mean, std):
    pass


if __name__ == '__main__':
    file_path = "/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/Corpora/TwiConv/time_and_tweets.json"

    with open(file_path, 'r') as file:
        tweets = json.load(file)

    simulation = TweetsIncomingSim(tweets)
    simulation.run()

