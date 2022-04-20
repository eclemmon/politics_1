from nltk import tokenize
from nltk import pos_tag


def get_pos_tuples(text: str):
    """
    Gets tuples of the parts of speech of a text
    :param text: str
    :return: list of lists of tuples. e.g. [[('I', 'PRP'), ('love', 'VBP')], [('Let', 'VB'), ('me', 'PRP')]]
    """
    res = []
    sentences = tokenize.sent_tokenize(text, language="english")
    sentences = [tokenize.word_tokenize(sentence) for sentence in sentences]
    for sentence in sentences:
        res.append(pos_tag(sentence))
    return res


def count_discrete_pos(pos_count_dict: dict):
    """
    Counts the number of different parts of speech in a pos_count_dict
    :param pos_count_dict: Dict. e.g. {'PRP': 3}
    :return: int
    """
    return len(pos_count_dict)


def count_total_pos(pos_count_dict: dict):
    """
    Counts the total number of parts of speech
    :param pos_count_dict: Dict. e.g. {'PRP': 3}
    :return: int
    """
    res = 0
    for value in pos_count_dict.values():
        res += value
    return res


def build_pos_count_dict(text: str):
    """
    Builds a dictionary of parts of speech as the key and the number of each POS as the value.
    :param text: str.
    :return: dict {str: int}. e.g. {'PRP': 3, 'VBP': 1, 'DT': 1, 'NN': 2, '.': 3, 'VB': 2, 'IN': 1, 'VBZ': 1}
    """
    pos_count = {}
    for sentence in get_pos_tuples(text):
        for word in sentence:
            pos_count[word[1]] = pos_count.get(word[1], 0) + 1
    return pos_count


if __name__ == "__main__":
    # file_path = "/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/Corpora/TwiConv/time_and_tweets.json"
    #
    # with open(file_path, 'r') as file:
    #     tweets = json.load(file)
    #
    # simulation = TweetsIncomingSim(tweets)
    # sentiment_analyzer = SentimentIntensityAnalyzer()
    text = "I love the train! Let me get on it fam! Woohoo!"
    pos_count_dict = build_pos_count_dict(text)
    print(pos_count_dict)
    print(get_pos_tuples(text))
    print(count_discrete_pos(pos_count_dict))
    print(count_total_pos(pos_count_dict))