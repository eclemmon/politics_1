import unittest
import math
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

    def test_vertice_angles_by_poly_size(self):
        self.assertEquals(vertex_angles_by_poly_size(4), [0, 0.5 * math.pi, 1 * math.pi, 1.5 * math.pi - (2 * math.pi)])

    def test_add_three_vectors_for_politics(self):
        self.assertAlmostEquals(add_three_vectors_for_politics(1, 1, 1)[0], 0)
        self.assertAlmostEquals(add_three_vectors_for_politics(1, 1, 1)[1], 0)

    def test_get_closest_polygon_vertice_index_from_three_added_vectors(self):
        pass

    def test_find_index_of_closest_vector2vertice_in_new_poly(self):
        self.assertEquals(find_index_of_closest_vector2vertex_in_new_poly(math.pi / 2, 4), 1)
        self.assertEquals(find_index_of_closest_vector2vertex_in_new_poly(math.pi / 4, 4), 0)
        self.assertEquals(find_index_of_closest_vector2vertex_in_new_poly(math.pi * 3 / 4, 4), 1)




