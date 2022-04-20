from Classes.meter import SimpleDuple
from Classes.meter import SimpleTriple
from Classes.meter import ComplexMeter
from Classes.meter import CompoundMeter
from Classes.meter import Meter
from itertools import chain
from typing import Union
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


def subdivide_meter_into_polyrhythm(num_beats: Union[int, float], subdivided_by: int):
    """
    Helper function to divide input n number of beats by input var subdivided_by and give back subdivided_by
    number of note durations.
    :param num_beats: int || float
    :param subdivided_by: int
    :return: list
    """
    return [num_beats * 0.25 * 4 / subdivided_by for _ in range(subdivided_by)]


class RhythmSection:
    """
    RhythmSection superclass. Serves as a template for other RhythmSection subclasses.
    """
    def __init__(self, meter: Meter, midi_note_arrays: Union[None, list] = None,
                 midi_note_duration_arrays: Union[None, list] = None):
        """
        Initialization for RhythmSection class. midi_note_arrays and midi_note_duration_arrays can be either None - in
        which case the RhythmSection subclass will generate the data for each variable based on default data. Otherwise
        will use the input data. Both midi_note_arrays and midi_note_duration_arrays should be 2d lists.
        :param meter: Meter
        :param midi_note_arrays: list of lists - must be a 2d list
        :param midi_note_duration_arrays: list - must be a 2d list
        """
        self.meter = meter
        self.midi_notes = midi_note_arrays
        self.midi_note_duration_arrays = midi_note_duration_arrays

    def transform_rhythm_to_meter(self):
        """
        A logical operator template for transforming RhythmSection subclasses according to the logic of the rhythmic
        substrata via slicing defined in each rhythm_to_METER() call.
        :return: None
        """
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
        """
        Template function
        :return: None
        """
        pass

    def rhythm_to_triple(self):
        """
        Template function
        :return: None
        """
        pass

    def rhythm_to_four(self):
        """
        Template function
        :return: None
        """
        pass

    def rhythm_to_five(self):
        """
        Template function
        :return: None
        """
        pass

    def rhythm_to_six(self):
        """
        Template function
        :return: None
        """
        pass

    def rhythm_to_seven(self):
        """
        Template function
        :return: None
        """
        pass

    def rhythm_to_nine(self):
        """
        Template function
        :return: None
        """
        pass

    def rhythm_to_twelve(self):
        """
        Template function
        :return: None
        """
        pass

    def flatten(t):
        """
        Helper function to flatten a 2d list into a 1d list.
        :return:
        """
        return [item for sublist in t for item in sublist]

    def build_new_midi_note_duration_array(self, *slices: slice):
        """
        Abstracted helper function that uses passed in slices to build a new list of midi note durations. Used
        to transform the rhythm information from one meter into another.
        :param slices: slice
        :return: list
        """
        new_midi_note_durations_array = []
        for array in self.midi_note_duration_arrays:
            new_array = []
            for sl in slices:
                new_array = new_array + array[sl]
            new_midi_note_durations_array.append(new_array)
        return new_midi_note_durations_array


