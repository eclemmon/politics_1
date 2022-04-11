
def subdivide_meter_into_polyrhythm(num_beats, subdivided_by):
    return [num_beats * 0.25 * 4 / subdivided_by for _ in range(subdivided_by)]