
def generate_spatialization_values(time_interval: int, sentiment_dict: dict):
    """
    Generates spatialization values. Data that determines spatialization:
    Motion = starting point to inverse starting point,
    time_interval = length of message. 280 max.
    Starting point = Composite Sentiment,
    Target = Inverse Sentiment val
    So if composite sentiment is -0.5 in value, will find the value of the avg. positive sentiment of the document
    and use that as the target destination.
    :param time_interval: int
    :param sentiment_dict: dict
    :return: list of floats
    """
    start_point = sentiment_dict['compound']
    if start_point > 0:
        target_sent = 'neg'
    elif start_point == 0:
        target_sent = 'neu'
    else:
        target_sent = 'pos'
    target = sentiment_dict[target_sent]
    return [time_interval, start_point, target]


