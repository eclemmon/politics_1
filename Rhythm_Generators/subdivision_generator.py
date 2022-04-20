
def subdivide_meter_into_polyrhythm(num_beats: int, subdivided_by: int):
    """
    Helper function for subdividing the total duration of a meter into n number of subdivisions.
    :param num_beats: int
    :param subdivided_by: int
    :return: list of floats
    """
    return [num_beats * 0.25 * 4 / subdivided_by for _ in range(subdivided_by)]
