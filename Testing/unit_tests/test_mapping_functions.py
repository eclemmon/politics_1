import unittest

from Utility_Tools.mapping_functions import *


class TestMappingFunctions(unittest.TestCase):
    def test_linear_to_logistic(self):
        self.assertAlmostEqual(linear_to_logistic(0, 0, 1000), -0.4621171572600098)
        self.assertAlmostEqual(linear_to_logistic(5, 0, 10), 0)
        self.assertAlmostEqual(linear_to_logistic(10, 0, 10), 0.4621171572600098)

    def test_linear_to_linear(self):
        self.assertAlmostEqual(linear_to_linear(0, 0, 280, 100, 0), 100)
        self.assertAlmostEqual(linear_to_linear(280, 0, 280, 100, 0), 0)
        self.assertAlmostEqual(linear_to_linear(140, 0, 280, 100, 0), 50)
