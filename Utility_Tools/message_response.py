import tweepy
import json
from twilio.rest import Client
from dotenv import dotenv_values


class PoliticsMessageResponder:
    """
    PoliticsMessageResponder for generating texts and sending them via SMS or tweet back to audience members.
    """
    def __init__(self, twilio_account_sid: str, twilio_auth_token: str, from_number: str, tweepy_auth):
        """
        Constructs the politics message responder that will be used to send messages back to users.
        :param twilio_account_sid: str Twilio account session ID
        :param twilio_auth_token: str Twilio authentication token
        :param from_number: str Phone number to send messages from (if, for example the phone number owned changes)
        :param tweepy_auth: tweepy auth handler.
        """
        self.client = Client(twilio_account_sid, twilio_auth_token)
        self.tweepy_api = tweepy.API(tweepy_auth)
        self.from_number = from_number

    def send_sms(self, message: str, to_number: str):
        """
        Sends an sms message to the to_number
        :param message: String message to be sent
        :param to_number: String formatted "+19999999999"
        :return: True
        """
        try:
            self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
        except BaseException as e:
            print("Error send_sms: {}".format(str(e)))
        finally:
            return True

    def send_twitter_reply_message(self, message: str, tweet_id: int):
        """
        Sends a tweet message as a reply to the tweet_id
        :param tweet_id: Integer of user id to be responded to
        :param message: String message to be tweeted.
        :return: True
        """
        print("sending message...")
        try:
            self.tweepy_api.update_status(
                status=message,
                in_reply_to_status_id=tweet_id
            )
        except BaseException as e:
            print("Error send_twitter_direct_message: {}".format(str(e)))
        finally:
            return True


def generate_discourse_message_response(message_responder: PoliticsMessageResponder, data: dict, kwargs: dict):
    """
    Responder function to build and send response messages during the discourse movement.
    :param message_responder:
    :param data: dict
    :param kwargs: dict
    :return: None
    """
    if data.get('sms'):
        message_responder.send_sms(generate_sms_discourse_message(data, kwargs), data['username'])
    elif data.get('tweet'):
        message_responder.send_twitter_reply_message(generate_tweet_discourse_message(data, kwargs),
                                                     data['tweet_id'])
    else:
        return None


def generate_tweet_discourse_message(data: dict, kwargs: dict):
    """
    String constructor for generating tweet responses during the discourse movement
    :param data: dict
    :param kwargs: dict
    :return: str
    """
    return "Hi {}, I processed your msg and this is some of what happened:\n8va: {}\nMusLen: {} s\n{}\n{}".format(
        "@" + data['username'],
        kwargs['od'],
        kwargs['time_interval'],
        construct_spatialization_response_tweet(kwargs['spat']),
        construct_rhythm_response_tweet(kwargs['rhythm'])
    )


def generate_sms_discourse_message(data: dict, kwargs: dict):
    """
    String constructor for generating sms responses during the discourse movement
    :param data: dict
    :param kwargs: dict
    :return: str
    """
    return "{}{}{}{}{}{}{}".format(
        construct_prefix_response_message(data['username']),
        construct_octave_response_message(kwargs['od']),
        construct_time_interval_response_message(kwargs['time_interval']),
        construct_rhythm_response_message(kwargs['rhythm']),
        construct_delay_response_message(kwargs['delay_t_a_d']),
        construct_spatialization_response_message(kwargs['spat']),
        construct_emojis_response_message(kwargs['pmod'])
    )


def generate_cybernetic_republic_message_response(message_responder: PoliticsMessageResponder, data: dict,
                                                  kwargs: dict):
    """
    Responder function to build and send responses during the cybernetic republic movement
    :param message_responder: PoliticsMessageResponder
    :param data: dict
    :param kwargs: dict
    :return: str
    """
    if data.get('sms'):
        message_responder.send_sms(generate_cybernetic_republic_message(data, kwargs), data['username'])
    elif data.get('tweet'):
        message_responder.send_twitter_reply_message(generate_cybernetic_republic_message(data, kwargs),
                                                     data['tweet_id'])
    else:
        return None


def generate_cybernetic_republic_message(data: dict, kwargs: dict):
    """
    String constructor function for building responses during the cybernetic republic message.
    :param data: dict
    :param kwargs: dict
    :return: str
    """
    if not kwargs['voting-period']:
        return "Hi {}, voting is currently closed. Please wait until voting opens!".format(data['username'])
    if kwargs['no-option-selected']:
        return "Hi {}, you said: {}... I tried finding one of the vote options, but couldn't. Remember, you have to " \
               "write the vote exactly as it appears for me to tally it. Try again?".format(
                data['username'], data['text'][:20]
                )
    if kwargs['already-voted']:
        return "Hi {}, it seems like you already voted in this section. You may only vote once!".format(
            data['username'])
    else:
        if kwargs['introduction'] and kwargs['first-option'].lower() not in kwargs['vote-text'].lower():
            return "I suggested you vote for the first option during the tutorial, but that's OK! " \
                   "I still parsed your message and added the first vote option I found to the tally." \
                   " These are the updated results: \n {}".format(kwargs['vote'])
        else:
            return "Hi {}, I parsed your message, and added the first vote option I found to the " \
                   "tally! These are the updated results: \n{}".format(data['username'], kwargs['vote'])


def construct_time_interval_response_message(time_interval: float):
    """
    Helper function to build a string describing how a user message affected time_interval data
    :param time_interval: float
    :return: str
    """
    return '# The musical gesture will last this long (outside of reverb and delay): {} seconds\n\n'.format(
        time_interval)


