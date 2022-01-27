
def generate_instrument_dict(instrument_names):
    instrument_dict = {}
    for count, name in enumerate(instrument_names):
        key = 'sound{}'.format(count + 1)
        instrument_dict[key] = name
    return instrument_dict


def generate_instrument_graph(instrument_dict):
    keys = list(instrument_dict.keys())
    graph = {}
    for count, key in enumerate(keys):
        if keys[count] == key:
            graph[key] = keys[:count] + keys[count+1:]
    return graph


def get_next_instrument(instrument_graph, current_instrument, value, total_no_instruments):
    index = hash(value) % total_no_instruments
    return instrument_graph[current_instrument][index]


def get_first_instrument(value, total_no_instruments):
    instrument_keys = ['sound{}'.format(count + 1) for count in range(total_no_instruments)]
    index = (hash(value) % total_no_instruments)
    return instrument_keys[index]


def get_instrument_chain(num_inst_to_run, instrument_graph, sentiment_dict, emoji_sentiment, total_no_instruments):
    if num_inst_to_run > 4:
        num_inst_to_run = 4

    res = [get_first_instrument(sentiment_dict['compound'], total_no_instruments)]
    values = list(sentiment_dict.values()) + list(emoji_sentiment.values())
    for _ in range(num_inst_to_run):
        res.append(get_next_instrument(instrument_graph, res[-1], values[_], total_no_instruments))
    return res


if __name__ == "__main__":
    from Data_Dumps.instrument_names import instrument_names
    from NLP_Tools.emoji_counter import get_emoji_sentiment
    instrument_graph = generate_instrument_graph(generate_instrument_dict(instrument_names))
    print(instrument_graph)
    print(get_instrument_chain(4, instrument_graph, {'neg': 0.4734343, 'neu': 0.657, 'pos': 0.403, 'compound': -0.863},
                               get_emoji_sentiment("❤"), len(instrument_names)))