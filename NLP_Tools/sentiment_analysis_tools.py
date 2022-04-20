import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from statistics import mean


def get_sentiment_with_text(sentiment_analyzer: SentimentIntensityAnalyzer, text: str):
    """
    Gets the sentiment of each sentence in a text and returns the sentence as key and value of a dict of the sentiment.
    :param sentiment_analyzer: SentimentIntensityAnalyzer
    :param text: str
    :return: dict {sentence1: {polarity_score}, sentence2: {polarity_score}...}
    """
    sentences = tokenize.sent_tokenize(text, language="english")
    return {sentence: sentiment_analyzer.polarity_scores(sentence) for sentence in sentences}


def get_sentiment(sentiment_analyzer: SentimentIntensityAnalyzer, text: str):
    """
    Gets the sentiment of each sentence in a text and returns only the dict polarity scores as a list.
    :param sentiment_analyzer: SentimentIntensityAnalyzer
    :param text: str
    :return: list of dicts [{polarity_score1}, {polarity_score2}...]
    """
    sentences = tokenize.sent_tokenize(text, language="english")
    return [sentiment_analyzer.polarity_scores(sentence) for sentence in sentences]


def get_average_sentiment(sentiment_analyzer: SentimentIntensityAnalyzer, text: str):
    """
    Gets the average sentiment of the entire text (delineated by taking the mean of all the polarity
    scores of each sentence).
    :param sentiment_analyzer: SentimentIntensityAnalyzer
    :param text: str
    :return: dict of mean_polarity_score
    """
    sentences = tokenize.sent_tokenize(text, language="english")
    sentiments = [sentiment_analyzer.polarity_scores(sentence) for sentence in sentences]
    sentiment_mean = {}
    keys = ['neg', 'neu', 'pos', 'compound']
    for key in keys:
        val = []
        for d in sentiments:
            val += [d[key]]
        sentiment_mean[key] = mean(val)
    return sentiment_mean


if __name__ == "__main__":
    file_path = "/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/Corpora/TwiConv/time_and_tweets.json"

    with open(file_path, 'r') as file:
        tweets = json.load(file)

    # simulation = TweetsIncomingSim(tweets)
    sentiment_analyzer = SentimentIntensityAnalyzer()
    text = "I love the train! Let me get on it fam! Woohoo! I HATE the Train"
    print(get_sentiment_with_text(sentiment_analyzer, text=text))
    print(get_sentiment(sentiment_analyzer, text=text))
    print(get_average_sentiment(sentiment_analyzer, text=text))
