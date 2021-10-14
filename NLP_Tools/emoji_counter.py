import emoji

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

