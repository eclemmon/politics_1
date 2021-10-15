import unittest
from Utility_Tools.map_vectors import *

class TestMapVectors(unittest.TestCase):
    def test_build_vector_one(self):
        self.assertEqual(build_vector_one(0), (0, 0))
        self.assertEqual(build_vector_one(0.463), (0, 0.463))

    def test_build_vector_two(self):
        for _ in range(2):
            self.assertAlmostEquals(build_vector_two(5)[_], (-4.33012701892, -2.5)[_])
            self.assertAlmostEquals(build_vector_two(0)[_], (0, 0)[_])
            self.assertAlmostEquals(build_vector_two(1)[_], (-0.86602540378, -0.5)[_])

    def test_build_vector_three(self):
        for _ in range(2):
            self.assertAlmostEquals(build_vector_three(5)[_], (4.33012701892, -2.5)[_])
            self.assertAlmostEquals(build_vector_three(0)[_], (0, 0)[_])
            self.assertAlmostEquals(build_vector_three(1)[_], (0.86602540378, -0.5)[_])

    def test_add_vectors(self):
        self.assertEquals(add_vectors((0, 0), (-1, -1)), (-1, -1))
        self.assertEquals(add_vectors((-1, 2), (-3, -1), (2, -1)), (-2, 0))

    def test_vector_angle_from_pos_x_axis(self):
        self.assertAlmostEquals(vector_angle_from_pos_x_axis((0, 1)), 1.5707963268)
        self.assertAlmostEquals(vector_angle_from_pos_x_axis((1, 0)), 0)
        self.assertAlmostEquals(vector_angle_from_pos_x_axis((-1, 1)), 2.3561944902)
        self.assertAlmostEquals(vector_angle_from_pos_x_axis((-1, -1)), -2.3561944902)
        self.assertAlmostEquals(vector_angle_from_pos_x_axis((0, -1)), -1.5707963268)
