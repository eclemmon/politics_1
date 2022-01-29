import unittest
from Utility_Tools.politics_logger import logger_launcher
from a1_Discourse.python_files.discourse_music_gen import DiscourseMusicGen
from Data_Dumps.instrument_names import instrument_names
from Synthesis_Generators.instrument_key_generator import InstrumentKeyAndNameGenerator

logger = logger_launcher()
ikang = InstrumentKeyAndNameGenerator(instrument_names, 4)
music_gen = DiscourseMusicGen(logger, ikang)


class TestDiscourseMusicGen(unittest.TestCase):
    def test_send_music_data(self):
        self.assertEqual(music_gen.send_music_data({'username': "gumbo", 'text': "I went to the circus today"}), True)