class BreakBeat(RhythmSection):
    """
    BreakBeat rhythm section class. Contains two options. A more 'classic' break beat inspired by old-school disco and
    mo-town, and a more modern, 'housier' version. All hail Gregory Coleman of the Winstons who never got the
    recognition he deserved for inspiring a whole genre of beat-based sampling.
    """
    def __init__(self, meter: Meter, option: int = 2):
        """
        Initialization for BreakBeat class. Option call selects the kind of breakbeat. Init loads up the data, and
        transforms it to the given meter.
        :param meter: Meter
        :param option: int
        """
        # TODO: clean up midi_note_duration_arrays here using rr() and nr() calls
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
        """
        Transforms the meter and duration data from whatever its original meter is to a duple meter.
        :return: None
        """
        # TODO: use self.build_new_midi_note_duration_array with slices for cleaner, more maintainable code.
        new_midi_note_durations_array = []
        for array in self.midi_note_duration_arrays:
            new_array = array[0:8] + array[16:24] + array[32:40] + array[56:64]
            new_midi_note_durations_array.append(new_array)
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_triple(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a triple meter.
        :return: None
        """
        new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 12), slice(16, 28),
                                                                                slice(0, 12), slice(16, 28))
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_five(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a complex/asymmetrical 5 meter.
        :return: None
        """
        if self.meter.subdivisions == [2, 3]:
            new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 4), slice(16, 22),
                                                                                    slice(0, 4), slice(16, 22))
        else:
            new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 6), slice(20, 24),
                                                                                    slice(0, 6), slice(60, 64))
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_six(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 6 meter.
        :return: None
        """
        new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 6), slice(0, 6),
                                                                                slice(6, 12), slice(0, 6))
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_seven(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a complex/asymmetrical 7 meter.
        :return: None
        """
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
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 9 meter.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(6, 12), slice(0, 6), slice(0, 6))

    def rhythm_to_twelve(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 12 meter.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(6, 12), slice(0, 6),
                                                                                 slice(0, 6), slice(0, 6))


class CompoundSix(RhythmSection):
    """
    CompoundSix rhythm section. Kind of like the kit part to In the Still of the Nite by The Five Satins, or Rihanna's
    Love on the Brain. Kick on one, hi-hat or snare on 4 (2 of the compound big beats).
    """
    def __init__(self, meter: Meter):
        """
        Initialization for CompoundSix class.
        :param meter: Meter
        """
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
        """
        Transforms the meter and duration data from whatever its original meter is to two.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 10),
                                                                                 slice(36, 37), slice(41, 48))

    def rhythm_to_triple(self):
        """
        Transforms the meter and duration data from whatever its original meter is to three.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 3), slice(5, 9), slice(5, 10),
                                                                                 slice(0, 3), slice(5, 9),
                                                                                 slice(41, 44),
                                                                                 slice(2, 4))

    def rhythm_to_four(self):
        """
        Transforms the meter and duration data from whatever its original meter is to four.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 10), slice(0, 4),
                                                                                 slice(6, 10), slice(0, 4),
                                                                                 slice(6, 10),
                                                                                 slice(36, 37), slice(41, 48))

    def rhythm_to_five(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a complex/asymmetrical 5 meter.
        :return: None
        """
        if self.meter.subdivisions == [2, 3]:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 3), slice(5, 12),
                                                                                     slice(0, 3), slice(17, 24))
        else:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 10), slice(0, 8),
                                                                                     slice(22, 24))

    def rhythm_to_seven(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a complex/asymmetrical 7 meter.
        :return: None
        """
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
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 9 meter.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 11), slice(5, 12),
                                                                                 slice(0, 11), slice(41, 48))

    def rhythm_to_twelve(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 12 meter.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 11), slice(5, 11),
                                                                                 slice(17, 24), slice(0, 11),
                                                                                 slice(5, 11), slice(41, 48))


class TakeFive(RhythmSection):
    """
    TakeFive rhythm section class. A rhythm section that imitates Brubeck's Take Five. Not a transcription, but occupies
    the same timbral space on the kit, and is written originally in 5. Has some of the lilting swing of the Brubeck
    as well.
    """
    def __init__(self, meter: Meter):
        """
        Initialization for TakeFive class.
        :param meter: Meter
        """
        super().__init__(meter)
        self.midi_notes = [midi_note for midi_note in range(48, 53)]
        self.midi_note_duration_arrays = [
            [0.25] + rr(9) + [0.25] + rr(5) + [0.25] + rr(3) + [0.25] + rr(9) + [0.25] + rr(5) + [0.25] + rr(3),
            [0.25] + rr(5) + [0.25, '/r', 0.25, '/r', 0.25] + rr(5) + [0.25, '/r', 0.25, '/r', 0.25] + rr(5) +
            [0.25, '/r', 0.25, '/r', 0.25] + rr(5) + [0.25, '/r', 0.25, '/r'],  rr(2) + [0.25, '/r', 0.25, '/r',
            '/r', 0.25] + rr(4) + [0.25, '/r', 0.25, '/r', '/r', 0.25] + rr(4) + [0.25, '/r',  0.25, '/r', '/r', 0.25]
            + rr(4) + [0.25, '/r', 0.25, '/r', '/r', 0.25] + rr(2), rr(6) + [0.25] + rr(11) + [0.25, 0.25] + rr(2) +
            [0.25, 0.25] + rr(2) + [0.25, '/r', 0.25, 0.25, '/r'] + nr(5) + rr(2) + nr(2), rr(10) + [0.25] + rr(19) +
            [0.25] + rr(5) + [0.25, '/r', 0.25, '/r']
        ]
        self.transform_rhythm_to_meter()

    def rhythm_to_duple(self):
        """
        Transforms the meter and duration data from whatever its original meter is to two.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 10),
                                                                                 slice(30, 34), slice(36, 40))

    def rhythm_to_triple(self):
        """
        Transforms the meter and duration data from whatever its original meter is to three.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 10),
                                                                                 slice(6, 10), slice(30, 34),
                                                                                 slice(36, 40), slice(36, 40))

    def rhythm_to_four(self):
        """
        Transforms the meter and duration data from whatever its original meter is to four.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(2, 6), slice(6, 10),
                                                                                 slice(2, 6), slice(20, 28),
                                                                                 slice(32, 40))

    def rhythm_to_five(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a complex/asymmetrical 5 meter.
        Passes if the meter subdivisions are 3, 2 like the originally composed segment.
        :return: None
        """
        if self.meter.subdivisions == [3, 2]:
            pass
        else:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(16, 20), slice(6, 10),
                                                                                     slice(8, 10),
                                                                                     slice(36, 40), slice(30, 36))

    def rhythm_to_six(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 6 meter.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 6), slice(6, 10),
                                                                                 slice(8, 10),
                                                                                 slice(20, 26), slice(36, 40),
                                                                                 slice(38, 40))

    def rhythm_to_seven(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a complex/asymmetrical 7 meter.
        :return: None
        """
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
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 9 meter.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 6), slice(6, 10),
                                                                                 slice(8, 10), slice(6, 10),
                                                                                 slice(8, 10), slice(20, 26),
                                                                                 slice(6, 10), slice(8, 10),
                                                                                 slice(36, 40), slice(38, 40))

    def rhythm_to_twelve(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 12 meter.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 6), slice(6, 10),
                                                                                 slice(8, 10), slice(6, 10),
                                                                                 slice(8, 10), slice(6, 10),
                                                                                 slice(8, 10), slice(20, 26),
                                                                                 slice(6, 10), slice(8, 10),
                                                                                 slice(6, 10), slice(8, 10),
                                                                                 slice(36, 40), slice(38, 40))


