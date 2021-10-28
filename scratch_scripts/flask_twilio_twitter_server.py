from flask import Flask, json, request
from twilio.twiml.messaging_response import Message, MessagingResponse
from flask_socketio import SocketIO
import tweepy
import json

PATH = '/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/twitter_credentials.json'
with open(PATH, "r") as file:
    credentials = json.load(file)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'abc123'
sio = SocketIO(app, cors_allowed_origins="*")

auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
api = tweepy.API(auth)


class MyListener(tweepy.StreamListener):
    def on_status(self, status):
        print('status')

    def on_data(self, data):
        handle_message(data)

    def on_error(self, status):
        print('error')
        print(status)


stream_listener = MyListener()


@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    message_data = {"number": number, "msg": message_body}
    resp = MessagingResponse()
    resp.message('Hello {}, you said: {}'.format(number, message_body))
    handle_message(message_data)
    return str(resp)


@sio.on('connect')
def connect():
    print('connected')
    sio.emit('client_connected', "you connected")
    search_term = "#ericlemmon"
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=[search_term], is_async=True)
    sio.emit('client_connected', "the search term is {}".format(search_term))


@sio.on('disconnect')
def disconnect():
    print('Client Diconnected')


@sio.event
def handle_message(message):
    print("1", message)
    sio.emit('handle_message', message)


if __name__ == '__main__':
    sio.run(app)
