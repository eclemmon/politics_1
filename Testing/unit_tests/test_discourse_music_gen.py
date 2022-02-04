import unittest
import time
import random
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
        # print(music_gen.web.output_chord)

    def test_send_data_toSC(self):
        texts = [
            "Corn!",
            "My dresser is broken.",
            "I wish I was living in the blue house across the street.",
            "The neighbors in 1225, whom we have only known a few short weeks, are willing to help us—selflessly—with "
            "the cat!",
            "I AM SO HAPPY RIGHT NOW! :) :) :)",
            "I HATE YOU SO MUCH !!!!!!!!!!!!",
            "I ruined my sweater today :(",
            "Corny!",
            "My dresser is really broken.",
            "I wish I was living in the blue house across the street, maybe maybe.",
            "The neighbors in 1225, whom we have only known a few short weeks, are willing to help us—selflessly—with "
            "the cat! We are very appreciative of them",
            "I AM SO HAPPY RIGHT NOW! :) :) :). LIKE COMPLETELY OVERJOYED",
            "I HATE YOU SO MUCH !!!!!!!!!!!! BECAUSE YOUR HURT ME!!!!!!",
            "I ruined my sweater today :( it has bleach on it",
            "Corn!",
            "My dresser is broken.",
            "I wish I was living in the blue house across the street.",
            "The neighbors in 1225, whom we have only known a few short weeks, are willing to help us—selflessly—with "
            "the cat!",
            "I AM SO HAPPY RIGHT NOW! :) :) :)",
            "I HATE YOU SO MUCH !!!!!!!!!!!!",
            "I ruined my sweater today :(",
            "Corny!",
            "My dresser is really broken.",
            "I wish I was living in the blue house across the street, maybe maybe.",
            "The neighbors in 1225, whom we have only known a few short weeks, are willing to help us—selflessly—with "
            "the cat! We are very appreciative of them",
            "I AM SO HAPPY RIGHT NOW! :) :) :). LIKE COMPLETELY OVERJOYED",
            "I HATE YOU SO MUCH !!!!!!!!!!!! BECAUSE YOUR HURT ME!!!!!!",
            "I ruined my sweater today :( it has bleach on it",
        ]
        music_gen.harmonic_walk(1, 100, 20, music_gen.web)
        for text in texts:
            music_gen.send_music_data({'username': "gumbo", 'text': text})
            time.sleep(random.random() * 4)