class FourOnTheFloor(RhythmSection):
    """
    FourOnTheFloor rhythm section class. Imitates up-tempo big-band/lindy-hop four on the floor rather than disco/edm.
    """
    def __init__(self, meter: Meter):
        """
        Initialization for FourOnTheFloor class.
        :param meter: Meter
        """
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
        """
        Transforms the meter and duration data from whatever its original meter is to three.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(4, 8), slice(10, 12),
                                                                                 slice(16, 20), slice(18, 20),
                                                                                 slice(24, 28), slice(26, 28),
                                                                                 slice(28, 32), slice(30, 32))

    def rhythm_to_five(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a complex/asymmetrical 5 meter.
        Passes if the meter subdivisions are 3, 2 like the originally composed segment.
        :return: None
        """
        if self.meter.subdivisions == [2, 3]:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 8), slice(6, 8),
                                                                                     slice(24, 32), slice(30, 32))
        else:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(2, 4),
                                                                                     slice(4, 8), slice(24, 28),
                                                                                     slice(26, 32))

    def rhythm_to_six(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 6 meter.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(2, 4),
                                                                                 slice(4, 8), slice(6, 8),
                                                                                 slice(16, 20), slice(18, 20),
                                                                                 slice(28, 32), slice(30, 32))

    def rhythm_to_seven(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a complex/asymmetrical 7 meter.
        :return: None
        """
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
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 9 meter.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(2, 4),
                                                                                 slice(4, 8), slice(6, 8),
                                                                                 slice(28, 32), slice(30, 32))

    def rhythm_to_twelve(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 12 meter.
        :return: None
        """
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(16, 20), slice(18, 20),
                                                                                 slice(16, 20), slice(18, 20),
                                                                                 slice(12, 16), slice(18, 20),
                                                                                 slice(28, 32), slice(30, 32))


