import emoji
import emosent

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
            'composite': rank['sentiment_score']}
