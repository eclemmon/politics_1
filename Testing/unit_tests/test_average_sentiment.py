import unittest
from NLP_Tools.sentiment_dictionary import SentimentDict

avg_sent = SentimentDict()


class TestSentimentDict(unittest.TestCase):
    def test_add_average_sentiment_init(self):
        self.assertDictEqual(avg_sent.sent_dict, {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0})
        self.assertEqual(avg_sent.x_averaged, 1)
        self.assertIsInstance(avg_sent, SentimentDict)

    def test_add_average_sentiment_average(self):
        ones = SentimentDict({'neg': 1, 'neu': 1, 'pos': 1, 'compound': 1})
        self.assertDictEqual(avg_sent.average(ones).sent_dict, {'neg': 0.5, 'neu': 0.5, 'pos': 0.5, 'compound': 0.5})

    def test_add_average_sentiment_add_value_average(self):
        add_val_avg_once = avg_sent.add_value_average(SentimentDict({'neg': 1, 'neu': 1, 'pos': 1, 'compound': 1}))
        res = SentimentDict({'neg': 0.5, 'neu': 0.5, 'pos': 0.5, 'compound': 0.5})
        self.assertDictEqual(add_val_avg_once.sent_dict, res.sent_dict)

    def test_abs_difference(self):
        sd1 = SentimentDict({'neg': 0.5, 'neu': 0.75, 'pos': -0.5, 'compound': 0.5})
        sd2 = SentimentDict({'neg': 1, 'neu': 0.70, 'pos': 0.5, 'compound': -1.0})
        res = sd1.abs_difference(sd2).sent_dict
        testcase = {'neg': 0.5, 'neu': 0.05, 'pos': 1, 'compound': 1.5}
        for k, v in res.items():
            self.assertAlmostEqual(res[k], testcase[k])

