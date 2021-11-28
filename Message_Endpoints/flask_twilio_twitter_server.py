import eventlet
eventlet.monkey_patch()
from flask import Flask, json, request
from twilio.twiml.messaging_response import Message, MessagingResponse
from flask_socketio import SocketIO
import tweepy
import json


PATH = '/twitter_credentials.json'
with open(PATH, "r") as file:
    credentials = json.load(file)


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'abc123'
sio = SocketIO(app, message_queue='redis://', cors_allowed_origins="*")


class MyStream(tweepy.Stream):
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        super(MyStream, self).__init__(consumer_key, consumer_secret, access_token, access_secret)
        self.stream_sio = SocketIO(message_queue='redis://')

    def on_status(self, status):
        print('status')

    def on_data(self, data):
        json_data = json.loads(data)
        self.stream_sio.emit('handle_message', json_data['text'])
        # TODO: Send along all necessary information


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
    search_term = "#testingecl"
    stream = MyStream(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'],
                           credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
    stream.filter(track=[search_term], threaded=True)
    sio.emit('client_connected', "the search term is {}".format(search_term))


@sio.on('disconnect')
def disconnect():
    print('Client Diconnected')

def handle_message(message):
    sio.emit('handle_message', message)

if __name__ == '__main__':
    sio.run(app)
