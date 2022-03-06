import unittest
import time
import random
from Utility_Tools.politics_logger import logger_launcher
from a1_Discourse.python_files.discourse_music_gen import DiscourseMusicGen
from Data_Dumps.instrument_names import instrument_names_sc
from Data_Dumps.instrument_names import instrument_indices_daw
from Synthesis_Generators.instrument_key_generator import InstrumentKeyAndNameGenerator

logger = logger_launcher()
random.shuffle(instrument_indices_daw)
ikang = InstrumentKeyAndNameGenerator(instrument_indices_daw, 4)
music_gen = DiscourseMusicGen(logger, ikang)

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

texts_short = [
    "Corn!",
    "Corn!",
    "Corn!",
    "Corn!",
    "Corn!",
    "Corn!",
    "ANGRY!!!",
    "ANGRY!!!",
    "ANGRY!!!",
    "ANGRY!!!",
    "ANGRY!!!",
    "ANGRY!!!",
    "ANGRY!!!",
    "HAPPY!!!!",
    "HAPPY!!!!",
    "HAPPY!!!!",
    "HAPPY!!!!",
    "HAPPY!!!!",
]

texts_long = [
    "The neighbors in 1225, whom we have only known a few short weeks, are willing to help us—selflessly—with "
    "the cat!",
    "I had learned a little about writing from Soldiers' Pay--how to approach language, words: not with seriousness "
    "so much, as an essayist does, but with a kind of alert respect, as you approach dynamite; even with joy, "
    "as you approach women: perhaps with the same secretly unscrupulous intentions.",
    "I set out deliberately to write a tour-de-force. Before I ever put pen to paper and set down the first word, "
    "I knew what the last word would be and almost where the last period would fall.",
    "The book was almost finished before I acquiescedto the fact that it would not recur, since I was now aware "
    "before each word was written down just what the people would do, since now I was deliberately choosing among "
    "possibilities and probabilities of behavior and weighing and measuring each choice by the scale of the Jameses "
    "and Conrads and Balzacs",
    "I believed that I knew then why I had not recaptured that first ecstasy, and that I should never again recapture "
    "it; that whatever treenovels I should write in the future would be written without reluctance, but also without "
    "anticipation or joy: that in the Sound and The Fury I had already put perhaps the only thing in literature which "
    "would ever move me very much: Caddy climbing the pear tree to look in the window at her grandmother's funeral "
    "while Quentin and Jason and Benjy and the negroes looked up at the muddy seat of her drawers"
]


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

    def test_send_long_data_toSC(self):
        music_gen.harmonic_walk(1, 100, 20, music_gen.web)
        for text in texts_long:
            music_gen.send_music_data({'username': "Machiavelli", 'text': text})
            time.sleep(10)

    def test_send_short_data_toSC(self):
        music_gen.harmonic_walk(1, 100, 20, music_gen.web)
        for text in texts_short:
            music_gen.send_music_data({'username': "gumbo", 'text': text})
            time.sleep(random.random())

    def test_send_var_data_toSC(self):
        music_gen.harmonic_walk(1, 100, 20, music_gen.web)
        music_gen.send_music_data({'username': "Plato", 'text': "Why hello there!"})
        music_gen.send_gui_data({'username': "Plato", 'text': "Why hello there!"})
        time.sleep(random.random())
        for text in texts:
            music_gen.send_music_data({'username': "gumbo", 'text': text})
            music_gen.send_gui_data({'username': "gumbo", 'text': text})
            time.sleep(random.random() * 5)
