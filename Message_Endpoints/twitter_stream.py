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


class TwitterStream(tweepy.StreamingClient):
    """
    TwitterStream class to add some extra functionality to the tweepy stream so that it can communicate with the external
    redis server that functions as a thread-safe queue.
    """

    def __init__(self, bearer_token, post_address):
        """
        Initialization for TwitterStream class.
        :param consumer_key: str
        :param consumer_secret: str
        :param access_token: str
        :param access_secret: str
        """
        super(TwitterStream, self).__init__(bearer_token)
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
            'username': json_data['includes']['users'][0]['username'],
            'text': json_data['data']['text'].replace('@InteractiveMus4', '').replace('\n', ' ').strip(),
            "twitter_user_id": json_data['data']['author_id'],
            "tweet_id": json_data['data']['id']
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
    twitter_stream = TwitterStream(configuration['TWITTER_BEARER_TOKEN'], post_address)

    # clean-up pre-existing rules
    result = twitter_stream.get_rules()
    if result.data is not None:
        rule_ids = [rule.id for rule in result.data]
    else:
        rule_ids = []

    if (len(rule_ids) > 0):
        twitter_stream.delete_rules(rule_ids)
        twitter_stream = TwitterStream(configuration['TWITTER_BEARER_TOKEN'], post_address)
    else:
        print("no rules to delete")

    twitter_stream.add_rules(tweepy.StreamRule(configuration['SEARCH_TERM']))
    twitter_stream.filter(tweet_fields=["referenced_tweets"], expansions=["author_id"], threaded=True)
    return twitter_stream


config = dotenv_values()
post_address = 'http://127.0.0.1:8000/twitter'
twitter_stream = make_twitter_stream(config, post_address)
print("Twitter Stream Running.")
