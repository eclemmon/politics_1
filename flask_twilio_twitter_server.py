import eventlet

eventlet.monkey_patch()
from flask import Flask, json, request
from flask_migrate import Migrate
from twilio.twiml.messaging_response import MessagingResponse
from flask_socketio import SocketIO
from database import db
import tweepy
import json
import os
import datetime

TWITTER_PATH = 'twitter_credentials.json'
with open(TWITTER_PATH, "r") as file:
    credentials = json.load(file)

CONFIG_PATH = 'config.json'
with open(CONFIG_PATH, "r") as file:
    config = json.load(file)

SETTINGS_PATH = 'settings.json'
with open(SETTINGS_PATH, "r") as file:
    settings = json.load(file)

MIGRATION_DIR = os.path.join('models', 'migrations')

app = Flask(__name__)
app.config.update(config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.app_context().push()
migrate = Migrate(app, db, directory=MIGRATION_DIR)

from Models.user import User
from Models.message import Message

sio = SocketIO(app, message_queue='redis://', cors_allowed_origins="*")

class MyStream(tweepy.Stream):
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        super(MyStream, self).__init__(consumer_key, consumer_secret, access_token, access_secret)
        self.stream_sio = SocketIO(message_queue='redis://')

    def on_status(self, status):
        print('status')

    def on_data(self, data):
        json_data = json.loads(data)
        message_data = {'username': json_data['user']['screen_name'],
                        'text': json_data['text'].replace('@InteractiveMus4', '').replace('\n', ' ').strip()}
        store_message(message_data)
        self.stream_sio.emit('handle_message', message_data)


@app.route('/sms', methods=['POST'])
def sms():
    full_number = request.form['From']
    music_number = "XXX-XXX-" + request.form['From'][-4:]
    # print(music_number)
    message_body = request.form['Body']
    music_data = {"username": music_number, "text": message_body}
    message_data = {"username": full_number, "text": message_body}
    resp = MessagingResponse()
    resp.message('Thanks for your message {}, I am processing your message. You said: {}'.format(full_number, message_body))
    sio.emit('handle_message', music_data)
    handle_message(message_data)
    return str(resp)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return "Server shutting down..."


@app.route('/tweet', methods=['POST'])
def handle_message(message_data):
    store_message(message_data=message_data)
    # sio.emit('handle_message', message)


@sio.on('connect')
def connect():
    print('connected')
    sio.emit('client_connected', "you connected")
    stream = MyStream(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'],
                      credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
    stream.filter(track=[settings["SEARCH_TERM"]], threaded=True)
    sio.emit('client_connected', "the search term is {}".format(settings["SEARCH_TERM"]))


@sio.on('disconnect')
def disconnect():
    print('Client Diconnected')


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Server is not running with the Werkzeug Server or not running.")
    func()


def store_message(message_data):
    with app.app_context():
        try:
            user = get_or_make_user(message_data)
            msg = Message(text=message_data['text'],
                          date=datetime.datetime.now().isoformat(),
                          user_id=user.id,
                          movement=settings["MOVEMENT"],
                          scored=scored(settings))
            db.session.add(msg)
            db.session.commit()
            res = True
        except Exception as e:
            print("There was an exception!")
            print(e)
            db.session.rollback()
            res = False
        finally:
            db.session.close()
            return res


def get_or_make_user(message_data):
    with app.app_context():
        if db.session.query(User.id).filter_by(username=message_data['username']).first() is not None:
            return db.session.query(User).filter(User.username == message_data['username']).first()
        else:
            user = User(username=message_data['username'])
            try:
                db.session.add(user)
                db.session.commit()
                return user
            except:
                print("There was an exception in the making of the user!")
                db.session.rollback()
            finally:
                db.session.close()


def scored(settings):
    if settings["SCORED"] == "true":
        return True
    else:
        return False


if __name__ == '__main__':
    sio.run(app, port=8000)
