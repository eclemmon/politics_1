import unittest

from Utility_Tools.mapping_functions import *


class TestMappingFunctions(unittest.TestCase):
    def test_linear_to_logistic(self):
        self.assertAlmostEqual(linear_to_logistic(0, 0, 10), -1)
        self.assertAlmostEqual(linear_to_logistic(5, 0, 10), 0)
        self.assertAlmostEqual(linear_to_logistic(10, 0, 10), 1)
