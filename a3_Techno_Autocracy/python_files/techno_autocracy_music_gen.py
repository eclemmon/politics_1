from nltk.sentiment.vader import SentimentIntensityAnalyzer

import Utility_Tools.politics_logger
from NLP_Tools.sentiment_analysis_tools import get_average_sentiment
from pythonosc import udp_client
from pythonosc import osc_message_builder


class TechnoAutocracyMusicGen:
    def __init__(self, logger_object, sentiment_analyzer=SentimentIntensityAnalyzer(), total_time=120):
        self.logger_object = logger_object
        self.sentiment_analyzer = sentiment_analyzer
        self.total_time = total_time

        self.sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
        self.gui_client = udp_client.SimpleUDPClient("127.0.0.1", 12000)

        self.attack_address = "/attack"
        self.support_address = "/support"

    def attack(self, data, sentiment):
        self.send_gui_msg(data, sentiment, self.attack_address)
        self.send_sc_msg(sentiment, self.attack_address)

    def support(self, data, sentiment):
        self.send_gui_msg(data, sentiment, self.support_address)
        self.send_sc_msg(sentiment, self.support_address)

    def get_sentiment(self, message):
        return get_average_sentiment(self.sentiment_analyzer, message)

    def on_data(self, data):
        sentiment = self.get_sentiment(data['text'])['compound']
        if sentiment < 0:
            self.attack(data, sentiment)
        else:
            self.support(data, sentiment)

    def send_gui_msg(self, data, sentiment, address):
        gui_msg = osc_message_builder.OscMessageBuilder(address=address)
        gui_msg.add_arg(data['username'], arg_type='s')
        gui_msg.add_arg(sentiment, arg_type='f')
        gui_msg = gui_msg.build()
        self.gui_client.send(gui_msg)

    def send_sc_msg(self, sentiment, address):
        sc_msg = osc_message_builder.OscMessageBuilder(address=address)
        sc_msg.add_arg(sentiment, arg_type='f')
        sc_msg = sc_msg.build()
        self.sc_client.send(sc_msg)


if __name__ == "__main__":
    logger = Utility_Tools.politics_logger.logger_launcher()
    mg = TechnoAutocracyMusicGen(logger)
    mg.on_data({'username': "bogo", "text": "I REALLY HATE this!!!!!!!"})
    # mg.on_data({'username': "bogo", "text": "I Love this!!!!!!!"})
