import os
from twilio.rest import Client
from dotenv import dotenv_values


class PoliticsMessageResponder:
    def __init__(self, account_sid, auth_token, from_number):
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number

    def send_sms(self, message, to_number):
        self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=to_number
        )

    def generate_discourse_message(self, values):
        return "lorem ipsum factum"

if __name__ == "__main__":
    config = dotenv_values()
    print(config.keys(), config.values())
    account_sid = config['TWILIO_ACCOUNT_SID']
    auth_token = config['TWILIO_AUTH_TOKEN']
    responder = PoliticsMessageResponder(account_sid, auth_token, "+19293343697")
    responder.send_sms("hi eric", "+13058041575")