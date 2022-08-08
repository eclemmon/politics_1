import eventlet

# Monkey patch first, because that's just the magical way it works
eventlet.monkey_patch()
from flask import Flask, request
from flask_migrate import Migrate
from flask_socketio import SocketIO
from database import db
from dotenv import dotenv_values
from Classes.twitter_stream import TwitterStream
from Classes.discord_client import DiscordClient
import os

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

# Another import statement, but that's just how the magic of flask works.
from Utility_Tools.store_user_message import store_message

# Boot up socketIO
sio = SocketIO(app, message_queue='redis://', cors_allowed_origins="*")


class StreamRunner:
    def __init__(self, *streams):
        self.streams = streams

    def send_data_on(self):
        for stream in self.streams:
            stream.send_data_on()

    def send_data_off(self):
        for stream in self.streams:
            stream.send_data_off()


def boot_streams(application, configuration, database):
    print("OK RUNNING STREAMS")
    twitter_stream = TwitterStream(configuration['TWITTER_CONSUMER_KEY'], configuration['TWITTER_CONSUMER_SECRET'],
                                   configuration['TWITTER_ACCESS_TOKEN'], configuration['TWITTER_ACCESS_SECRET'],
                                   application, configuration, database)
    twitter_stream.filter(track=[configuration["SEARCH_TERM"]], threaded=True)
    stream_runner = StreamRunner(twitter_stream)
    return stream_runner


streams = boot_streams(app, config, db)


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
    store_message(message_data, app, config, db)
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
    print('Clients Connected')
    sio.emit('client_connected', "you connected")
    streams.send_data_on()
    sio.emit('client_connected', "the search term is {}".format(config["SEARCH_TERM"]))


@sio.on('disconnect')
def disconnect():
    """
    Print message for when the sio client disconnects
    :return:
    """
    print('Clients Diconnected')
    streams.send_data_off()


def shutdown_server():
    """
    Function to shut down the Flask server, so that the server doesn't keep running (but why?). Still trying to
    figure out safe shutdown on servers that aren't meant to be shut down...
    :return: None
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Server is not running with the Werkzeug Server or not running.")
    func()


if __name__ == '__main__':
    sio.run(app, port=8000)
