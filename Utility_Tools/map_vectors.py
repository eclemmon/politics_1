import math


def build_point_one(n):
    """
    Takes in a value and maps it to a vector that points directly up the y axis.
    :param n: Float length of vector along a radius of a circle where vector points up along y axis
    :return: tuple of vector values
    """
    return 0, n


def build_point_two(n):
    """
    Takes in a value and maps it to a vector that points south east, 30º below the x-axis of a cartesian plane.
    :param n: Float length of vector along a radius segment.
    :return: tuple of vector values
    """
    x = n * math.cos(math.radians(30)) * -1
    y = n * math.sin(math.radians(30)) * -1
    return x, y


def build_point_three(n):
    """
    Takes in a value and maps it to a vector that points south west, 30º below the x-axis of a cartesian plane.
    :param n: Float length of vector along a radius segment.
    :return: tuple of vector values
    """
    x = n * math.cos(math.radians(30))
    y = n * math.sin(math.radians(30)) * -1
    return x, y


def add_points(*tuples):
    """
    Adds all tuples as vector math. (-1, 0) + (1, 2) = (0, 2)
    :param tuples: a set of tuples.
    :return: tuple of all tuples added together
    """
    return tuple([sum(x) for x in zip(*tuples)])


def add_three_points_for_politics(*values):
    """
    Takes in a tuple of 3 values between 0 and 1, constructs 3 points and adds them.
    :param values: Tuple of three tuples as points.
    :return: tuple (x, y)
    """
    v1 = build_point_one(values[0])
    v2 = build_point_two(values[1])
    v3 = build_point_three(values[2])
    return add_points(v1, v2, v3)


def origin2point_angle_from_pos_x_axis(tup):
    """
    Calculates the angle in radians from the x axis. Quadrants I & II returns a positive value, III & IV, negative.
    (uses atan2 on two points).
    :param tup: Tuple of a point (x, y)
    :return: Float in radians
    """
    return math.atan2(tup[1], tup[0])


def get_closest_polygon_vertex_indexes_from_three_added_points(no_polygon_sides, *values):
    """
    For an equilateral polygon with no of sides x, finds the indexes of the closest two vertices of the polygon when
    it is inscribed within a circle.
    :param no_polygon_sides: Integer of number of sides.
    :param values: Three floats between 0.0 and 1.0
    :return: Tuple of two sorted indexes. E.g. (0, 3)
    """
    v = add_three_points_for_politics(*values)
    angle_in_rads = origin2point_angle_from_pos_x_axis(v)
    return tuple(sorted(find_indexes_of_closest_point2vertex_in_new_poly(angle_in_rads, no_polygon_sides)))


def vertex_angles_by_no_poly_sides(no_polygon_sides):
    """
    Gets a list of angles to the vertices of an equilateral polygon of n sides in radians.
    :param no_polygon_sides: Integer
    :return: List of angles in radians. e.g. [0.0, pi/2, pi, 3pi/2]
    """
    res = []
    for v in range(no_polygon_sides):
        if v == 0:
            res.append(0)
        else:
            num = 2 * math.pi * v / no_polygon_sides
            if num > math.pi:
                res.append(num - (2 * math.pi))
            else:
                res.append(num)
    return res


def find_indexes_of_closest_point2vertex_in_new_poly(original_origin2point_angle, polygon_size):
    """
    Finds the index of the closest two angles to the input vector angle from a set of angles in radians. The set of
    angles is derived from finding the vertices of an equal sided polygon inscribed in a circle, and taking the
    angle of these line segments from the positive x-axis. When original vector angle is the bisector of the two line
    segments it takes the smaller value.
    :param original_origin2point_angle:
    :param polygon_size:
    :return: tuple of closest two vertice's indexes
    """
    polygon_angles = vertex_angles_by_no_poly_sides(polygon_size)
    closest_index = min(range(len(polygon_angles)), key=lambda i: abs(polygon_angles[i] - original_origin2point_angle))
    if original_origin2point_angle >= 0:
        if original_origin2point_angle >= polygon_angles[closest_index]:
            return (closest_index,
                    (closest_index + 1) % polygon_size)  # returns the closest index and the vector greater than it.
        else:
            return (closest_index,
                    (closest_index - 1) % polygon_size)  # returns the closest index and the vector smaller than it.
    else:
        if original_origin2point_angle > polygon_angles[closest_index]:
            return closest_index, (closest_index + 1) % polygon_size
        else:
            return closest_index, (closest_index - 1) % polygon_size


