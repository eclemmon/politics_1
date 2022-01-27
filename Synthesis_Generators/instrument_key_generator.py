
def generate_instrument_dict(inst_names: list):
    """
    Builds a dictionary of instruments that are agnostic to the names inserted. Keys are organized as
    'sound[i+1]': 'name' based on the instrument_names list input.
    :param inst_names: List of instrument names e.g., ['sin', 'crazyness']
    :return: Dictionary of String:String e.g., {'sound1': 'sin', 'sound2': 'crazyness'}
    """
    instrument_dict = {}
    for count, name in enumerate(inst_names):
        key = 'sound{}'.format(count + 1)
        instrument_dict[key] = name
    return instrument_dict


def generate_instrument_graph(instrument_dict: dict):
    """
    Iterates through the keys of the instrument_dict and maps the key to an array of the other key names in the
    instrument_dict key set.
    :param instrument_dict: Dictionary of String: String. e.g. {'sound1': 'sin'}
    :return: Dictionary of String: List. e.g. {'sound1': ['sound2', 'sound3', 'sound4', 'sound5', 'sound6']}
    """
    keys = list(instrument_dict.keys())
    graph = {}
    for count, key in enumerate(keys):
        if keys[count] == key:
            graph[key] = keys[:count] + keys[count+1:]
    return graph


def get_next_instrument(inst_graph: dict, current_instrument: str, value: float, total_no_instruments: int):
    """
    Helper function that gets the next instrument by determining the next instrument index through hashing the input
    value to get a deterministic random number and getting the modulo of the number of instruments available.
    Returns the next instrument key name.
    :param inst_graph: Dictionary of String: List. e.g.
    {'sound1': ['sound2', 'sound3', 'sound4', 'sound5', 'sound6']}
    :param current_instrument: String of the current instrument. e.g. 'sound1'
    :param value: Float of value to be hashed and converted to an instrument.
    :param total_no_instruments: Integer of number of instruments.
    :return: String of next instrument key name. e.g. 'sound2'
    """
    index = hash(value) % total_no_instruments
    return inst_graph[current_instrument][index]


def get_first_instrument(value: float, total_no_instruments: int):
    """
    Helper function that gets the first instrument key name. Returns a string of the first instrument key
    :param value: Float of value to be hashed.
    :param total_no_instruments: Integer of total number of instruments available.
    :return: String of first instrument. e.g. 'sound1'
    """
    instrument_keys = ['sound{}'.format(count + 1) for count in range(total_no_instruments)]
    index = (hash(value) % total_no_instruments)
    return instrument_keys[index]
# TODO: defer some work done in this function to an object that can be passed around or that can be instantiated at run
#  time.


def get_instrument_chain(num_inst_to_run: int, inst_graph: dict, sentiment_dict: dict,
                         emoji_sentiment: dict, total_no_instruments: int):
    """
    Returns an array of instruments that can be passed to SuperCollider for runtime.
    :param num_inst_to_run: Integer of number of instruments in final array. Max is 4.
    :param inst_graph: Dict of String: List. e.g. {'sound1': ['sound2', 'sound3', 'sound4', 'sound5', 'sound6']}
    :param sentiment_dict: Dict String: Float. e.g. {'pos': 0.736...etc}
    :param emoji_sentiment: Dict String: Float. e.g. {'pos': 0.736...etc}
    :param total_no_instruments: Integer of total number of instruments
    :return: List of instrument keys. e.g. ['sound3', 'sound4', 'sound6', 'sound5', 'sound3']
    """
    if num_inst_to_run > 4:
        num_inst_to_run = 4

    res = [get_first_instrument(sentiment_dict['compound'], total_no_instruments)]
    values = list(sentiment_dict.values()) + list(emoji_sentiment.values())
    for _ in range(num_inst_to_run):
        res.append(get_next_instrument(inst_graph, res[-1], values[_], total_no_instruments))
    return res


if __name__ == "__main__":
    from Data_Dumps.instrument_names import instrument_names
    from NLP_Tools.emoji_counter import get_emoji_sentiment
    instrument_graph = generate_instrument_graph(generate_instrument_dict(instrument_names))
    print(instrument_graph)
    print(get_instrument_chain(4, instrument_graph, {'neg': 0.4734343, 'neu': 0.657, 'pos': 0.403, 'compound': -0.863},
                               get_emoji_sentiment("❤"), len(instrument_names)))