import unittest
import time
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

    def test_schedule_current_chord(self):
        music_gen.harmonic_walk(1, 100, 20, music_gen.web)
        text = """
        My name is eric lemmon and I am ready to rock and roll. But I am also putting out some tweets, you know???????
        BUT IF I MAKE A LONG TWEET< WHAT HAPPENS THEN?
        """
        music_gen.send_music_data({'username': "gumbo", 'text': text})
        print(music_gen.web.output_chord)
