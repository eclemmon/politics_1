import eventlet
# Monkey patch first, because that's just the magical way it works
eventlet.monkey_patch()
from flask import Flask, json, request
from flask_migrate import Migrate
from flask_socketio import SocketIO
from database import db
from dotenv import dotenv_values
import tweepy
import json
import os
import datetime

# Load .env data
config = dotenv_values()

# Get directory for migrations
MIGRATION_DIR = os.path.join('models', 'migrations')

# Create flask app and configure it.
app = Flask(__name__)
app.config.update({'DEBUG': config['DEBUG'],
                   'SECRET_KEY': config['SECRET_KEY'],
                   'SQLALCHEMY_DATABASE_URI': config['SQLALCHEMY_DATABASE_URI']})
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.app_context().push()
migrate = Migrate(app, db, directory=MIGRATION_DIR)

# Another import statement, but that's just how the magic of flash works.
from Models.user import User
from Models.message import Message

# Boot up socketIO
sio = SocketIO(app, message_queue='redis://', cors_allowed_origins="*")


class MyStream(tweepy.Stream):
    """
    MyStream class to add some extra functionality to the tweepy stream so that it can communicate with the external
    redis server that functions as a thread-safe queue.
    """
    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_secret: str):
        """
        Initialization for MyStream class.
        :param consumer_key: str
        :param consumer_secret: str
        :param access_token: str
        :param access_secret: str
        """
        super(MyStream, self).__init__(consumer_key, consumer_secret, access_token, access_secret)
        self.stream_sio = SocketIO(message_queue='redis://')

    def on_data(self, data):
        """
        When stream gets data, loads the data and stores it in a dict with the same formatting as sms messages.
        Stores the message and emits it to the socketio client that is waiting with the music data generator
        :param data: json
        :return: None
        """
        json_data = json.loads(data)
        message_data = {'username': json_data['user']['screen_name'],
                        'text': json_data['text'].replace('@InteractiveMus4', '').replace('\n', ' ').strip(),
                        'tweet': True, "twitter_user_id": json_data['user']['id'], "tweet_id": json_data['id']}
        store_message(message_data)
        self.stream_sio.emit('handle_message', message_data)

    def on_closed(self, response):
        """
        Prints a message when the stream was closed by twitter for debugging purposes
        :param response: str
        :return: None
        """
        msg = "Twitter closed the stream, this was the response: {}".format(response)
        print(msg)

    def on_request_error(self, status_code):
        """
        Prints a message when the stream got a request error from twitter
        :param status_code: str
        :return: None
        """
        msg = "There was a request error in the tweepy stream: {}".format(status_code)
        print(msg)


@app.route('/sms', methods=['POST'])
def sms():
    """
    Function for handling incoming POST requests from the flask app.
    :return: str with no data so that it doesn't produce a response
    """
    full_number = request.form['From']
    message_body = request.form['Body']
    message_data = {"username": full_number, "text": message_body, "sms": True}
    sio.emit('handle_message', message_data)
    store_message(message_data)
    return ""


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """
    When received a POST message to /shutdown, shuts down the server
    :return: None
    """
    shutdown_server()
    return "Server shutting down..."


@sio.on('connect')
def connect():
    """
    When movement has connected, boots up a twitter stream and starts accepting data from there.
    :return: None
    """
    print('connected')
    sio.emit('client_connected', "you connected")
    stream = MyStream(config['TWITTER_CONSUMER_KEY'], config['TWITTER_CONSUMER_SECRET'],
                      config['TWITTER_ACCESS_TOKEN'], config['TWITTER_ACCESS_SECRET'])
    stream.filter(track=[config["SEARCH_TERM"]], threaded=True)
    sio.emit('client_connected', "the search term is {}".format(config["SEARCH_TERM"]))


@sio.on('disconnect')
def disconnect():
    """
    Print message for when the sio client disconnects
    :return:
    """
    print('Client Diconnected')


def shutdown_server():
    """
    Function to shutdown the Flask server, so that the server doesn't keep running (but why?). Still trying to
    figure out safe shutdown on servers that aren't meant to be shut down...
    :return: None
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Server is not running with the Werkzeug Server or not running.")
    func()


def store_message(message_data):
    """
    Function to store data to the PostgresDB. Returns True of False depending on whether the operation was sucessful.
    :param message_data: dict
    :return: bool
    """
    with app.app_context():
        try:
            user = get_or_make_user(message_data)
            msg = Message(text=message_data['text'],
                          date=datetime.datetime.now().isoformat(),
                          user_id=user.id,
                          movement=config["MOVEMENT"],
                          scored=scored(config))
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
    """
    Function to create a user on the database
    :param message_data: dict
    :return: User on success || None on failure
    """
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


def scored(config):
    """
    A helper function to get settings from the config file, since settings come in as strings
    :param config: dict
    :return: bool
    """
    if config["SCORED"] == "true":
        return True
    else:
        return False


if __name__ == '__main__':
    sio.run(app, port=8000)
