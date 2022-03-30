
class Meter:
    def __init__(self, num_beats, accent_weights, subdivisions):
        self.num_beats = num_beats
        self.accent_weights = accent_weights
        self.subdivisions = subdivisions

    def __repr__(self):
        return self.accent_weights


class ComplexMeter(Meter):
    def __init__(self, num_beats, accent_weights, subdivisions):
        if num_beats == 5 or num_beats == 7:
            if num_beats != len(accent_weights) and sum(subdivisions) != num_beats:
                raise ValueError("The number of accent_weights and subdivisions in complex meter must equal the "
                                 "number of beats.")
            else:
                super().__init__(num_beats, accent_weights, subdivisions)
        else:
            raise ValueError("Complex meter must have accent_weights divisible by 3 and be at least 6 beats.")


class CompoundMeter(Meter):
    def __init__(self, num_beats, accent_weights, subdivisions):
        if (num_beats % 3 == 0) and num_beats >= 6 and sum(subdivisions) == num_beats:
            if num_beats != len(accent_weights):
                raise ValueError(
                    'The number of accent_weights and subdivisions in compound meter must equal the number of beats.')
            else:
                super().__init__(num_beats, accent_weights, subdivisions)
        else:
            raise ValueError("Compound meter must have accent_weights divisible by 3 and be at least 6 beats.")


class SimpleTriple(Meter):
    def __init__(self):
        super().__init__(3, [3, 1, 1], [3])


class SimpleDuple(Meter):
    def __init__(self, num_beats):
        if num_beats == 2:
            super().__init__(2, [3, 2], [1, 1])
        elif num_beats == 4:
            super().__init__(4, [3, 1, 2, 1], [2, 2])
        else:
            raise ValueError("SimpleDuple can only be in 2 or 4!")

