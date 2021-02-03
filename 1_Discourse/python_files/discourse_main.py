import tweepy
import json
from Utility_Tools.politics_logger import logger_launcher
from pythonosc import udp_client
from discourse_stream_listener import DiscourseStreamListener
from discourse_music_gen import DiscourseMusicGen

class MyStream:
    def __init__(self, auth, logger_object, music_gen):
        self.auth = auth
        self.logger_object = logger_object
        self.music_gen = music_gen

    def message_handler(self, message):
        """
        Just a simple message handler that prints message to the post window and logs it
        in the event log.
        :param message: Message to be posted and logged.
        """
        print(message)
        self.logger_object.info(message)

    def logging_handler(self, message):
        """
        Simple logger handler for logging info that I don't want posted to the stream.
        :param message: Message to be logged.
        :return:
        """
        self.logger_object.info(message)

    def run(self):
        """
        Initializes the main loop for the whole program.
        """
        try:
            self.logging_handler('Testing logger...')
            self.logging_handler("Launching Twitter Listener")
            api = tweepy.API(self.auth)
            self.logging_handler("Launching Passer")
            client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
            self.logging_handler("testing passer")
            client.send_message("/filter", ["Testing OSC Message"])
            self.logging_handler("Information passed, check SuperCollider to see if arrived")
            self.logging_handler('Trying to listen')
            self.stream_listener = DiscourseStreamListener(client, self.logger_object, self.music_gen)
            self.stream = tweepy.Stream(auth=api.auth, listener=self.stream_listener)
            self.stream.filter(follow=["1191395193615990785"])
            # self.stream.filter(track=["Swiss"])
            self.logging_handler('Boot complete\n\n')
        except Exception:
            self.logger_object.exception("There Was a Problem in the Main Loop\n")

    def disconnect(self):
        """
        Disconnects the stream on call.
        :return:
        """
        self.stream_listener.on_data("closing")
        self.stream.disconnect()


if __name__ == '__main__':
    PATH = '/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/twitter_credentials.json'
    with open(PATH, "r") as file:
        credentials = json.load(file)

    auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
    auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])

    logger = logger_launcher()
    music_gen = DiscourseMusicGen(logger_object=logger)
    tweet_stream = MyStream(auth, logger, music_gen)
    tweet_stream.run()
