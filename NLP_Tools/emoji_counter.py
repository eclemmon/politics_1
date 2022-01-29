import emoji
import emosent
from nltk.tokenize import word_tokenize
from NLP_Tools.sentiment_dictionary import SentimentDict


def is_emoji(token):
    if emoji.is_emoji(token):
        return True
    else:
        return False


def count_emojis(tokens):
    count = 0
    for token in tokens:
        if is_emoji(token):
            count += 1
    return count


def get_emoji_sentiment(token):
    rank = emosent.get_emoji_sentiment_rank(token)
    return {'neg': rank['negative'],
            'neu': rank['neutral'],
            'pos': rank['positive'],
            'compound': rank['sentiment_score']}


def get_emojis(text):
    tokens = word_tokenize(text)
    emojis = []
    for token in tokens:
        if is_emoji(token):
            emojis.append(token)
    return emojis


def get_average_emoji_sent_from_msg(emojis: list):
    sent_dict = SentimentDict()

    if len(emojis) <= 0:
        return None
    else:
        for emo in emojis:
            emoji_sent = SentimentDict(get_emoji_sentiment(emo))
            sent_dict.add_value_average(emoji_sent)
        return sent_dict

