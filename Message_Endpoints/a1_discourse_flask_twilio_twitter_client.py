import socketio
import json
from Data_Dumps.instrument_names import instrument_names_sc
from Data_Dumps.instrument_names import instrument_indices_daw
from a1_Discourse.python_files.discourse_music_gen import DiscourseMusicGen
from Synthesis_Generators.instrument_key_generator import InstrumentKeyAndNameGenerator
from Utility_Tools.politics_logger import logger_launcher
from dotenv import dotenv_values

config = dotenv_values()

# Determine instrument names
if config["DAW"] == 'true':
    instruments = instrument_indices_daw
    inst_key_name_gen = InstrumentKeyAndNameGenerator(instruments, 16)
else:
    instruments = instrument_names_sc
    inst_key_name_gen = InstrumentKeyAndNameGenerator(instruments, 4)

# Initialize client, logger and music generator
client = socketio.Client()
logger = logger_launcher()
music_gen = DiscourseMusicGen(logger, inst_key_name_gen)


@client.on('client_connected')
def on_connect(message):
    print(message)


@client.on('handle_message')
def message(data):
    music_gen.trigger_sounds(data)


client.connect('http://127.0.0.1:8000/')
client.wait()
