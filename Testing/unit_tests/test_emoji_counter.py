import unittest
from NLP_Tools.emoji_counter import is_emoji
from nltk.tokenize import word_tokenize
from nltk.tokenize.casual import TweetTokenizer
from NLP_Tools.emoji_counter import count_emojis
from NLP_Tools.emoji_counter import get_emoji_sentiment

tweet_tokenizer = TweetTokenizer()
tokens_one = word_tokenize("Academic freedom guaranteed by tenure is more than a hiring gimmick. Georgia cannot compete for talent or produce innovation if we undermine our public universities. @BORUSG has already abandoned the physical health of our schools. Let’s not destroy intellectual capacity as well.")
tokens_two = word_tokenize("oh my gooOooOdness what a precious little angel!! ❤️ ❤️")
tokens_three = tweet_tokenizer.tokenize("Super stars 😔 😔🌟 🌟 🌟 😁 🥶")

class TestEmojiCounter(unittest.TestCase):
    def test_tokens_three_len_nine(self):
        self.assertEqual(len(tokens_three), 9)

    def test_is_emoji(self):
        self.assertTrue(is_emoji("❤️"))
        self.assertFalse(is_emoji("yes I am lol"))

    def test_count_emojis(self):
        self.assertEqual(count_emojis(tokens_one), 0)
        self.assertEqual(count_emojis(tokens_two), 2)
        self.assertEqual(count_emojis(tokens_three), 7)

    def test_get_emoji_sentiment(self):
        self.assertEqual(get_emoji_sentiment("❤"), {'neg': 355,
                                                    'neu': 1334,
                                                    'pos': 6361,
                                                    'composite': 0.746})
