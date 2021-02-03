import tweepy
import json
from Utility_Tools.politics_logger import logger_launcher
from pythonosc import udp_client


class DiscourseStreamListener(tweepy.StreamListener):
    def __init__(self, client, logger_object, music_gen):
        self.client = client
        self.keys_to_query = ['created_at', 'text', 'in_reply_to_status_id', 'in_reply_to_status_id_str',
                              'in_reply_to_screen_name', 'geo', 'coordinates',
                              'place', 'is_quote_status', 'quote_count', 'reply_count',
                              'retweet_count', 'favorite_count', 'favorited',
                              'retweeted', 'lang', 'timestamp_ms']
        self.user_keys_to_query = ['name', 'screen_name', 'location', 'url', 'description',
                                   'created_at', ]
        self.entities_keys_to_query = ['hashtags', 'urls', 'user_mentions', 'symbols']
        self.logger_object = logger_object
        self.music_gen = music_gen

    def on_connect(self):
        """
        Posts a message to message handler.
        """
        msg = "Successfully connected to streaming server."
        self.message_handler(msg)

    def message_handler(self, message):
        """
        Message handler logs information coming in from twitter as well as prints it
        to the post window. It also runs the music_gen's trigger sounds function,
        which is the meat and potatoes of Politics I.
        :param message: tweet from tweet stream.
        """
        print(message)
        self.logger_object.info(message)
        self.music_gen.trigger_sounds(message)

    def logging_handler(self, message):
        """
        Logs information that needs to be logged without posting it to window or
        calling some other function or method.
        :param message: The message to be logged.
        """
        self.logger_object.info(message)

    def on_error(self, status_code):
        """
        If twitter returns an error code, this will post it to log
        and potentially, safely exit the program.
        :param status_code: Status code received from Twitter API
        :return: returns False if status_code = 420
        """
        print(status_code)
        self.logging_handler(status_code)
        if status_code == 420:
            return False

    def on_data(self, raw_data):
        """
        Takes in data in json format from Twitter, and checks for the data fields desired to be
        taken in for processing. Currently only logs and posts the data to console and log file.
        Will call NLP processes on the data in the future and pass the data to SuperCollider.
        :param raw_data: Data as json from Twitter
        """
        try:
            raw_data_as_dict = json.loads(raw_data)
            messageheader = '\n\n##### START OF TWEET DATA #####\n\n'
            message_body_list = []
            for item in self.user_keys_to_query:
                message_body_list.append('{:<25}: {:}\n'.format(item.upper(), raw_data_as_dict['user'][item]))
            for item in self.entities_keys_to_query:
                message_body_list.append('{:<25}: {:}\n'.format(item.upper(), raw_data_as_dict['entities'][item]))
            for key in self.keys_to_query:
                message_body_list.append('{:<25}: {:}\n'.format(key.upper(), raw_data_as_dict[key]))
            message_body = ''.join(message_body_list)
            message_footer = '\n##### END OF TWEET DATA #####\n'
            full_message = messageheader + message_body + message_footer
            self.message_handler(full_message)
        except Exception:
            self.logger_object.exception("Something went wrong while trying to collect data!\n")
