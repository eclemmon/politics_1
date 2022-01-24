from Data_Dumps import penn_treebank_pos_tags


def delay_time_and_decay(pos_count_dict,
                         noun_tags=penn_treebank_pos_tags.penn_treebank_pos_nouns,
                         verb_tags=penn_treebank_pos_tags.penn_treebank_pos_verbs):
    """
    This function counts the number of nouns and verbs in a string and returns them as a tuple.
    :param pos_count_dict: Dictionary that maps pos tag as string to an integer count e.g. {'NN': 4, 'VB': 2}
    :param noun_tags: A list of noun pos tags based on the tagger used. e.g. ['NN', 'NNS', etc...]
    :param verb_tags: A list of verb pos tags based on the tagger used. e.g. ['VB', 'VBZ', etc...]
    :return: Tuple e.g. (4, 2)
    """
    nouns = 0
    verbs = 0
    for tag in noun_tags:
        nouns += pos_count_dict[tag]
    for tag in verb_tags:
        verbs += pos_count_dict[verb_tags]
    return nouns, verbs



