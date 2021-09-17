from nltk.sentiment.vader import SentimentIntensityAnalyzer
from NLP_Tools.sentiment_analysis_tools import get_average_sentiment


class TechnoAutocracyMusicGen:
    def __init__(self, logger_object, sentiment_analyzer=SentimentIntensityAnalyzer(), total_length=120):
        self.logger_object = logger_object
        self.sentiment_analyzer = sentiment_analyzer

    def attack(self):
        pass

    def support(self):
        pass

    def get_sentiment(self, message):
        return get_average_sentiment(self.sentiment_analyzer, message)

    def trigger(self, message):
        if self.get_sentiment(message)['compound'] < 0:
            self.attack()
        else:
            self.support()


