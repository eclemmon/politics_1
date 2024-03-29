import unittest
import math
import numpy as np
import numpy.testing

from Utility_Tools.map_vectors import *


class TestMapVectors(unittest.TestCase):
    def test_build_point_one(self):
        self.assertEqual(build_point_one(0), (0, 0))
        self.assertEqual(build_point_one(0.463), (0, 0.463))

    def test_build_point_two(self):
        for _ in range(2):
            self.assertAlmostEquals(build_point_two(5)[_], (-4.33012701892, -2.5)[_])
            self.assertAlmostEquals(build_point_two(0)[_], (0, 0)[_])
            self.assertAlmostEquals(build_point_two(1)[_], (-0.86602540378, -0.5)[_])

    def test_build_point_three(self):
        for _ in range(2):
            self.assertAlmostEquals(build_point_three(5)[_], (4.33012701892, -2.5)[_])
            self.assertAlmostEquals(build_point_three(0)[_], (0, 0)[_])
            self.assertAlmostEquals(build_point_three(1)[_], (0.86602540378, -0.5)[_])

    def test_add_points(self):
        self.assertEquals(add_points((0, 0), (-1, -1)), (-1, -1))
        self.assertEquals(add_points((-1, 2), (-3, -1), (2, -1)), (-2, 0))

    def test_origin2point_angle_from_pos_x_axis(self):
        self.assertAlmostEquals(origin2point_angle_from_pos_x_axis((0, 1)), 1.5707963268)
        self.assertAlmostEquals(origin2point_angle_from_pos_x_axis((1, 0)), 0)
        self.assertAlmostEquals(origin2point_angle_from_pos_x_axis((-1, 1)), 2.3561944902)
        self.assertAlmostEquals(origin2point_angle_from_pos_x_axis((-1, -1)), -2.3561944902)
        self.assertAlmostEquals(origin2point_angle_from_pos_x_axis((0, -1)), -1.5707963268)

    def test_vertex_angles_by_poly_size(self):
        self.assertEquals(vertex_angles_by_no_poly_sides(4), [0, 0.5 * math.pi, 1 * math.pi, 1.5 * math.pi - (2 * math.pi)])

    def test_add_three_points_for_politics(self):
        self.assertAlmostEquals(add_three_points_for_politics(1, 1, 1)[0], 0)
        self.assertAlmostEquals(add_three_points_for_politics(1, 1, 1)[1], 0)

    def test_get_closest_polygon_vertex_index_from_three_added_vectors(self):
        pass

    def test_find_index_of_closest_point2vertex_in_new_poly(self):
        self.assertEquals(find_indexes_of_closest_point2vertex_in_new_poly(math.pi / 2, 4), (1, 2))
        self.assertEquals(find_indexes_of_closest_point2vertex_in_new_poly(math.pi / 4, 4), (0, 1))
        self.assertEquals(find_indexes_of_closest_point2vertex_in_new_poly(math.pi * 3 / 4, 4), (1, 2))
        self.assertEquals(find_indexes_of_closest_point2vertex_in_new_poly(math.pi * 2 / 3 * -1, 4), (3, 2))
        self.assertEquals(find_indexes_of_closest_point2vertex_in_new_poly(math.pi * 2 / 5 * -1, 4), (3, 0))

    def test_generate_vertices_points_by_no_polygon_sides(self):
        np.testing.assert_almost_equal(generate_vertices_points_by_no_polygon_sides(4), [(1, 0), (0, 1), (-1, 0), (0, -1)], 7)

    def test_get_closest_polygon_vertex_indexes_from_three_added_points(self):
        self.assertEquals(get_closest_polygon_vertex_indexes_from_three_added_points(4, 1, 1, 0), (1, 2))
        self.assertEquals(get_closest_polygon_vertex_indexes_from_three_added_points(4, 1, 0, 1), (0, 1))
        self.assertEquals(get_closest_polygon_vertex_indexes_from_three_added_points(4, 0, 0, 1), (0, 3))
        self.assertEquals(get_closest_polygon_vertex_indexes_from_three_added_points(4, 0, 1, 1), (2, 3))

    def test_vertex_angles_by_poly_size(self):
        np.testing.assert_almost_equal(vertex_angles_by_no_poly_sides(4), [0,
                                                                           2 * math.pi / 4,
                                                                           math.pi * 4 / 4,
                                                                           -math.pi * 2 / 4])
        angles = []
        for i in range(6):
            num = i * math.pi / 3
            if num > math.pi:
                angles.append(num - (2 * math.pi))
            else:
                angles.append(num)
        np.testing.assert_almost_equal(vertex_angles_by_no_poly_sides(6), angles)

    def test_find_indexes_of_closest_point2vertex_in_new_poly(self):
        self.assertEquals(find_indexes_of_closest_point2vertex_in_new_poly(0.3, 4), (0, 1))
        self.assertEquals(find_indexes_of_closest_point2vertex_in_new_poly(1.7, 4), (1, 2))
        self.assertEquals(find_indexes_of_closest_point2vertex_in_new_poly(3.15, 6), (3, 4))

    def test_get_distance_between_points(self):
        self.assertAlmostEquals(get_distance_between_points((1, 2), (-2, -2)), 5.0)
        self.assertAlmostEquals(get_distance_between_points((-2, -2.5), (4, 2.5)), 7.8102496759067)

    def test_get_point_end_vertices_distance(self):
        self.assertAlmostEquals(get_point_end_vertices_distance((1, 0), [(0, 0), (1, 0), (0, 1)]),
                                [1, 0, math.sqrt(2)])

    def test_get_linear_weights_by_distances(self):
        numpy.testing.assert_almost_equal(get_linear_weights_by_distances((0, 1), [(0, 0), (0, 1), (1, 0)]),
                                          [0.5857864, 1, 0.4142136])


    def test_get_closest_tri_vertices_to_point(self):
        numpy.testing.assert_almost_equal(get_closest_tri_vertices_to_point(4, 0, 1), [(0, 0), (1, 0), (0, 1)])
        numpy.testing.assert_almost_equal(get_closest_tri_vertices_to_point(4, 3, 0), [(0, 0), (0, -1), (1, 0)])

    def test_get_graph_chord_indexes_and_weights(self):
        self.assertDictEqual(get_graph_chord_indexes_and_weights({"neg": 1, "neu": 1, "pos": 1}, 4),
                             {"home": 1.0, 1: 0.5, 2: 0.5})

