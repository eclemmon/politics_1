import tweepy, json, logging, politics_logger
from pythonosc import osc_message_builder
from pythonosc import udp_client

with open("twitter_credentials.json", "r") as file:
    credentials = json.load(file)

auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])


def logger_launcher():
    """
    This function launches the logger so any/all data is printed to the log file during the course of a concert.
    :return: Returns the logger object.
    """
    print("Launching Logger")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    filehandler = politics_logger.setuplogger(politics_logger.FILE_PATH)
    formatter = logging.Formatter('OUTPUT %(asctime)s: %(message)s')
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    return logger


class StreamListener(tweepy.StreamListener):
    """
    This class is the main stream listener for twitter. It subclasses from tweepy's stream listener
    to handle data specific to the purposes of Politics.
    """
    def __init__(self, osc_client):
        """
        Initializes class. Must take in a osc client that can send messages to SuperCollider's
        server. Other data initialized are data elements that we want to scrape from twitter
        that arrive in a json format, which is easy to convert to a dictionary.
        :param osc_client: The osc client object.
        """
        self.osc_client = osc_client
        self.keys_to_query = ['created_at', 'text', 'in_reply_to_status_id', 'in_reply_to_status_id_str',
                              'in_reply_to_screen_name', 'geo', 'coordinates',
                              'place', 'is_quote_status', 'quote_count', 'reply_count',
                              'retweet_count', 'favorite_count', 'favorited',
                              'retweeted', 'lang', 'timestamp_ms']
        self.user_keys_to_query = ['name', 'screen_name', 'location', 'url', 'description',
                                   'created_at', ]
        self.entities_keys_to_query = ['hashtags', 'urls', 'user_mentions', 'symbols']

    def on_connect(self):
        """
        Posts a message to message handler.
        """
        msg = "Successfully connected to streaming server."
        message_handler(msg, logger_object)

    def on_status(self, status):
        """
        Primarily will not be using this in favor of on_data. But will log a status
        and send it to OSC when received. May be deprecated in the future.
        :param status: a tweet status
        """
        self.osc_client.send_message("/filter", [status.text])
        message_handler(status.text, logger_object)

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
            message_handler(full_message, logger_object)
        except Exception:
            logger_object.exception("Something went wrong while trying to collect data!\n")


    def on_error(self, status_code):
        """
        If twitter returns an error code, this will post it to log
        and potentially, safely exit the program.
        :param status_code: Status code received from Twitter API
        :return: returns False if status_code = 420
        """
        print(status_code)
        message_handler(status_code, logger_object)
        if status_code == 420:
            return False


def message_handler(message, logger_object):
    """
    This function takes in any data and prints it to console and to the log file.
    Will be deprecated in the future.
    :param message: Message is the formatted text that is to be printed and logged.
    :param logger_object: Logger object is the logger that prints formatted text to file.
    """
    print(message)
    logger_object.info(message)


def main(logger_object):
    """
    This is the main loop.
    :param logger_object: needs the logger object passed to it so it knows what to use.
    """
    try:
        message_handler('Testing logger...', logger_object)
        message_handler("Launching Twitter Listener", logger_object)
        api = tweepy.API(auth)
        message_handler("Launching Passer", logger_object)
        client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
        message_handler("testing passer", logger_object)
        client.send_message("/filter", ["Testing OSC Message"])
        message_handler("Information passed, check SuperCollider to see if arrived", logger_object)
        message_handler('Trying to listen', logger_object)
        stream_listener = StreamListener(client)
        stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        stream.filter(follow=["1191395193615990785"])
        message_handler('Boot complete\n\n', logger_object)
    except Exception:
        logger_object.exception("There Was a Problem in the Main Loop\n")


if __name__ == '__main__':
    logger_object = logger_launcher()
    main(logger_object)
