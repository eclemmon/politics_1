import numpy


def linear_to_logistic(lin_input: float, lin_min: float, lin_max: float, logistic_min: float = -1,
                       logistic_max: float = 1, k: float = 1):
    """
    This function will transform a y input within a chosen linear functions y-min and -max into the output
    of a sigmoid function based on a determined logistic functions minimum and maximum as x approaches inf and -inf.
    the logistic function's k can also be manipulated.
    :param lin_input: flaot  the input you want transformed
    :param lin_min: float the minimum of your data set's values
    :param lin_max: float the maximum of your data set's values
    :param logistic_min: float the new minimum of the sigmoid function as x approaches -inf
    :param logistic_max: float the new maximum of the sigmoid function as x approaches inf
    :param k: float the slope of the sigmoid function at its midpoint
    :return:float  returns a y value from the sigmoid function based on the transformed lin_input
    """
    linear_range = lin_max - lin_min
    logistic_range = logistic_max - logistic_min
    logistic_linear_ratio = logistic_range / linear_range
    intercept = logistic_max - lin_max * logistic_linear_ratio
    x = lin_input * logistic_linear_ratio + intercept
    midpoint = (logistic_max+logistic_min) / 2
    result = (logistic_max-logistic_min) / (1 + numpy.exp(-k * (x - midpoint))) + logistic_min
    return result


def linear_to_linear(x: float, r1min: float, r1max: float, r2min: float, r2max: float):
    """
    This function maps a given input between a min and max of range 1 to a range 2
    :param x: float
    :param r1min: float
    :param r1max: float
    :param r2min: float
    :param r2max: float
    :return: float
    """
    return (x - r1min) * (r2max - r2min) / (r1max - r1min) + r2min
