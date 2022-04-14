from Classes.meter import SimpleDuple
from Classes.meter import SimpleTriple
from Classes.meter import ComplexMeter
from Classes.meter import CompoundMeter
from itertools import chain
import random


def rr(i, note_length=0.25):
    """
    Helper function that returns a range of rests as a list
    :param i: Integer of number of rests
    :return: List of strings that represent rests
    """
    return ['/r'+str(note_length) for _ in range(i)]


def nr(i, note_length=0.25):
    """
    Helper function that returns a range of notes as a list
    :param i: Integer of number of notes
    :param note_length: Float of length of note value — should be in multiples of 0.25
    :return: List of floats that represent note values
    """
    return [note_length for _ in range(i)]


def subdivide_meter_into_polyrhythm(num_beats, subdivided_by):
    return [num_beats * 0.25 * 4 / subdivided_by for _ in range(subdivided_by)]


class RhythmSection:
    def __init__(self, meter, midi_note_arrays=None, midi_note_duration_arrays=None):
        self.meter = meter
        self.midi_notes = midi_note_arrays
        self.midi_note_duration_arrays = midi_note_duration_arrays

    def transform_rhythm_to_meter(self):
        if self.meter.num_beats == 2:
            self.rhythm_to_duple()
        elif self.meter.num_beats == 3:
            self.rhythm_to_triple()
        elif self.meter.num_beats == 4:
            self.rhythm_to_four()
        elif self.meter.num_beats == 5:
            self.rhythm_to_five()
        elif self.meter.num_beats == 6:
            self.rhythm_to_six()
        elif self.meter.num_beats == 7:
            self.rhythm_to_seven()
        elif self.meter.num_beats == 9:
            self.rhythm_to_nine()
        elif self.meter.num_beats == 12:
            self.rhythm_to_twelve()
        else:
            pass

    def rhythm_to_duple(self):
        pass

    def rhythm_to_triple(self):
        pass

    def rhythm_to_four(self):
        pass

    def rhythm_to_five(self):
        pass

    def rhythm_to_six(self):
        pass

    def rhythm_to_seven(self):
        pass

    def rhythm_to_nine(self):
        pass

    def rhythm_to_twelve(self):
        pass

    def flatten(t):
        return [item for sublist in t for item in sublist]

    def build_new_midi_note_duration_array(self, *slices):
        new_midi_note_durations_array = []
        for array in self.midi_note_duration_arrays:
            new_array = []
            for sl in slices:
                new_array = new_array + array[sl]
            new_midi_note_durations_array.append(new_array)
        return new_midi_note_durations_array


