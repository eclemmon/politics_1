import unittest
from Harmony_Generators.octave_displacement_generator import get_octave_placement

max_chars = '*' * 280
min_chars = ''
medium_chars = '*' * 140


class TestOctaveDisplacementGenerator(unittest.TestCase):
    def test_get_octave_placement(self):
        self.assertEqual(get_octave_placement(max_chars), 1)
        self.assertEqual(get_octave_placement(min_chars), 10)
        self.assertEqual(get_octave_placement(medium_chars), 6)
