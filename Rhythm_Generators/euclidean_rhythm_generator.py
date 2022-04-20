from NLP_Tools.part_of_speech_tools import count_discrete_pos
from nltk import tokenize


def generate_euclidean(onsets: int, pulses: int):
    """
    Generates a euclidean rhythm based on the onsets and pulses offered.
    :param onsets: int - Num of onsets of musical events
    :param pulses: int - Num of pulses to be divided up over the onsets.
    :return: list of 1s and 0s, e.g. [1,0,1,0,1,0,0]
    """
    front = [[1] for i in range(onsets)]
    back = [[0] for i in range(pulses)]
    return [item for sublist in euclidian_recursive(front, back) for item in sublist]


def euclidian_recursive(front: list, back: list):
    """
    Generates the list of lists based on grouped subunits of a euclidean rhythm based on the two lists of 1s and
    0s fed in
    :param front: list of 1s [1,1,1,1]
    :param back: list of 0s [0,0,0,0,0,0]
    :return: list of lists grouped with a 1 as onset and 0 as trailing post. [[1,0],[1,0],[1,0,0]]
    """
    if len(back) <= 1:
        return front+back
    else:
        new_front = []
        while len(front) > 0 and len(back) > 0:
            new_front.append(front.pop()+back.pop())
        return euclidian_recursive(new_front, back+front)


def euclidian_splitter(euclidian_rhythm_1d_list):
    """
    Takes in a euclidean rhythm list and splits it into a list of lists organized by onsets grouped with
    trailing pulses.
    :param euclidian_rhythm_1d_list: list e.g. [1,0,0,1,0,1,0]
    :return: list of lists, e.g., [[1, 0, 0], [1, 0], [1, 0], [1, 0, 0], [1, 0], [1, 0]]
    """
    # This can be done better....
    res = []
    sub_array = []
    while len(euclidian_rhythm_1d_list) > 0:
        val = euclidian_rhythm_1d_list.pop(0)
        if val == 1:
            res.append(sub_array)
            sub_array = [1]
        else:
            sub_array.append(val)
    res.append(sub_array)
    return res[1:]


def impulse_offset_generator(text):
    """
    Takes in a text and counts the number of tokens and number o discrete parts of speech.
    :param text: str e.g., "This is a sentence"
    :return: tuple of integers e.g., (4, 3)
    """
    discrete_pos = count_discrete_pos(text)
    tokens = len(tokenize.word_tokenize(text))
    return tokens, discrete_pos


if __name__ == '__main__':
    print(generate_euclidean(6, 8))
    euc = generate_euclidean(6, 8)
    print(euclidian_splitter(euc))
    print(impulse_offset_generator("This is a sentence"))

