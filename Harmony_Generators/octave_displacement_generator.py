from Utility_Tools.mapping_functions import linear_to_logistic as lin2sigmoid
from Utility_Tools.mapping_functions import linear_to_linear as lin2lin
from nltk.tokenize import word_tokenize


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
    return int(lin2lin(length, 0, 144, 96, 24)) // 12


def get_octave_placement_piecewise(text):
    char_len = len(text)
    if char_len <= 29:
        # Short texts
        return int(lin2lin(char_len, 0, 29, 96, 60)) // 12
    else:
        tokens = word_tokenize(text)
        tokens_len = len(tokens)
        # average word length in english is 4.7 characters
        # round up to 5
        # max characters in text message is 160
        # average num words in max text message len ~ 27 (160 characters = 5 characters * num_words + num_spaces)
        if tokens_len > 27:
            tokens_len = 27
        return int(lin2lin(tokens_len, 0, 27, 60, 24)) // 12


if __name__ == "__main__":
    texts = [
        "and",
        "and above and",
        "to infinite and beyond",
        "here is a string with eight words or so",
        "Here is a long string, LORUM IPSUM, LORUM IPSUM, LORUM IPSUM, LORUM IPSUM, LORUM IPSUM, LORUM IPSUM, LORUM IPSUM"
    ]
    for text in texts:
        print(get_octave_placement_piecewise(text))