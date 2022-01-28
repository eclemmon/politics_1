import unittest
from Synthesis_Generators.delay_values_generator import delay_time_and_decay
from NLP_Tools.part_of_speech_tools import build_pos_count_dict

text = "I love the train! Let me get on it fam! Woohoo!"
pos_count_dict = build_pos_count_dict(text)


class TestDelayTimeAndDecay(unittest.TestCase):
    def test_delay_time_and_decay(self):
        self.assertEqual(delay_time_and_decay(pos_count_dict), (5, 4))