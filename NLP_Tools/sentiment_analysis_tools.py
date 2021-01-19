import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk import pos_tag
from Testing_Scripts.simulation_incoming_tweets import TweetsIncomingSim


def get_sentiment(sentiment_analyzer, text):
    sentences = tokenize.sent_tokenize(text, language="english")
    return {sentence: sentiment_analyzer.polarity_scores(sentence) for sentence in sentences}


if __name__ == "__main__":
    file_path = "/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/Corpora/TwiConv/time_and_tweets.json"

    with open(file_path, 'r') as file:
        tweets = json.load(file)

    simulation = TweetsIncomingSim(tweets)
    sentiment_analyzer = SentimentIntensityAnalyzer()
    text = "I love the train! Let me get on it fam! Woohoo!"
    print(get_sentiment(sentiment_analyzer, text=text))