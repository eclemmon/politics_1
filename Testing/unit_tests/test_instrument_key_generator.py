import unittest
from Synthesis_Generators.instrument_key_generator import generate_instrument_dict

instrument_names = ['sin', 'saw', 'noise']
instrument_dict = {'sound1': 'sin', 'sound2': 'saw', 'sound3': 'noise'}


class TestInstrumentKeyGenerator(unittest.TestCase):
    def test_generate_instrument_dict(self):
        self.assertDictEqual(generate_instrument_dict(instrument_names), instrument_dict)