class BreakBeat(RhythmSection):
    def __init__(self, meter, option=2):
        super().__init__(meter)
        if option == 1:
            self.midi_notes = [i for i in range(60, 68)]
            self.midi_note_duration_arrays = [
                [0.25, '/r', 0.25, '/r', '/r', '/r', 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', '/r', 0.25, '/r', 0.25,
                 '/r', 0.25, '/r', '/r', '/r', 0.25, 0.25, '/r', 0.25, '/r', '/r', '/r', '/r', 0.25, '/r', 0.25, '/r',
                 0.25, '/r', '/r', '/r', 0.25, 0.25, '/r', 0.25, '/r', '/r', '/r', '/r', '/r', 0.25, 0.25, '/r', 0.25,
                 '/r', '/r', '/r', 0.25, '/r', '/r', 0.25, 0.25, '/r', 0.25, '/r', '/r', '/r'],
                [0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25, '/r',
                 '/r', '/r', 0.25, 0.25, 0.25, '/r', '/r', '/r', 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25, 0.25, 0.25,
                 '/r', 0.25, 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r',
                 '/r',
                 0.25, 0.25, '/r', '/r', 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25],
                ['/r', '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r',
                 '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r',
                 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', 0.25, '/r', '/r', '/r', 0.25,
                 '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', 0.25, '/r'],
                ['/r', '/r', '/r', '/r', '/r', '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r',
                 '/r', '/r', '/r', '/r', '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r',
                 '/r', '/r', '/r', '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r',
                 '/r', '/r', '/r', '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r'],
                ['/r' for _ in range(4 * 4 + 1)] + [0.25, '/r', '/r', '/r', '/r', '/r', '/r', 0.25] +
                ['/r' for _ in range(9 * 4 + 3)],
                ['/r' for _ in range(5 * 4 + 3)] + [0.25] + ['/r' for _ in range(10 * 4)],
                [0.25] + ['/r' for _ in range(6 * 4 + 1)] + [0.25] + ['/r' for _ in range(3 * 4 + 3)] + [0.25, 0.25] +
                ['/r' for _ in range(4)] + [0.25, 0.25] + ['/r', '/r', '/r'] + [0.25, 0.25] + ['/r', '/r', '/r'] +
                [0.25, 0.25] + ['/r', '/r', '/r'] + [0.25],
                ['/r' for _ in range(4)] + [0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] +
                [0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] + [0.25] +
                ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(9)] +
                [0.25] + [0.25]
            ]
        else:
            self.midi_notes = [i for i in range(36, 42)]
            self.midi_note_duration_arrays = [
                [0.25, '/r', 0.25] + ['/r' for _ in range(3)] + [0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', '/r', 0.25,
                '/r', 0.25, '/r', 0.25, '/r', '/r', '/r', 0.25, 0.25, '/r', 0.25] + ['/r' for _ in range(4)] + [0.25,
                '/r', 0.25, '/r', 0.25, '/r', '/r', '/r', 0.25, 0.25, '/r', 0.25] + ['/r' for _ in range(5)] + [0.25,
                0.25, '/r', 0.25, '/r', '/r', '/r', 0.25, '/r', '/r', 0.25, 0.25, '/r', 0.25, '/r', '/r', '/r'],
                ['/r' for _ in range(4)] + [0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] +
                [0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] + [0.25] +
                ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(9)] +
                [0.25, 0.25],
                [0.25, 0.25, '/r'] + [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25, 0.25, '/r'] +
                [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25, 0.25,
                                                                                                  '/r'] + [0.25, 0.25,
                                                                                                           0.25,
                                                                                                           '/r'] + [
                    0.25, 0.25, 0.25, '/r'] + [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25,
                                                                          0.25, '/r'] + [0.25, 0.25, 0.25, '/r',
                                                                                         '/r'] + [0.25, 0.25, '/r',
                                                                                                  '/r', 0.25, 0.25,
                                                                                                  '/r', 0.25, 0.25,
                                                                                                  0.25, '/r', 0.25],
                ['/r' for _ in range(6)] + [0.25] + ['/r' for _ in range(15)] + [0.25] + ['/r' for _ in range(15)] +
                [0.25] + ['/r' for _ in range(16)] + [0.25] + ['/r' for _ in range(8)],
                ['/r', '/r', 0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] + [0.25] +
                ['/r' for _ in range(15)] + [0.25] + ['/r' for _ in range(11)] + [0.25] + ['/r' for _ in range(3)] +
                [0.25] + ['/r' for _ in range(11)] + [0.25, '/r'],
                ['/r' for _ in range(6 * 4 + 2)] + [0.25] + ['/r' for _ in range(15)] + [0.25, 0.25] +
                ['/r' for _ in range(4)] + [0.25, '/r', '/r', 0.25, '/r', '/r', 0.25, '/r', '/r', 0.25, '/r', '/r',
                                            0.25, 0.25, 0.25, 0.25]
            ]

        self.transform_rhythm_to_meter()

    def rhythm_to_duple(self):
        new_midi_note_durations_array = []
        for array in self.midi_note_duration_arrays:
            new_array = array[0:8] + array[16:24] + array[32:40] + array[56:64]
            new_midi_note_durations_array.append(new_array)
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_triple(self):
        new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 12), slice(16, 28),
                                                                                slice(0, 12), slice(16, 28))
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_five(self):
        if self.meter.subdivisions == [2, 3]:
            new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 4), slice(16, 22),
                                                                                    slice(0, 4), slice(16, 22))
        else:
            new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 6), slice(20, 24),
                                                                                    slice(0, 6), slice(60, 64))
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_six(self):
        new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 6), slice(0, 6),
                                                                                slice(6, 12), slice(0, 6))
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_seven(self):
        if self.meter.subdivisions == [2, 2, 3]:
            new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 10),
                                                                                    slice(0, 6))
        elif self.meter.subdivisions == [2, 3, 2]:
            new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 4), slice(0, 6),
                                                                                    slice(6, 10))
        else:
            new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 6), slice(0, 4),
                                                                                    slice(6, 10))
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_nine(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(6, 12), slice(0, 6), slice(0, 6))

    def rhythm_to_twelve(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(6, 12), slice(0, 6),
                                                                                 slice(0, 6), slice(0, 6))