def generate_vertices_points_by_no_polygon_sides(no_polygon_sides):
    """
    Generates the vertices of an equilateral polygon based on the number of sides as a list.
    :param no_polygon_sides: Integer
    :return: List of tuples. e.g. [(1, 0), (0, 1), (-1, 0), (0, -1)]
    """
    polygon_angles = vertex_angles_by_no_poly_sides(no_polygon_sides)
    return list(zip([math.cos(a) for a in polygon_angles], [math.sin(a) for a in polygon_angles]))


def get_distance_between_points(point1, point2):
    """
    Calculates the distance between two points on a cartesian plane.
    :param point1: Tuple (x, y)
    :param point2: Tuple (x, y)
    :return: Float as distance
    """
    return math.hypot(point2[0]-point1[0], point2[1]-point1[1])


def get_point_end_vertices_distance(point, vertices):
    """
    Gets the distance between a point and a list of points.
    :param point: Tuple (x, y)
    :param vertices: List of tuples e.g. [(x, y), (x, y)]
    :return: List of floats.
    """
    return [get_distance_between_points(point, i) for i in vertices]


def get_linear_weights_by_distances(point, *vertices):
    """
    Gets the weights of the distances between a point and a list of vertices. If distance between point i and vertex j
    is 0, weight = 1.
    :param point: tuple (x, y)
    :param vertices: List of tuples [(x, y), (x, y)]
    :return: List of floats.
    """
    distances = get_point_end_vertices_distance(point, *vertices)
    return [(sum(distances) - distance) / sum(distances) for distance in distances]
# TODO: make an exponentially decreasing weighting function.


def get_closest_tri_vertices_to_point(no_polygon_sides, *indexes):
    """
    Gets two vertices of a polygon with n sides based on the index of of the vertex. Vertex index 0 starts at x-axis
    and continues counter clockwise. Appends two vertices to a list containing the origin to give three points that
    represent the vertices of a triangle inscribed inside the polygon.
    :param no_polygon_sides: Integer
    :param indexes: List of indexes. e.g. [0, 1]
    :return: List of tuples [(0, 0), (0, 1), (1, 0)]
    """
    res = [(0, 0)]
    vertices = generate_vertices_points_by_no_polygon_sides(no_polygon_sides)
    return res + [vertices[i] for i in indexes]


def get_graph_chord_indexes_and_weights(sentiment_values, num_adjacent_chords):
    """
    Gets the respective weights of chords in a graph based on the input sentiment values. Chords will always include
    the current node, as well as two of the "next" chords in the graph based on the index that is also calculated.
    :param sentiment_values: Dictionary of three sentiment values from NLTK's VADER {"neg": x, "neu": y, "pos": z}
    :param num_adjacent_chords: Integer
    :return: Dictionary of indexes => weights, "home" is current chord. e.g. {"home": 1.0, 2: 0.54325, 3: 0.335472}
    """
    sentiment_values = list(sentiment_values.values())
    # TODO: fix the ordering of the sentiment values
    # get vector end based on sentiment values
    vector_end = add_three_points_for_politics(*sentiment_values)
    # get indexes of the closest vertexes
    indexes = get_closest_polygon_vertex_indexes_from_three_added_points(num_adjacent_chords, *sentiment_values)
    # generate closest vertices
    vertices = get_closest_tri_vertices_to_point(num_adjacent_chords, *indexes)
    # get weights based on the distance between vector end and closest vertices
    weights = get_linear_weights_by_distances(vector_end, vertices)
    indexes = ['home'] + list(indexes)
    return dict(zip(indexes, weights))
