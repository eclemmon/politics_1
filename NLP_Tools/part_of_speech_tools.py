from nltk import tokenize
from nltk import pos_tag


def get_pos_tuples(text):
    res = []
    sentences = tokenize.sent_tokenize(text, language="english")
    sentences = [tokenize.word_tokenize(sentence) for sentence in sentences]
    for sentence in sentences:
        res.append(pos_tag(sentence))
    return res


def count_discrete_pos(pos_count_dict):
    return len(pos_count_dict)


def count_total_pos(pos_count_dict):
    res = 0
    for value in pos_count_dict.values():
        res += value
    return res


def build_pos_count_dict(text):
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