class RandomRhythms(RhythmSection):
    """
    RandomRhythms rhythm section class. Generates rhythms randomly for playback.
    """
    def __init__(self, meter: Meter):
        """
        Initialization for RandomRhythms class
        :param meter: Meter
        """
        super().__init__(meter)
        self.midi_notes = [midi_note for midi_note in range(60, 80)]
        self.midi_note_duration_arrays = [[random.uniform(0.1, 5) for _ in range(24)] for
                                          midi_note in range(len(self.midi_notes))]


class PolyRhythms(RhythmSection):
    """
    PolyRhythms rhythm section class. Generates polyrhythms based on n number of input notes.
    """
    def __init__(self, meter: Meter, number_notes: int = 6):
        """
        Initialization for PolyRhythms class.
        :param meter: Meter
        :param number_notes: int number of midi notes (or different percussion instruments to generate)
        """
        # TODO: Fix naming of number_notes to be more descriptive.
        super().__init__(meter)
        self.midi_notes = random.sample([midi_note for midi_note in range(60, 80)], number_notes)
        self.midi_note_duration_arrays = [subdivide_meter_into_polyrhythm(meter.num_beats, random.randint(1, 13))
                                          for _ in range(len(self.midi_notes))]

    def transform_rhythm_to_meter(self, meter: Meter):
        """
        Generates new polyrhythms to conform to the new metrical unit.
        :param meter: Meter
        :return: None
        """
        self.meter = meter
        self.midi_note_duration_arrays = [subdivide_meter_into_polyrhythm(meter.num_beats, random.randint(1, 13))
                                          for _ in range(len(self.midi_notes))]


class IntroductionRhythms(RhythmSection):
    """
    IntroductionRhythms class. Generates a simple on beat patter for every quarter note. A little House-y
    """
    def __init__(self, meter: Meter):
        """
        Initialization for IntroductionRhythms
        :param meter: Meter
        """
        super().__init__(meter)
        self.midi_notes = [88]
        self.midi_note_duration_arrays = [
            [1, 1, 1, 1]
        ]

    def rhythm_to_duple(self):
        """
        Transforms the meter and duration data from whatever its original meter is to two.
        :return: None
        """
        self.midi_note_duration_arrays = nr(2)

    def rhythm_to_triple(self):
        """
        Transforms the meter and duration data from whatever its original meter is to three.
        :return: None
        """
        self.midi_note_duration_arrays = nr(3)

    def rhythm_to_four(self):
        """
        Transforms the meter and duration data from whatever its original meter is to four.
        :return: None
        """
        self.midi_note_duration_arrays = nr(4)

    def rhythm_to_five(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a complex/asymmetrical 5 meter.
        :return: None
        """
        self.midi_note_duration_arrays = nr(5)

    def rhythm_to_six(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 6 meter.
        :return: None
        """
        self.midi_note_duration_arrays = nr(6)

    def rhythm_to_seven(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a complex/asymmetrical 7 meter.
        :return: None
        """
        self.midi_note_duration_arrays = nr(7)

    def rhythm_to_nine(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 9 meter.
        :return: None
        """
        self.midi_note_duration_arrays = nr(9)

    def rhythm_to_twelve(self):
        """
        Transforms the meter and duration data from whatever its original meter is to a compound 12 meter.
        :return: None
        """
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

    print(pr12.meter.num_beats)