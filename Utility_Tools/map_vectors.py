import math

def build_vector_one(n):
    """
    Takes in a value and maps it to a vector that points directly up the y axis.
    :param n: Float length of vector along a radius of a circle where vector points up along y axis
    :return: tuple of vector values
    """
    return 0, n

def build_vector_two(n):
    """
    Takes in a value and maps it to a vector that points south east, 30º below the x-axis of a cartesian plane.
    :param n: Float length of vector along a radius segment.
    :return: tuple of vector values
    """
    x = n * math.cos(math.radians(30)) * -1
    y = n * math.sin(math.radians(30)) * -1
    return x, y

def build_vector_three(n):
    """
    Takes in a value and maps it to a vector that points south west, 30º below the x-axis of a cartesian plane.
    :param n: Float length of vector along a radius segment.
    :return: tuple of vector values
    """
    x = n * math.cos(math.radians(30))
    y = n * math.sin(math.radians(30)) * -1
    return x, y

def add_vectors(*tuples):
    """
    Adds all tuples as vector math. (-1, 0) + (1, 2) = (0, 2)
    :param tuples: a set of tuples.
    :return: tuple of all tuples added together
    """
    return tuple([sum(x) for x in zip(*tuples)])

def add_three_vectors_for_politics(*values):
    v1 = build_vector_one(values[0])
    v2 = build_vector_two(values[1])
    v3 = build_vector_three(values[2])
    return add_vectors(v1, v2, v3)

def vector_angle_from_pos_x_axis(tuple):
    return math.atan2(tuple[1], tuple[0])

def get_closest_polygon_vertex_index_from_three_added_vectors(values, polygon_size):
    v = add_three_vectors_for_politics(values)
    angle_in_rads = vector_angle_from_pos_x_axis(v)
    return find_index_of_closest_vector2vertex_in_new_poly(angle_in_rads, polygon_size)

def vertex_angles_by_poly_size(polygon_size):
    res = []
    for v in range(polygon_size):
        if v == 0:
            res.append(0)
        else:
            num = 2 * math.pi * v / polygon_size
            if num > math.pi:
                res.append(num - (2 * math.pi))
            else:
                res.append(num)
    return res

def find_index_of_closest_vector2vertex_in_new_poly(original_vector_angle, polygon_size):
    """
    Finds the index of the closest angle to the input vector angle from a set of angles in radians. The set of angles
    is derived from finding the vertices of an equal sided polygon inscribed in a circle, and taking the angle of
    these line segments from the positive x-axis.
    When original vector angle is the bisector of the two line segments it takes the smaller value.
    :param original_vector_angle:
    :param polygon_size:
    :return:
    """
    polygon_angles = vertex_angles_by_poly_size(polygon_size)
    return min(range(len(polygon_angles)), key=lambda i: abs(abs(polygon_angles[i]) - abs(original_vector_angle)))
