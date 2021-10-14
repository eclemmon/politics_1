import math

def build_vector_one(n):
    """
    Takes in a value and maps it to a vector that points directly up the y axis.
    :param n: Float length of vector along a radius of a circle where vector points up along y axis
    :return: tuple of vector values
    """
    return (0, n)

def build_vector_two(n):
    """
    Takes in a value and maps it to a vector that points south east, 30º below the x-axis of a cartesian plane.
    :param n: Float length of vector along a radius segment.
    :return: tuple of vector values
    """
    y = n * math.sin(math.radians(30)) * -1
    x = n * math.cos(math.radians(30)) * -1
    return x, y

def build_vector_three(n):
    """
    Takes in a value and maps it to a vector that points south west, 30º below the x-axis of a cartesian plane.
    :param n: Float length of vector along a radius segment.
    :return: tuple of vector values
    """
    y = n * math.sin(math.radians(30)) * -1
    x = n * math.cos(math.radians(30))
    return x, y

def add_vectors(*tuples):
    result = (0, 0)
    for tup in tuples:
        result += tup
    return result
