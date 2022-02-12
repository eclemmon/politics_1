from Utility_Tools.mapping_functions import linear_to_logistic as lin2sigmoid
from Utility_Tools.mapping_functions import linear_to_linear as lin2lin


def get_octave_placement_sigmoid(text):
    length = len(text)
    return int(lin2sigmoid(length, 0, 280, 96, 24, -0.3)) // 12


def get_octave_placement_linear(text):
    length = len(text)
    if length > 144:
        length = 144
    elif length < 0:
        length = 0
    else:
        length = length
    return int(lin2lin(length, 0, 54, 96, 24)) // 12