class CompoundSix(RhythmSection):
    def __init__(self, meter):
        super().__init__(meter)
        self.midi_notes = [midi_note for midi_note in range(44, 48)]
        self.midi_note_duration_arrays = [
            [0.25] + rr(11) + [0.25] + rr(9) + [0.25, '/r', 0.25] + rr(11) + [0.25] + rr(5) + [0.25] + rr(3) +
            [0.25, '/r'],
            rr(5) + [0.25] + rr(11) + [0.25] + rr(11) + [0.25] + rr(11) + [0.25] + rr(2) + [0.25] + rr(3),
            list(chain.from_iterable([[0.25, '/r'] for _ in range(24)])),
            rr(6) + [0.25] + rr(11) + [0.25] + rr(11) + [0.25] + rr(11) + [0.25] + rr(2) + [0.25] + rr(2)
        ]
        self.transform_rhythm_to_meter()

    def rhythm_to_duple(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 10),
                                                                                 slice(36, 37), slice(41, 48))

    def rhythm_to_triple(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 3), slice(5, 9), slice(5, 10),
                                                                                 slice(0, 3), slice(5, 9),
                                                                                 slice(41, 44),
                                                                                 slice(2, 4))

    def rhythm_to_four(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 10), slice(0, 4),
                                                                                 slice(6, 10), slice(0, 4),
                                                                                 slice(6, 10),
                                                                                 slice(36, 37), slice(41, 48))

    def rhythm_to_five(self):
        if self.meter.subdivisions == [2, 3]:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 3), slice(5, 12),
                                                                                     slice(0, 3), slice(17, 24))
        else:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 10), slice(0, 8),
                                                                                     slice(22, 24))

    def rhythm_to_seven(self):
        if self.meter.subdivisions == [2, 2, 3]:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 3), slice(5, 9),
                                                                                     slice(5, 12), slice(0, 3),
                                                                                     slice(5, 9), slice(17, 24))
        elif self.meter.subdivisions == [2, 3, 2]:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 3), slice(5, 11),
                                                                                     slice(5, 9))
        else:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 9), slice(5, 10))

    def rhythm_to_nine(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 11), slice(5, 12),
                                                                                 slice(0, 11), slice(41, 48))

    def rhythm_to_twelve(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 11), slice(5, 11),
                                                                                 slice(17, 24), slice(0, 11),
                                                                                 slice(5, 11), slice(41, 48))


