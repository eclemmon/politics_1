import random
import hashlib


class InstrumentKeyAndNameGenerator:
    """
    InstrumentKeyAndNameGenerator class to help in constructing sound selection to be passed to SuperCollider.
    """
    def __init__(self, inst_names: list, max_no_instruments: int):
        """
        Initialization for InstrumentKeyAndNameGenerator
        :param inst_names: list of instrument names available, e.g. ['sin', 'saw']
        :param max_no_instruments: int of maximum number of instruments allowed, purely a safety value to cap
        the number of instruments allowed to run. Set at object construction time.
        """
        self.total_no_instruments = len(inst_names)
        self.instrument_dict = generate_instrument_dict(inst_names)
        self.instrument_graph = generate_instrument_graph(self.instrument_dict)
        self.max_instruments = max_no_instruments
        self.instrument_keys = ['sound{}'.format(count + 1) for count in range(len(inst_names))]

    def get_instrument_chain_keys(self, sent_dict: dict, emoji_sent_dict: dict, num_inst_to_run: int = 4):
        """
        Gets the keys for instruments to be activated in SuperCollider.
        :param sent_dict: dict String: Float. e.g. {'pos': 0.736...etc}
        :param emoji_sent_dict: dict String: Float. e.g. {'pos': 0.736...etc}
        :param num_inst_to_run: int of number of instruments in final array.
        :return: list of instrument keys. e.g. ['sound3', 'sound4', 'sound6', 'sound5', 'sound3']
        """
        return get_instrument_chain(num_inst_to_run - 1, self.instrument_graph, sent_dict,
                                    emoji_sent_dict, self.total_no_instruments, self.instrument_keys,
                                    self.max_instruments)

    def get_instrument_chain_names(self, instrument_keys: list):
        """
        Gets a list of the instrument names to pass to SuperCollider
        :param instrument_keys: keys in the instrument key dict. ['sound1', 'sound2']
        :return: List of instrument names ['sin', 'saw']
        """
        return [self.instrument_dict[key] for key in instrument_keys]

    def get_n_instrument_chain_names(self, instrument_keys: list, num_insts: int):
        """
        Gets a list of n instrument names to pass to SuperCollider
        :param instrument_keys: list of keys in the instrument key dict. ['sound1', 'sound2']
        :param num_insts: int of number of instruments desired.
        :return: list of strs, instrument names ['sin', 'saw']
        """
        instruments = self.get_instrument_chain_names(instrument_keys)
        return instruments[:num_insts]


def generate_instrument_dict(inst_names: list):
    """
    Builds a dictionary of instruments that are agnostic to the names inserted. Keys are organized as
    'sound[i+1]': 'name' based on the instrument_names_sc list input.
    :param inst_names: list of instrument names e.g., ['sin', 'crazyness']
    :return: dict of String: String e.g., {'sound1': 'sin', 'sound2': 'crazyness'}
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
    :param instrument_dict: dict of String: String. e.g. {'sound1': 'sin'}
    :return: dict of String: List. e.g. {'sound1': ['sound2', 'sound3', 'sound4', 'sound5', 'sound6']}
    """
    keys = list(instrument_dict.keys())
    graph = {}
    for count, key in enumerate(keys):
        if keys[count] == key:
            graph[key] = keys[:count] + keys[count + 1:]
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
    index = int(better_hash(value) % total_no_instruments - 1)
    return inst_graph[current_instrument][index]


def get_first_instrument(value: float, instrument_keys: list, total_no_instruments: int):
    """
    Helper function that gets the first instrument key name. Returns a string of the first instrument key
    :param instrument_keys: List of instrument keys
    :param value: Float of value to be hashed.
    :param total_no_instruments: Integer of total number of instruments available.
    :return: String of first instrument. e.g. 'sound1'
    """
    index = (better_hash(value) % total_no_instruments)
    return instrument_keys[index]


def get_instrument_chain(num_inst_to_run: int, inst_graph: dict, sentiment_dict: dict,
                         emoji_sentiment, total_no_instruments: int, instrument_keys: list, max_inst_to_run=4):
    """
    Returns an array of instruments that can be passed to SuperCollider for runtime.
    :param instrument_keys: List of instrument keys.
    :param max_inst_to_run: Integer of maximum instruments to run. Default is 4.
    :param num_inst_to_run: Integer of number of instruments in final array.
    :param inst_graph: Dict of String: List. e.g. {'sound1': ['sound2', 'sound3', 'sound4', 'sound5', 'sound6']}
    :param sentiment_dict: Dict String: Float. e.g. {'pos': 0.736...etc}
    :param emoji_sentiment: Dict String or NoneType: Float. e.g. {'pos': 0.736...etc}, None
    :param total_no_instruments: Integer of total number of instruments
    :return: List of instrument keys. e.g. ['sound3', 'sound4', 'sound6', 'sound5', 'sound3']
    """
    if num_inst_to_run > max_inst_to_run:
        num_inst_to_run = 4

    res = [get_first_instrument(sentiment_dict['compound'], instrument_keys, total_no_instruments)]

    if emoji_sentiment is not None:
        values = list(sentiment_dict.values()) + list(emoji_sentiment.values())
    else:
        values = list(sentiment_dict.values())

    for _ in range(num_inst_to_run):
        res.append(get_next_instrument(inst_graph, res[-1], values[_], total_no_instruments))
    return res


def better_hash(to_be_hashed):
    """
    Function to hash an input object with a hashing function that generates more random values.
    :param to_be_hashed: Object
    :return: int
    """
    return int.from_bytes(hashlib.sha3_256(repr(to_be_hashed).encode()).digest()[:8], 'little')


if __name__ == "__main__":
    from Data_Dumps.instrument_names import instrument_names_sc
    from Data_Dumps.instrument_names import instrument_indices_daw
    from NLP_Tools.emoji_counter import get_emoji_sentiment

    key_gen = InstrumentKeyAndNameGenerator(instrument_indices_daw, 16)
    keys = key_gen.get_instrument_chain_keys({'neg': 0.24, 'neu': 0.955466, 'pos': 0.245, 'compound': -1},
                                            None)
    print(key_gen.get_n_instrument_chain_names(keys, 4))
