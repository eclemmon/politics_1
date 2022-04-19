from logging import Logger

from nltk.sentiment.vader import SentimentIntensityAnalyzer

import Utility_Tools.politics_logger
from NLP_Tools.sentiment_analysis_tools import get_average_sentiment
from pythonosc import udp_client
from pythonosc import osc_message_builder


class TechnoAutocracyMusicGen:
    def __init__(self, logger_object: Logger, sentiment_analyzer=SentimentIntensityAnalyzer(), total_time: int = 120):
        """
        Initializes TechnoAutocracyMusicGen
        :param logger_object: Logger
        :param sentiment_analyzer: SentimentIntensityAnalyzer
        :param total_time: int
        """
        # Set passed in objects
        self.logger_object = logger_object
        self.sentiment_analyzer = sentiment_analyzer
        self.total_time = total_time

        # Boot UDP Clients for SC and GUI
        self.sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
        self.gui_client = udp_client.SimpleUDPClient("127.0.0.1", 12000)

        # Set OSC addresses
        self.attack_address = "/attack"
        self.support_address = "/support"

    def attack(self, data: dict, sentiment: dict):
        """
        Function that reads the data and sentiment value generated and sends the data to the GUI and SuperCollider on
        the attack osc address.
        :param data: dict {String: String}
        :param sentiment: dict of sentiment values {String: float}
        :return: None
        """
        self.send_gui_msg(data, sentiment, self.attack_address)
        self.send_sc_msg(sentiment, self.attack_address)

    def support(self, data: dict, sentiment: dict):
        """
        Function that reads the data and sentiment value generated and sends the data to GUI and SuperCollider on the
        support address.
        :param data: dict {String: String}
        :param sentiment: dict of sentiment values {String: float}
        :return: None
        """
        self.send_gui_msg(data, sentiment, self.support_address)
        self.send_sc_msg(sentiment, self.support_address)

    def get_sentiment(self, message: str):
        """
        Gets the average sentiment of a series of sentences or one sentence input as a text.
        :param message: String
        :return: dict of sentiment values {String: float}
        """
        return get_average_sentiment(self.sentiment_analyzer, message)

    def on_data(self, data: str):
        """
        On receiving data, will get the compound value of the sentiment data and determine whether to attack or
        support the technoautocracy.
        :param data: str
        :return: None
        """
        sentiment = self.get_sentiment(data['text'])['compound']
        if sentiment < 0:
            self.attack(data, sentiment)
        else:
            self.support(data, sentiment)

    def send_gui_msg(self, data: dict, sentiment: float, address: str):
        """
        Helper function to send message, user, and sentiment data over to the GUI.
        :param data: dict {str: str}
        :param sentiment: float
        :param address: str
        :return: None
        """
        gui_msg = osc_message_builder.OscMessageBuilder(address=address)
        gui_msg.add_arg(data['username'], arg_type='s')
        gui_msg.add_arg(sentiment, arg_type='f')
        gui_msg = gui_msg.build()
        self.gui_client.send(gui_msg)

    def send_sc_msg(self, sentiment: float, address: str):
        """
        Helper function to send sentiment data over to SuperCollider.
        :param sentiment: float
        :param address: str
        :return: None
        """
        sc_msg = osc_message_builder.OscMessageBuilder(address=address)
        sc_msg.add_arg(sentiment, arg_type='f')
        sc_msg = sc_msg.build()
        self.sc_client.send(sc_msg)


if __name__ == "__main__":
    logger = Utility_Tools.politics_logger.logger_launcher()
    mg = TechnoAutocracyMusicGen(logger)
    mg.on_data({'username': "bogo", "text": "I REALLY HATE this!!!!!!!"})
    # mg.on_data({'username': "bogo", "text": "I Love this!!!!!!!"})
