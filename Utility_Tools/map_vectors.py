import math

def build_vector_one(n):
    """

    :param n:
    :return:
    """
    return (0, n)

def build_vector_two(n):
    """

    :param n:
    :return:
    """
    y = n * math.sin(math.radians(30)) * -1
    x = n * math.cos(math.radians(30)) * -1
    return x, y

def build_vector_three(n):
    """

    :param n:
    :return:
    """
    y = n * math.sin(math.radians(30)) * -1
    x = n * math.cos(math.radians(30))
    return x, y

def add_vectors(*tuples):
    result = (0, 0)
    for tup in tuples:
        result += tup
    return result
