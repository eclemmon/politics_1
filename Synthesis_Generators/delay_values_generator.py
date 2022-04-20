from Data_Dumps import pos_tags


def delay_time_and_decay(pos_count_dict: dict,
                         noun_tags: list = pos_tags.penn_treebank_pos_nouns,
                         verb_tags: list = pos_tags.penn_treebank_pos_verbs):
    """
    This function counts the number of nouns and verbs in a string and returns them as a tuple.
    :param pos_count_dict: dict that maps pos tag as string to an integer count e.g. {'NN': 4, 'VB': 2}
    :param noun_tags: list of noun pos tags based on the tagger used. e.g. ['NN', 'NNS', etc...]
    :param verb_tags: list of verb pos tags based on the tagger used. e.g. ['VB', 'VBZ', etc...]
    :return: tuple e.g. (4, 2)
    """
    nouns = 0
    verbs = 0
    for tag in noun_tags:
        if pos_count_dict.get(tag) is not None:
            nouns += pos_count_dict.get(tag)
        else:
            pass
    for tag in verb_tags:
        if pos_count_dict.get(tag) is not None:
            verbs += pos_count_dict.get(tag)
        else:
            pass
    return nouns, verbs