class TakeFive(RhythmSection):
    def __init__(self, meter):
        super().__init__(meter)
        self.midi_notes = [midi_note for midi_note in range(48, 53)]
        self.midi_note_duration_arrays = [
            [0.25] + rr(9) + [0.25] + rr(5) + [0.25] + rr(3) + [0.25] + rr(9) + [0.25] + rr(5) + [0.25] + rr(3),
            [0.25] + rr(5) + [0.25, '/r', 0.25, '/r', 0.25] + rr(5) + [0.25, '/r', 0.25, '/r', 0.25] + rr(5) + [0.25,
                                                                                                                '/r',
                                                                                                                0.25,
                                                                                                                '/r',
                                                                                                                0.25] + rr(
                5) + [0.25, '/r', 0.25, '/r'],
            rr(2) + [0.25, '/r', 0.25, '/r', '/r', 0.25] + rr(4) + [0.25, '/r', 0.25, '/r', '/r', 0.25] + rr(4) + [0.25,
                                                                                                                   '/r',
                                                                                                                   0.25,
                                                                                                                   '/r',
                                                                                                                   '/r',
                                                                                                                   0.25] + rr(
                4) + [0.25, '/r', 0.25, '/r', '/r', 0.25] + rr(2),
            rr(6) + [0.25] + rr(11) + [0.25, 0.25] + rr(2) + [0.25, 0.25] + rr(2) + [0.25, '/r', 0.25, 0.25, '/r'] +
            nr(5) + rr(2) + nr(2),
            rr(10) + [0.25] + rr(19) + [0.25] + rr(5) + [0.25, '/r', 0.25, '/r']
        ]
        self.transform_rhythm_to_meter()

    def rhythm_to_duple(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 10),
                                                                                 slice(30, 34), slice(36, 40))

    def rhythm_to_triple(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 10),
                                                                                 slice(6, 10), slice(30, 34),
                                                                                 slice(36, 40), slice(36, 40))

    def rhythm_to_four(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(2, 6), slice(6, 10),
                                                                                 slice(2, 6), slice(20, 28),
                                                                                 slice(32, 40))

    def rhythm_to_five(self):
        if self.meter.subdivisions == [3, 2]:
            pass
        else:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(16, 20), slice(6, 10),
                                                                                     slice(8, 10),
                                                                                     slice(36, 40), slice(30, 36))

    def rhythm_to_six(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 6), slice(6, 10),
                                                                                 slice(8, 10),
                                                                                 slice(20, 26), slice(36, 40),
                                                                                 slice(38, 40))

    def rhythm_to_seven(self):
        if self.meter.subdivisions == [2, 2, 3]:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 10),
                                                                                     slice(6, 8), slice(6, 8),
                                                                                     slice(6, 8), slice(0, 4),
                                                                                     slice(10, 14),
                                                                                     slice(30, 36))
        elif self.meter.subdivisions == [2, 3, 2]:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 8),
                                                                                     slice(6, 8), slice(6, 8),
                                                                                     slice(16, 20), slice(20, 24),
                                                                                     slice(32, 34), slice(32, 34),
                                                                                     slice(32, 34), slice(36, 40))
        else:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 6), slice(6, 10),
                                                                                     slice(6, 10), slice(30, 36),
                                                                                     slice(36, 40), slice(36, 40))

    def rhythm_to_nine(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 6), slice(6, 10),
                                                                                 slice(8, 10), slice(6, 10),
                                                                                 slice(8, 10), slice(20, 26),
                                                                                 slice(6, 10), slice(8, 10),
                                                                                 slice(36, 40), slice(38, 40))

    def rhythm_to_twelve(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 6), slice(6, 10),
                                                                                 slice(8, 10), slice(6, 10),
                                                                                 slice(8, 10), slice(6, 10),
                                                                                 slice(8, 10), slice(20, 26),
                                                                                 slice(6, 10), slice(8, 10),
                                                                                 slice(6, 10), slice(8, 10),
                                                                                 slice(36, 40), slice(38, 40))


