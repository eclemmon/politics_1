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


def vector_angle_from_pos_x_axis(tup):
    return math.atan2(tup[1], tup[0])


def get_closest_polygon_vertex_indexes_from_three_added_vectors(polygon_size, *values):
    v = add_three_vectors_for_politics(*values)
    # print(v)
    angle_in_rads = vector_angle_from_pos_x_axis(v)
    # print(angle_in_rads)
    return tuple(sorted(find_indexes_of_closest_vector2vertex_in_new_poly(angle_in_rads, polygon_size)))


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


def find_indexes_of_closest_vector2vertex_in_new_poly(original_vector_angle, polygon_size):
    """
    Finds the index of the closest two angles to the input vector angle from a set of angles in radians. The set of
    angles is derived from finding the vertices of an equal sided polygon inscribed in a circle, and taking the
    angle of these line segments from the positive x-axis. When original vector angle is the bisector of the two line
    segments it takes the smaller value.
    :param original_vector_angle:
    :param polygon_size:
    :return: tuple of two closest vertices in circle
    """
    polygon_angles = vertex_angles_by_poly_size(polygon_size)
    # print("polygon angles: ", polygon_angles)
    # print("original vector angle: ", original_vector_angle)
    closest_index = min(range(len(polygon_angles)), key=lambda i: abs(polygon_angles[i] - original_vector_angle))
    # print("closest index: ", closest_index)
    if original_vector_angle >= 0:
        if original_vector_angle >= polygon_angles[closest_index]:
            return (closest_index,
                    (closest_index + 1) % polygon_size)  # returns the closest index and the vector greater than it.
        else:
            return (closest_index,
                    (closest_index - 1) % polygon_size)  # returns the closest index and the vector smaller than it.
    else:
        if original_vector_angle > polygon_angles[closest_index]:
            return closest_index, (closest_index + 1) % polygon_size
        else:
            return closest_index, (closest_index - 1) % polygon_size


def generate_vertices_points_by_polygon_size(polygon_size):
    polygon_angles = vertex_angles_by_poly_size(polygon_size)
    return list(zip([math.cos(a) for a in polygon_angles], [math.sin(a) for a in polygon_angles]))


def get_distance_between_points(point1, point2):
    return math.hypot(point2[0]-point1[0], point2[1]-point1[1])


def get_vector_end_vertices_distance(vector_end, vertices):
    return [get_distance_between_points(vector_end, i) for i in vertices]


def get_weights_by_distances(vector_end, *vertices):
    distances = get_vector_end_vertices_distance(vector_end, *vertices)
    return [(sum(distances) - distance) / sum(distances) for distance in distances]


def get_closest_tri_vertices_to_vector(polygon_size, *indexes):
    res = [(0, 0)]
    vertices = generate_vertices_points_by_polygon_size(polygon_size)
    print(vertices)
    print(indexes)
    return res + [vertices[i] for i in indexes]


def get_graph_chord_indexes_and_weights(sentiment_values, num_adjacent_chords):
    sentiment_values = list(sentiment_values.values())
    # get vector end based on sentiment values
    vector_end = add_three_vectors_for_politics(*sentiment_values)
    # get indexes of closest vertexes
    indexes = get_closest_polygon_vertex_indexes_from_three_added_vectors(num_adjacent_chords, *sentiment_values)
    # generate closest vertices
    vertices = get_closest_tri_vertices_to_vector(num_adjacent_chords, *indexes)
    # get weights based on the distance between vector end and closest vertices
    weights = get_weights_by_distances(vector_end, vertices)
    indexes = ['home'] + list(indexes)
    print(weights)
    return dict(zip(indexes, weights))
