import eventlet
# Monkey patch first, because that's just the magical way it works
eventlet.monkey_patch()
from flask import Flask, request, session
from flask_migrate import Migrate
from flask_socketio import SocketIO
from database import db
from dotenv import dotenv_values
import os


# Load .env data
config = dotenv_values()

# Get directory for migrations
MIGRATION_DIR = os.path.join('models', 'migrations')

# Create flask app and configure it.
app = Flask(__name__)
app.config.update({'DEBUG': config['DEBUG'],
                   'SECRET_KEY': config['SECRET_KEY'],
                   'SQLALCHEMY_DATABASE_URI': config['SQLALCHEMY_DATABASE_URI'],
                   'LISTENING': False
                   })
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.app_context().push()
migrate = Migrate(app, db, directory=MIGRATION_DIR)

# Another import statement, because Flask wants it that way.
from Utility_Tools.store_user_message import store_message

# Boot up socketIO
sio = SocketIO(app, message_queue='redis://', cors_allowed_origins="*")


@app.route('/sms', methods=['POST'])
def sms():
    """
    Function for handling incoming POST requests from the /sms Route to the Flask app.
    :return: str with no data so that it doesn't produce a direct response
    """
    if app.config.get_namespace('LISTENING'):
        full_number = request.form['From']
        message_body = request.form['Body']
        message_data = {"username": full_number, "text": message_body, "sms": True}
        sio.emit('handle_message', message_data)
        store_message(message_data, app, config, db)
    return ""


@app.route('/discord', methods=['POST'])
def discord():
    """
    Function for handling incoming POST requests from the /discord Route to the Flask app.
    :return: str with no data so that it doesn't produce a direct response
    """
    if app.config.get_namespace('LISTENING'):
        message_data = {
            'id': request.form['id'],
            'channel_id': request.form['channel_id'],
            'author_id': request.form['author_id'],
            'username': request.form['username'],
            'guild_id': request.form['guild_id'],
            'guild_name': request.form['guild_name'],
            'text': request.form['text'],
            'discord': True
        }
        sio.emit('handle_message', message_data)
        store_message(message_data, app, config, db)
    return ""


@app.route('/twitter', methods=['POST'])
def twitter():
    """
    Function for handling incoming POST requests from the /discord Route to the Flask app.
    :return: str with no data so that it doesn't produce a direct response
    """
    if app.config.get_namespace('LISTENING'):
        message_data = {
            'username': request.form['username'],
            'text': request.form['text'],
            'tweet': True,
            "twitter_user_id": request.form['twitter_user_id'],
            "tweet_id": request.form['tweet_id']
        }
        sio.emit('handle_message', message_data)
        store_message(message_data, app, config, db)


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
    When movement has connected, allows POST routes and twitter stream to send data to REDIS.
    :return: None
    """
    print('Clients Connected')
    sio.emit('client_connected', "you connected")
    sio.emit('client_connected', "the search term is {}".format(config["SEARCH_TERM"]))
    app.config.update('LISTENING', True)


@sio.on('disconnect')
def disconnect():
    """
    When movement has disconnected, ends POST and twitter stream permission to send messages to REDIS
    :return: None
    """
    print('Clients Diconnected')
    app.config.update('LISTENING', False)


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


sio.run(app, port=8000)







