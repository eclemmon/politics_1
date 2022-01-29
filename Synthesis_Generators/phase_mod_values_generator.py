from NLP_Tools.emoji_counter import get_average_emoji_sent_from_msg
from NLP_Tools.emoji_counter import get_emojis


def phase_mod_values_generator(text):
    emojis = get_emojis(text)
    avg_emoji_sent = get_average_emoji_sent_from_msg(emojis)
    if avg_emoji_sent is None:
        return 0, 0
    else:
        return len(emojis), avg_emoji_sent.sent_dict['compound']
