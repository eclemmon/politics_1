from nltk.sentiment.vader import SentimentIntensityAnalyzer


class TechnoAutocracyMusicGen:
    def __init__(self, logger_object, sentiment_analyzer=SentimentIntensityAnalyzer(), total_length=120):
        self.logger_object = logger_object
        self.sentiment_analyzer = sentiment_analyzer

    def attack(self, message):
        pass

    def get_sentiment(self, message):
        pass
