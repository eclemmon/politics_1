from Utility_Tools.logistic_function import linear_to_logistic as l2l


def get_octave_placement(text):
    length = len(text)
    return int(l2l(length, 0, 280, 21, 108, 0.5)) // 12
