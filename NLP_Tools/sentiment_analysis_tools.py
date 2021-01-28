import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from statistics import mean
from nltk import pos_tag
from Testing_Scripts.simulation_incoming_tweets import TweetsIncomingSim


def get_sentiment_with_text(sentiment_analyzer, text):
    """

    :param sentiment_analyzer:
    :param text:
    :return:
    """
    sentences = tokenize.sent_tokenize(text, language="english")
    return {sentence: sentiment_analyzer.polarity_scores(sentence) for sentence in sentences}

def get_sentiment(sentiment_analyzer, text):
    sentences = tokenize.sent_tokenize(text, language="english")
    return [sentiment_analyzer.polarity_scores(sentence) for sentence in sentences]

def get_average_sentiment(sentiment_analyzer, text):
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
