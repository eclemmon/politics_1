from Classes.meter import *

cybernetic_republic_meter_data = {
    'two': SimpleDuple(2),
    'three': SimpleTriple(),
    'four': SimpleDuple(4),
    'five-23': ComplexMeter(5, [3, 1, 2, 1, 1], [2, 3]),
    'five-32': ComplexMeter(5, [3, 1, 1, 2, 1], [3, 2]),
    'six': CompoundMeter(6, [3, 1, 1, 2, 1, 1], [3, 3]),
    'seven-223': ComplexMeter(7, [3, 1, 2, 1, 2, 1, 1], [2, 2, 3]),
    'seven-232': ComplexMeter(7, [3, 1, 2, 1, 1, 3, 1], [2, 3, 2]),
    'seven-322': ComplexMeter(7, [3, 1, 1, 2, 1, 2, 1], [3, 2, 2]),
    'nine': CompoundMeter(9, [3, 1, 1, 2, 1, 1, 2, 1, 1], [3, 3, 3]),
    'twelve': CompoundMeter(12, [3, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1], [3, 3, 3, 3])
}