from Utility_Tools.mapping_functions import linear_to_logistic as l2l


def get_octave_placement_sigmoid(text):
    length = len(text)
    return int(l2l(length, 0, 280, 96, 24, -0.3)) // 12

def get_octave_placement_linear(text):
    length = len(text)
