import socketio
from a2_Cybernetic_Republic.python_files.cybernetic_republic_music_gen import CyberneticRepublicMusicGen
from Data_Dumps.vote_options import vote_options
from Utility_Tools.politics_logger import logger_launcher

# Initialize client, logger and music generator
client = socketio.Client()
logger = logger_launcher()

music_gen = CyberneticRepublicMusicGen(logger, vote_options, num_cycles=21)


@client.on('client_connected')
def on_connect(message):
    print(message)


@client.on('handle_message')
def message(data):
    print(data)
    music_gen.on_data(data)


music_gen.run()
client.connect('http://127.0.0.1:8000/')
client.wait()
