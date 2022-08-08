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
from flask_socketio import SocketIO
from Utility_Tools.store_user_message import store_message


class TwitterStream(tweepy.Stream):
    """
    TwitterStream class to add some extra functionality to the tweepy stream so that it can communicate with the external
    redis server that functions as a thread-safe queue.
    """

    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_secret: str, app, config, db):
        """
        Initialization for TwitterStream class.
        :param consumer_key: str
        :param consumer_secret: str
        :param access_token: str
        :param access_secret: str
        """
        super(TwitterStream, self).__init__(consumer_key, consumer_secret, access_token, access_secret)
        self.stream_sio = SocketIO(message_queue='redis://')
        self.send_data = False
        self.app = app
        self.config = config
        self.db = db

    def on_data(self, data):
        """
        When stream gets data, loads the data and stores it in a dict with the same formatting as sms messages.
        Stores the message and emits it to the socketio client that is waiting with the music data generator
        :param data: json
        :return: None
        """
        if self.send_data:
            json_data = json.loads(data)
            message_data = {'username': json_data['user']['screen_name'],
                            'text': json_data['text'].replace('@InteractiveMus4', '').replace('\n', ' ').strip(),
                            'tweet': True, "twitter_user_id": json_data['user']['id'], "tweet_id": json_data['id']}
            store_message(data, self.app, self.config, self.db)
            self.stream_sio.emit('handle_message', message_data)

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

    def send_data_off(self):
        self.send_data = False
        print(self.send_data_report())

    def send_data_on(self):
        self.send_data = True
        print(self.send_data_report())

    def send_data_report(self):
        return 'Sending data set to: {}'.format(self.send_data)



