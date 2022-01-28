import unittest
from NLP_Tools.average_sentiment import AverageSentiment

avg_sent = AverageSentiment()

class TestAverageSentiment(unittest.TestCase):
    def test_add_average_sentiment_init(self):
        self.assertDictEqual(avg_sent.avg_sent, {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0})
        self.assertEqual(avg_sent.x_averaged, 1)
        self.assertIsInstance(avg_sent, AverageSentiment)

    def test_add_average_sentiment_average(self):
        ones = AverageSentiment({'neg': 1, 'neu': 1, 'pos': 1, 'compound': 1})
        self.assertDictEqual(avg_sent.average(ones).avg_sent, {'neg': 0.5, 'neu': 0.5, 'pos': 0.5, 'compound': 0.5})

    def test_add_average_sentiment_add_value_average(self):
        rand_sent_dict = AverageSentiment({'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0.0})
        add_val_avg_once = avg_sent.add_value_average(AverageSentiment({'neg': 1, 'neu': 1, 'pos': 1, 'compound': 1}))
        res = AverageSentiment({'neg': 0.5, 'neu': 0.5, 'pos': 0.5, 'compound': 0.5})
        self.assertDictEqual(add_val_avg_once.avg_sent, res.avg_sent)

