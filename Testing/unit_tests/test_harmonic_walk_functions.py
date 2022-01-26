import unittest

from Harmony_Generators.harmonic_walk_functions import get_octave_placement

max_chars = '*' * 280
min_chars = ''
medium_chars = '*' * 140

class TestHarmonicWalkFunctions(unittest.TestCase):
    def test_get_octave_placement(self):
        self.assertEqual(get_octave_placement(max_chars), 8)
        self.assertEqual(get_octave_placement(min_chars), 1)
        self.assertEqual(get_octave_placement(medium_chars), 5)