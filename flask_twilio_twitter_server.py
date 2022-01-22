import eventlet

eventlet.monkey_patch()
from flask import Flask, json, request
from flask_sqlalchemy import SQLAlchemy
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
        message_data = {'username': json_data['user']['screen_name'], 'msg': json_data['text']}
        store_message(message_data)
        self.stream_sio.emit('handle_message', message_data)
        # TODO: Send along all necessary information


@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    message_data = {"username": number, "msg": message_body}
    resp = MessagingResponse()
    resp.message('Hello {}, you said: {}'.format(number, message_body))
    sio.emit('handle_message', message_data)
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
    search_term = "@InteractiveMus4"
    stream = MyStream(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'],
                      credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
    stream.filter(track=[search_term], threaded=True)
    sio.emit('client_connected', "the search term is {}".format(search_term))


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
            msg = Message(text=message_data['msg'], date=datetime.datetime.now().isoformat(), user_id=user.id)
            db.session.add(msg)
            db.session.commit()
            res = True
        except:
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




if __name__ == '__main__':
    sio.run(app)
