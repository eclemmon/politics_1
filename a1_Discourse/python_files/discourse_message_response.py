import os
from twilio.rest import Client
from dotenv import dotenv_values


def generate_discourse_message(values):
    return "lorem ipsum factum"


class PoliticsMessageResponder:
    def __init__(self, account_sid, auth_token, from_number):
        """
        Constructs the politics message responder that will be used to send messages back to users.
        :param account_sid: Twilio account session ID
        :param auth_token: Twilio authentication token
        :param from_number: Phone number to send messages from (if, for example the phone number owned changes)
        """
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number

    def send_sms(self, message, to_number):
        """
        Sends an sms message to the to_number
        :param message: String message to be sent
        :param to_number: String formatted "+19999999999"
        :return: None
        """
        self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=to_number
        )


if __name__ == "__main__":
    config = dotenv_values()
    account_sid = config['TWILIO_ACCOUNT_SID']
    auth_token = config['TWILIO_AUTH_TOKEN']
    phone_number = config['TWILIO_PHONE_NUMBER']
    responder = PoliticsMessageResponder(account_sid, auth_token, phone_number)
    responder.send_sms("hi eric", "+13058041575")