class FourOnTheFloor(RhythmSection):
    def __init__(self, meter):
        super().__init__(meter)
        self.midi_notes = [midi_note for midi_note in range(76, 85)]
        self.midi_note_duration_arrays = [
            list(chain.from_iterable([[0.25, '/r'] for _ in range(32)])),
            rr(3 * 12 + 1) + nr(2) + ['/r'] + [0.25] + rr(10) + [0.25, '/r', 0.25, '/r', 0.25, '/r'],
            rr(2) + [0.25] + rr(3) + [0.25] + rr(3) + [0.25] + rr(3) + [0.25] + rr(3) + [0.25] + rr(3) + [0.25] +
            rr(3) + [0.25] + rr(3) + [0.25] + rr(1),
            nr(32),
            rr(7) + [0.25] + rr(6 * 4),
            rr(5) + nr(1) + rr(6 * 4 + 2),
            rr(2) + nr(2) + rr(4 * 6 + 2) + nr(1) + rr(8),
            rr(12) + nr(1) + rr(8) + nr(1) + rr(4) + nr(1) + rr(3) + nr(1) + rr(1),
            rr(6 * 4) + nr(1) + rr(3) + nr(1) + rr(1) + nr(1) + rr(1)
        ]
        self.transform_rhythm_to_meter()

    def rhythm_to_triple(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(4, 8), slice(10, 12),
                                                                                 slice(16, 20), slice(18, 20),
                                                                                 slice(24, 28), slice(26, 28),
                                                                                 slice(28, 32), slice(30, 32))

    def rhythm_to_five(self):
        if self.meter.subdivisions == [2, 3]:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 8), slice(6, 8),
                                                                                     slice(24, 32), slice(30, 32))
        else:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(2, 4),
                                                                                     slice(4, 8), slice(24, 28),
                                                                                     slice(26, 32))

    def rhythm_to_six(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(2, 4),
                                                                                 slice(4, 8), slice(6, 8),
                                                                                 slice(16, 20), slice(18, 20),
                                                                                 slice(28, 32), slice(30, 32))

    def rhythm_to_seven(self):
        if self.meter.subdivisions == [2, 2, 3]:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 8), slice(0, 4),
                                                                                     slice(2, 4), slice(24, 32),
                                                                                     slice(28, 32), slice(30, 32))
        elif self.meter.subdivisions == [2, 3, 2]:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(16, 20), slice(16, 20),
                                                                                     slice(18, 20), slice(28, 32))
        else:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(16, 20), slice(18, 20),
                                                                                     slice(24, 32))

    def rhythm_to_nine(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(2, 4),
                                                                                 slice(4, 8), slice(6, 8),
                                                                                 slice(28, 32), slice(30, 32))

    def rhythm_to_twelve(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(16, 20), slice(18, 20),
                                                                                 slice(16, 20), slice(18, 20),
                                                                                 slice(12, 16), slice(18, 20),
                                                                                 slice(28, 32), slice(30, 32))


class RandomRhythms(RhythmSection):
    def __init__(self, meter):
        super().__init__(meter)
        self.midi_notes = [midi_note for midi_note in range(60, 80)]
        self.midi_note_duration_arrays = [[random.uniform(0.1, 5) for _ in range(24)] for
                                          midi_note in range(len(self.midi_notes))]


class PolyRhythms(RhythmSection):
    def __init__(self, meter, number_notes=6):
        super().__init__(meter)
        self.midi_notes = random.sample([midi_note for midi_note in range(60, 80)], number_notes)
        self.midi_note_duration_arrays = [subdivide_meter_into_polyrhythm(meter.num_beats, random.randint(1, 13))
                                          for _ in range(len(self.midi_notes))]

    def transform_rhythm_to_meter(self, meter):
        self.meter = meter
        self.midi_note_duration_arrays = [subdivide_meter_into_polyrhythm(meter.num_beats, random.randint(1, 13))
                                          for _ in range(len(self.midi_notes))]

class IntroductionRhythms(RhythmSection):
    def __init__(self, meter):
        super().__init__(meter)
        self.midi_notes = [88]
        self.midi_note_duration_arrays = [1, 1, 1, 1]

    def rhythm_to_duple(self):
        self.midi_note_duration_arrays = nr(2)

    def rhythm_to_triple(self):
        self.midi_note_duration_arrays = nr(3)

    def rhythm_to_four(self):
        self.midi_note_duration_arrays = nr(4)

    def rhythm_to_five(self):
        self.midi_note_duration_arrays = nr(5)

    def rhythm_to_six(self):
        self.midi_note_duration_arrays = nr(6)

    def rhythm_to_seven(self):
        self.midi_note_duration_arrays = nr(7)

    def rhythm_to_nine(self):
        self.midi_note_duration_arrays = nr(9)

    def rhythm_to_twelve(self):
        self.midi_note_duration_arrays = nr(12)


