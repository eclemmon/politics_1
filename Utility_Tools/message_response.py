import tweepy
import json
from twilio.rest import Client
from dotenv import dotenv_values


class PoliticsMessageResponder:
    def __init__(self, twilio_account_sid, twilio_auth_token, from_number, tweepy_auth):
        """
        Constructs the politics message responder that will be used to send messages back to users.
        :param account_sid: Twilio account session ID
        :param auth_token: Twilio authentication token
        :param from_number: Phone number to send messages from (if, for example the phone number owned changes)
        """
        self.client = Client(twilio_account_sid, twilio_auth_token)
        self.tweepy_api = tweepy.API(tweepy_auth)
        self.from_number = from_number

    def send_sms(self, message, to_number):
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

    def send_twitter_direct_message(self, message, tweet_id):
        """
        Sents a tweet message as a reply to the tweet_id
        :param message: String message to be tweeted.
        :param twitter_user_id: Integer of user id to be responded to
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


def generate_discourse_message_response(message_responder: PoliticsMessageResponder, data, kwargs):
    if data.get('sms'):
        message_responder.send_sms(generate_sms_discourse_message(data, kwargs), data['username'])
    elif data.get('tweet'):
        message_responder.send_twitter_direct_message(generate_tweet_discourse_message(data, kwargs),
                                                      data['tweet_id'])
    else:
        return None


def generate_tweet_discourse_message(data, kwargs):
    return "Hi {}, I processed your msg and this is some of what happened:\n8va: {}\nMusLen: {} s\n{}\n{}".format(
        "@" + data['username'],
        kwargs['od'],
        kwargs['time_interval'],
        construct_spatialization_response_tweet(kwargs['spat']),
        construct_rhythm_response_tweet(kwargs['rhythm'])
    )


def generate_sms_discourse_message(data, kwargs):
    return "{}{}{}{}{}{}{}".format(
        construct_prefix_response_message(data['username']),
        construct_octave_response_message(kwargs['od']),
        construct_time_interval_response_message(kwargs['time_interval']),
        construct_rhythm_response_message(kwargs['rhythm']),
        construct_delay_response_message(kwargs['delay_t_a_d']),
        construct_spatialization_response_message(kwargs['spat']),
        construct_emojis_response_message(kwargs['pmod'])
    )


def construct_time_interval_response_message(time_interval):
    return '# The musical gesture will last this long (outside of reverb and delay): {} seconds\n\n'.format(time_interval)


def construct_rhythm_response_message(rhythm):
    count = 0
    for i in rhythm:
        if i > 0:
            count += 1
    return "# You triggered {} notes during the musical gesture by using {} discrete parts of speech.\n\n".format(
        count, count)


def construct_rhythm_response_tweet(rhythm):
    count = 0
    for i in rhythm:
        if i > 0:
            count += 1
    return "Num Notes: {}".format(count)

def construct_delay_response_message(delay_t_a_d):
    return "# You submitted {} noun(s) and {} verb(s) to control the delay time and feedback amount\n\n".format(delay_t_a_d[0],
                                                                                                        delay_t_a_d[1])


def construct_spatialization_response_message(spat):
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
    if pmod[0] == 0:
        return "# I don't think you submitted any emojis, so I didn't apply any special sauce to the synth...\n\n"
    else:
        return '# You submitted emojis, and their average sentiment was: {}\nI applied some special sauce ' \
               'to the synth based on your cute emojis!\n\n '.format(pmod[1])


def construct_octave_response_message(od):
    if od >= 6:
        return "# Your message was relatively short, so it will be relatively high and short.\n\n"
    elif 3 <= od <= 5:
        return "# Your message was medium in length, so it will be in the middle of our hearing range.\n\n"
    else:
        return "# Your message was long, so it will be low and long!\n\n"


def construct_prefix_response_message(username):
    return "Thanks so much for your message {}! I processed it and here is some information about how it will affect " \
           "the music it generated:\n\n".format(username)


if __name__ == "__main__":

    config = dotenv_values()

    TWITTER_PATH = '/Users/ericlemmon/Documents/PhD/PhD_Project_v2/twitter_credentials.json'
    with open(TWITTER_PATH, "r") as file:
        credentials = json.load(file)

    twitter_auth = tweepy.OAuth1UserHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'], credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
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
    responder.send_twitter_direct_message(message, 1498422393735458816)
