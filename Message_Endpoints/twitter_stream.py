"""
twitter_stream.py
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2022, Eric Lemmon"
__credits__ = ["Eric Lemmon"]
__version__ = ""
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Production"

import tweepy
import json
import requests
from flask_socketio import SocketIO
import collections
from dotenv import dotenv_values


class TwitterStream(tweepy.Stream):
    """
    TwitterStream class to add some extra functionality to the tweepy stream so that it can communicate with the external
    redis server that functions as a thread-safe queue.
    """

    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_secret: str, post_address):
        """
        Initialization for TwitterStream class.
        :param consumer_key: str
        :param consumer_secret: str
        :param access_token: str
        :param access_secret: str
        """
        super(TwitterStream, self).__init__(consumer_key, consumer_secret, access_token, access_secret)
        self.stream_sio = SocketIO(message_queue='redis://')
        self.post_address = post_address

    def on_data(self, data):
        """
        When stream gets data, loads the data and stores it in a dict with the same formatting as sms messages.
        Stores the message and emits it to the socketio client that is waiting with the music data generator
        :param data: json
        :return: None
        """
        json_data = json.loads(data)
        message_data = {
            'username': json_data['user']['screen_name'],
            'text': json_data['text'].replace('@InteractiveMus4', '').replace('\n', ' ').strip(),
            "twitter_user_id": json_data['user']['id'],
            "tweet_id": json_data['id']
        }
        requests.post(self.post_address, data=message_data)


    def on_closed(self, response):
        """
        Prints a message when the stream was closed by twitter for debugging purposes
        :param response: str
        :return: None
        """
        msg = "Twitter closed the stream, this was the response: {}".format(response)
        print(msg)

    def on_request_error(self, status_code):
        """
        Prints a message when the stream got a request error from twitter
        :param status_code: str
        :return: None
        """
        msg = "There was a request error in the tweepy stream: {}".format(status_code)
        print(msg)


def make_twitter_stream(configuration: collections.OrderedDict, post_address):
    print("OK RUNNING STREAMS")
    # Boot threaded twitter stream
    twitter_stream = TwitterStream(configuration['TWITTER_CONSUMER_KEY'], configuration['TWITTER_CONSUMER_SECRET'],
                                   configuration['TWITTER_ACCESS_TOKEN'], configuration['TWITTER_ACCESS_SECRET'], post_address)
    twitter_stream.filter(track=[configuration["SEARCH_TERM"]])
    return twitter_stream


config = dotenv_values()
post_address = 'http://127.0.0.1:8000/discord'
twitter_stream = make_twitter_stream(config, post_address)
