# Data that determines spatialization <== Motion == starting point -> inverse starting point, time_interval
# {time_interval = length of message. 280 max. Starting point = Composite Sentiment, Target = Inverse Sentiment val}

def generate_spatialization_values(time_interval, sentiment_dict):
    start_point = sentiment_dict['compound']
    if start_point > 0:
        target_sent = 'neg'
    elif start_point == 0:
        target_sent = 'neu'
    else:
        target_sent = 'pos'
    target = sentiment_dict[target_sent]
    return [time_interval, start_point, target]