if __name__ == "__main__":
    from pythonosc import udp_client

    sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
    meter = SimpleDuple(4)
    duplemeter = SimpleDuple(2)
    triplemeter = SimpleTriple()
    threetwo = ComplexMeter(5, [3, 1, 1, 2, 1], [3, 2])
    twothree = ComplexMeter(5, [3, 1, 2, 1, 1], [2, 3])
    twotwothree = ComplexMeter(7, [3, 1, 2, 1, 2, 1, 1], [2, 2, 3])
    twothreetwo = ComplexMeter(7, [3, 1, 2, 1, 1, 2, 1], [2, 3, 2])
    threetwotwo = ComplexMeter(7, [3, 1, 1, 2, 1, 2, 1], [3, 2, 2])
    six = CompoundMeter(6, [3, 1, 1, 2, 1, 1], [3, 3])
    nine = CompoundMeter(9, [3, 1, 1, 2, 1, 1, 2, 1, 1], [3, 3, 3])
    twelve = CompoundMeter(12, [3, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1], [3, 3, 3, 3])
    bb = BreakBeat(meter)
    bb2beats = BreakBeat(duplemeter)
    bb3beats = BreakBeat(triplemeter)
    bbtwothree = BreakBeat(twothree)
    bbthreetwo = BreakBeat(threetwo)
    bbsix = BreakBeat(six)
    bbtwotwothree = BreakBeat(twotwothree)
    bbtwothreetwo = BreakBeat(twothreetwo)
    bbthreetwotwo = BreakBeat(threetwotwo)
    bbnine = BreakBeat(nine)
    bbtwelve = BreakBeat(twelve)

    cc = CompoundSix(six)
    cc2 = CompoundSix(duplemeter)
    cc3 = CompoundSix(triplemeter)
    cc4 = CompoundSix(meter)
    cc23 = CompoundSix(twothree)
    cc32 = CompoundSix(threetwo)
    cc223 = CompoundSix(twotwothree)
    cc232 = CompoundSix(twothreetwo)
    cc322 = CompoundSix(threetwotwo)
    cc9 = CompoundSix(nine)
    cc12 = CompoundSix(twelve)
    tf32 = TakeFive(threetwo)
    tf2 = TakeFive(duplemeter)
    tf3 = TakeFive(triplemeter)
    tf4 = TakeFive(meter)
    tf23 = TakeFive(twothree)
    tf6 = TakeFive(six)
    tf223 = TakeFive(twotwothree)
    tf232 = TakeFive(twothreetwo)
    tf322 = TakeFive(threetwotwo)

    ff = FourOnTheFloor(meter)
    ff3 = FourOnTheFloor(triplemeter)
    ff23 = FourOnTheFloor(twothree)
    ff32 = FourOnTheFloor(threetwo)
    ff6 = FourOnTheFloor(six)
    ff223 = FourOnTheFloor(twotwothree)
    ff232 = FourOnTheFloor(twothreetwo)
    ff322 = FourOnTheFloor(threetwotwo)
    ff9 = FourOnTheFloor(nine)
    ff12 = FourOnTheFloor(twelve)

    pr = PolyRhythms(meter)
    pr2 = PolyRhythms(duplemeter)
    pr3 = PolyRhythms(triplemeter)
    pr23 = PolyRhythms(twothree)
    pr6 = PolyRhythms(six)
    pr7 = PolyRhythms(twothreetwo)
    pr9 = PolyRhythms(nine)
    pr12 = PolyRhythms(twelve)

