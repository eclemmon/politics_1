from NLP_Tools.sentiment_dictionary import SentimentDict


def phase_mod_values_generator(avg_emoji_sent: SentimentDict, emojis: str):
    """
    Function to generate values for phase modulation in SuperCollider by reading sentiment of emojis and num of emojis.
    :param avg_emoji_sent: SentimentDict
    :param emojis: str
    :return: tuple of (float, float)
    """
    if avg_emoji_sent is None:
        return 0, 0
    else:
        return len(emojis), avg_emoji_sent.sent_dict['compound']