def construct_rhythm_response_message(rhythm: list):
    """
    Helper function to build a string describing how a user message affected rhythm data for sms.
    :param rhythm: list
    :return: str
    """
    count = 0
    for i in rhythm:
        if i > 0:
            count += 1
    return "# You triggered {} notes during the musical gesture by using {} discrete parts of speech.\n\n".format(
        count, count)


def construct_rhythm_response_tweet(rhythm: list):
    """
    Helper function to build a string describing how a user message affected rhythm data for tweet.
    :param rhythm: list
    :return: str
    """
    count = 0
    for i in rhythm:
        if i > 0:
            count += 1
    return "Num Notes: {}".format(count)


def construct_delay_response_message(delay_t_a_d: tuple):
    """
    Helper function to build a string describing how a user message affected delay data
    :param delay_t_a_d: tuple of floats
    :return: str
    """
    return "# You submitted {} noun(s) and {} verb(s) to control the delay time and feedback amount\n\n".format(
        delay_t_a_d[0],
        delay_t_a_d[1])


def construct_spatialization_response_message(spat):
    """
    Helper function to build a string describing how a user message affected spatialization data for sms.
    :param spat: tuple of floats.
    :return: str
    """
    if spat[1] > 0:
        if spat[2] == 0:
            return "# Your musical gesture will move from: [ROH] {} --> [C] {}\n\n".format(spat[1], spat[2])
        else:
            return "# Your musical gesture will move from: [ROH] {} --> [LOH] {}\n\n".format(spat[1], spat[2])
    elif spat[1] == 0:
        if spat[2] < 0:
            return "# Your musical gesture will move from: [C] {} --> [LOH] {}\n\n".format(spat[1], spat[2])
        else:
            return "# Your musical gesture will move from: [C] {} --> [ROH] {}\n\n".format(spat[1], spat[2])
    else:
        if spat[2] == 0:
            return "# Your musical gesture will move from: [LOH] {} --> [C] {}\n\n".format(spat[1], spat[2])
        else:
            return "# Your musical gesture will move from: [LOH] {} --> [ROH] {}\n\n".format(spat[1], spat[2])


def construct_spatialization_response_tweet(spat):
    """
    Helper function to build a string describing how a user message affected spatialization data for tweets.
    :param spat: tuple of floats.
    :return: str
    """
    if spat[1] > 0:
        if spat[2] == 0:
            return "Spat: [ROH] {} --> [C] {}".format(spat[1], spat[2])
        else:
            return "Spat: [ROH] {} --> [LOH] {}".format(spat[1], spat[2])
    elif spat[1] == 0:
        if spat[2] < 0:
            return "Spat: [C] {} --> [LOH] {}".format(spat[1], spat[2])
        else:
            return "Spat: [C] {} --> [ROH] {}".format(spat[1], spat[2])
    else:
        if spat[2] == 0:
            return "Spat: [LOH] {} --> [C] {}".format(spat[1], spat[2])
        else:
            return "Spat: [LOH] {} --> [ROH] {}".format(spat[1], spat[2])


def construct_emojis_response_message(pmod):
    """
    Helper function to build a string describing how a user message affected phase modulation.
    :param pmod: float
    :return: str
    """
    if pmod[0] == 0:
        return "# I don't think you submitted any emojis, so I didn't apply any special sauce to the synth...\n\n"
    else:
        return '# You submitted emojis, and their average sentiment was: {}\nI applied some special sauce ' \
               'to the synth based on your cute emojis!\n\n '.format(pmod[1])


def construct_octave_response_message(od):
    """
    Helper function to build a string describing how a user message affected the octave placement of the musical
    gesture.
    :param od: int
    :return: str
    """
    if od >= 6:
        return "# Your message was relatively short, so it will be relatively high and short.\n\n"
    elif 3 <= od <= 5:
        return "# Your message was medium in length, so it will be in the middle of our hearing range.\n\n"
    else:
        return "# Your message was long, so it will be low and long!\n\n"


def construct_prefix_response_message(username):
    """
    Helper function to build the prefix with context.
    :param username: str
    :return: str
    """
    return "Thanks so much for your message {}! I processed it and here is some information about how it will affect " \
           "the music it generated:\n\n".format(username)


if __name__ == "__main__":
    config = dotenv_values()

    TWITTER_PATH = '/Users/ericlemmon/Documents/PhD/PhD_Project_v2/twitter_credentials.json'
    with open(TWITTER_PATH, "r") as file:
        credentials = json.load(file)

    twitter_auth = tweepy.OAuth1UserHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'],
                                            credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
    # twitter_auth.set_access_token()

    data = {'username': "+13058041575"}
    tweet_data = {'username': "EricCLemmon"}
    kwargs = {'od': 8, 'time_interval': 3.234,
              'rhythm': [1, -1.5, 1, -1.5, -1.5], 'delay_t_a_d': (0.23, 0.4),
              'spat': (3.234, 1, -1), 'pmod': (3342, 8)}
    account_sid = config['TWILIO_ACCOUNT_SID']
    auth_token = config['TWILIO_AUTH_TOKEN']
    phone_number = config['TWILIO_PHONE_NUMBER']
    responder = PoliticsMessageResponder(account_sid, auth_token, phone_number, twitter_auth)
    message = generate_sms_discourse_message(data, kwargs)
    message = generate_tweet_discourse_message(tweet_data, kwargs)
    # responder.send_sms(message, "+13058041575")
    responder.send_twitter_reply_message(message, 1498422393735458816)
