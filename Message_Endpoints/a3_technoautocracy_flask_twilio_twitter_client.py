import socketio
from a3_Techno_Autocracy.python_files.techno_autocracy_music_gen import TechnoAutocracyMusicGen
from Utility_Tools.politics_logger import logger_launcher

# Initialize client, logger and music generator
client = socketio.Client()
logger = logger_launcher()
music_gen = TechnoAutocracyMusicGen(logger)


@client.on('client_connected')
def on_connect(message):
    print(message)


@client.on('handle_message')
def message(data):
    # print(data)
    music_gen.on_data(data)


client.connect('http://127.0.0.1:8000/')
client.wait()
