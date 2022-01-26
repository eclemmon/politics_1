# TODO: Data that determines spatialization <== Motion == starting point -> inverse starting point, time
# TODO: {time = length of message. 280 max. Starting point = Composite Sentiment, Target = Inverse Sentiment val}

def generate_spatialization_values(time, sentiment_dict):
    starting_point = sentiment_dict['compound']
    if starting_point > 0:
        target_sent = 'neg'
    elif starting_point == 0:
        target_sent = 'neu'
    else:
        target_sent = 'pos'
    target = sentiment_dict[target_sent]
    return [time, starting_point, target]


