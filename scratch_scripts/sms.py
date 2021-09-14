import os
import json
from twilio.rest import Client

PATH = '/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/twitter_credentials.json'
with open(PATH, "r") as file:
    credentials = json.load(file)

account_sid = credentials['TWILIO_ACCOUNT_SID']
auth_token = credentials['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages.create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_="+19293343697",
                     to="+4915751361152"
                 )

print(message.sid)