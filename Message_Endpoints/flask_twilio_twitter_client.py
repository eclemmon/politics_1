import socketio
from a1_Discourse.python_files.discourse_music_gen import DiscourseMusicGen
from Utility_Tools.politics_logger import logger_launcher

# Initialize client, logger and music generator
client = socketio.Client()
logger = logger_launcher()
music_gen = DiscourseMusicGen(logger)


@client.on('client_connected')
def on_connect(message):
    print(message)


@client.on('handle_message')
def message(data):
    print("got data")
    print(data)
    music_gen.trigger_sounds(data)


client.connect('http://127.0.0.1:5000/')
client.wait()
