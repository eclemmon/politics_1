import emoji
import emosent
from nltk.tokenize import word_tokenize
from NLP_Tools.sentiment_dictionary import SentimentDict


def is_emoji(token: str):
    """
    Helper function for determining whether an emoji is an emoji.
    :param token: str
    :return: boolean
    """
    if emoji.is_emoji(token):
        return True
    else:
        return False


def count_emojis(tokens: str):
    """
    Helper function for counting emojis.
    :param tokens: str
    :return: int
    """
    count = 0
    for token in tokens:
        if is_emoji(token):
            count += 1
    return count


def get_emoji_sentiment(token: str):
    """
    Function for getting the sentiment of an emoji and converting it into the same key, val pairings as NLTK's VADER
    :param token: str
    :return: dict
    """
    try:
        rank = emosent.get_emoji_sentiment_rank(token)
    except:
        rank = {'negative': 0.0, 'neutral': 0.0, 'positive': 0.0, 'sentiment_score': 0.0}
    finally:
        return {'neg': rank['negative'],
                'neu': rank['neutral'],
                'pos': rank['positive'],
                'compound': rank['sentiment_score']}


def get_emojis(text: str):
    """
    Scans a text for emojis and returns all of them as a list
    :param text: str
    :return: list
    """
    tokens = word_tokenize(text)
    emojis = []
    for token in tokens:
        if is_emoji(token):
            emojis.append(token)
    return emojis


def get_average_emoji_sent_from_msg(emojis: list):
    """
    Gets the average sentiment of emojis and returns it as a SentimentDict() object.
    :param emojis: list of emojis
    :return: SentimentDict
    """
    sent_dict = SentimentDict()

    if len(emojis) <= 0:
        return sent_dict
    else:
        for emo in emojis:
            emoji_sent = SentimentDict(get_emoji_sentiment(emo))
            sent_dict.add_value_average(emoji_sent)
        return sent_dict

