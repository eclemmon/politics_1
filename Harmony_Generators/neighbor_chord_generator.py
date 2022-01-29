from Utility_Tools.map_vectors import get_graph_chord_indexes_and_weights


def generate_neighbor_chord_weights(sentiment_dict, num_adj_chords):
    sent = {'neg': sentiment_dict['neg'], 'neu': sentiment_dict['neu'], 'pos': sentiment_dict['pos']}
    return get_graph_chord_indexes_and_weights(sent, num_adj_chords)


def build_weight_and_chord_array(current_chord, neighbor_notes, weights):
    res = []
    for k, v in weights.items():
        if k == 'home':
            res.append(weights['home'])
            res.append(len(current_chord))
            res += current_chord
        else:
            res.append(v)
            res.append(len(neighbor_notes[k]))
            res += neighbor_notes[k]
    return res
