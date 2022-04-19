import numpy as np

from typing import Union
from Classes.meter import *
from Classes.chord_progression import ChordProgression
from Classes.chord import Chord
from Classes.note import Note


def split_off_duration(durations: list, index: int, amount: int = 1):
    """
    Helper function for taking a duration at index i in a list of durations and splitting off a number of beats
    (amount) and inserting it at index i+1. e.g. [2, 3] --> [1, 1, 3]
    :param durations: list
    :param index: int
    :param amount: int
    :return: list
    """
    durations[index] = durations[index] - amount
    durations.insert(index+1, amount)
    return durations


def recursive_split_meter(meter_subdivision: list, n_splits: int, n_recursions: int = 0):
    """
    Helper function to recursively split a meter into a number of subdivisions. This is to generate a duration value
    associated with a number of n chords. As a minimum, default rule in Cybernetic Republic, the harmonic rhythm
    can only progress at one chord per quarter note value. Therefore, the base case is
    durations = [1 for i beats in a measure].
    > The recursive function can account for different meter subdivisions. So a complex meter of 5, with 3+2 will
    subdivide to [2, 1, 2] then [2, 1, 1, 1], and finally, [1, 1, 1, 1, 1] after 3 recursions before returning the
    base case.
    > If n_recursions is equal to the n_splits, this means that the number of chords is equal to the number of
    subdivisions in the meter passed in. This is normally the target return of this function.
    > If the number of splits is less than the number of recursions while the number of splits is greater than 0,
    then the chord should have a durational value that lasts at least as long as the measure. So 1 chord in a simple
    duple meter 4 beats long will return [4]
    :param meter_subdivision: list of primary meter subdivisions
    :param n_splits: int of number of splits to occur in the meter
    :param n_recursions: int to track the number of recursions executed.
    :return: list
    """
    if all(i == 1 for i in meter_subdivision):
        return [1 for _ in range(sum(meter_subdivision))]
    elif n_recursions > n_splits >= 0:
        return [sum(meter_subdivision)]
    elif n_recursions == n_splits:
        return meter_subdivision
    else:
        greatest_index = 0
        for count, value in enumerate(meter_subdivision):
            if value >= meter_subdivision[greatest_index]:
                greatest_index = count
        # make a copy of the meter subdivision because referenced objects being operated on again is baaaaddd
        meter_subdivision_copy = meter_subdivision[:]
        new_meter_subdivision = split_off_duration(meter_subdivision_copy, greatest_index)
        return recursive_split_meter(new_meter_subdivision, n_splits, n_recursions + 1)


def chords_in_bar_equal_subdivisions(subdivisions: list):
    """
    Optimization helper function to return subdivision immediately without calling recusive_split_meter when n_chords is
    equal to len(subdivisions).
    :param subdivisions: list
    :return: list
    """
    return subdivisions


def chords_in_bar_less_than_subdivisions(num_chords: int, subdivisions: list):
    """
    Logical helper function that adds n subdivisions together based on the number of chords less than len(subdivisions)
    So 2 chords in a compound 9 measure would become [6, 3]
    :param num_chords: int
    :param subdivisions: list
    :return: list
    """
    return [sum(subdivisions[:len(subdivisions)-num_chords+1])] + subdivisions[len(subdivisions)-num_chords+1:]


def chords_in_bar_greater_than_subdivisions(num_chords: int, subdivisions: list):
    """
    Logical helper function that calls recursive split meter to get the subdivisions of the meter whne num_chords is >
    len(subdivisions)
    :param num_chords: int
    :param subdivisions: list
    :return: list
    """
    return recursive_split_meter(subdivisions, num_chords)


def generate_beat_subdivisions_for_chords(num_chords: int, subdivisions: list):
    """
    Logical operator function to return the various subdivision functions contained above in this module.
    :param num_chords: int
    :param subdivisions: list
    :return: list
    """
    if num_chords == len(subdivisions):
        return chords_in_bar_equal_subdivisions(subdivisions)
    elif num_chords < len(subdivisions):
        return chords_in_bar_less_than_subdivisions(num_chords, subdivisions)
    else:
        return chords_in_bar_greater_than_subdivisions(num_chords, subdivisions)


def fill_chords_to_number_of_bars(progression: ChordProgression, num_bars: int):
    """
    Helper function that distributes the chords over n_bars if the number of chords in the progression is less than
    the number of bars. So if the HarmonicRhythm has 4 bars, and the ChordProgression has 3 Chords: CMM7, Dmm7, G7,
    this function will fill out the HarmonicRhythm chord blocks so that the measures are:
    [Bar 1: CMM7]
    [Bar 2: CMM7]
    [Bar 3: Dmm7]
    [Bar 4: G7]
    :param progression: ChordProgression
    :param num_bars: int
    :return: tuple of chords
    """
    res = progression.chords
    while len(res) < num_bars:
        for chord in range(num_bars-len(progression.chords)):
            res = res[:chord] + [progression.chords[chord]] + res[chord:]
            if len(progression.chords) >= num_bars:
                break
    return res


class HarmonicRhythm:
    """
    HarmonicRhythm class for building matched blocks of chords and durations for each chord.
    """
    def __init__(self, meter: Meter, progression: ChordProgression, num_bars: int = 4,
                 hr_durations: Union[list, None] = None):
        """
        Initialization for HarmonicRhythm class.
        :param meter: Meter
        :param progression: ChordProgression
        :param num_bars: int
        :param hr_durations: list || None
        """
        self.meter = meter
        self.progression = progression
        self.num_bars = num_bars
        if len(self.progression.chords) < self.num_bars:
            self.progression = ChordProgression(fill_chords_to_number_of_bars(self.progression, num_bars))

        if hr_durations is None:
            self.hr_durations = self.get_hr_durations()
        else:
            # 2d Array please!
            self.hr_durations = hr_durations
        self.flattened_hr_durations = [item for sublist in self.hr_durations for item in sublist]

    def get_hr_durations(self):
        """
        Constructor for durations in HarmonicRhythm Class. Gets a helping hand from NumPy's array_split.
        :return: list of durations (ints)
        """
        # split progression across num_bars number of bars
        chords = np.array_split(self.progression.chords, self.num_bars)
        # split the remaining progression amongst by strong metrical subdivisions within the bar
        res = []
        for i in chords:
            chords_subdivided_into_bar = i.tolist()
            chords_durations = generate_beat_subdivisions_for_chords(len(chords_subdivided_into_bar),
                                                                     self.meter.subdivisions)
            res.append(chords_durations)
        return res

    def get_zipped_hr_chords_and_durations(self):
        """
        Zips the chords and flattened harmonic rhythm durations into a set of tuples so that chords are attached to
        their respective durations.
        :return: list of tuples
        """
        return [i for i in zip(self.progression.chords, self.flattened_hr_durations)]

    def get_chords_and_durations(self):
        """
        Returns a list of lists. list[0] hold the chords of the progression, list[1] holds the flattened durations
        of the HarmonicRhythm.
        :return: list of lists.
        """
        return [self.progression.chords, self.flattened_hr_durations]

    def transpose_return_new(self, num: int):
        """
        Builds a new HarmonicRhythm object from self with the ChordProgression transposed. Passes in self.hr_durations
        so that reserved durations do not need to be computationally built again.
        :param num: int
        :return: HarmonicRhythm
        """
        return HarmonicRhythm(self.meter, self.progression.transpose_return_new(num), self.num_bars, self.hr_durations)


def build_harmonic_rhythm(meter, chords):
    return HarmonicRhythm(meter, ChordProgression(chords))



if __name__ == "__main__":
    # meter = ComplexMeter(7, [3, 1, 2, 1, 2, 1, 1], [2, 2, 3])
    # meter = CompoundMeter(9, [3,1,1,2,1,1,2,1,1], [3, 3, 3])
    # meter = SimpleDuple(2)
    # meter = CompoundMeter(12, [3, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1], [3,3, 3, 3])
    meter = ComplexMeter(5, [3, 1, 1, 2, 1], [3, 2])
    c_major = Chord(Note(0), Note(4), Note(7))
    CM7 = Chord(Note(0), Note(4), Note(7), Note(11))
    Cmm7 = Chord(Note(0), Note(3), Note(7), Note(10))
    a = Chord(Note(9), Note(0), Note(3))
    G7 = Chord(Note(7), Note(11), Note(14), Note(17))
    long = ChordProgression([c_major, CM7, Cmm7, a, G7, a])
    short = ChordProgression([c_major, CM7, Cmm7])
    medium = ChordProgression([c_major, CM7, Cmm7, a])
    hr = HarmonicRhythm(meter, long)
    # print("long: ", hr.get_chords_and_durations())
    hr = HarmonicRhythm(meter, short)
    # print("short: ", hr.get_chords_and_durations())
    hr = HarmonicRhythm(meter, medium)
    # print("mediusm: ", hr.get_chords_and_durations())
    # print(hrhythm.get_zipped_hr_chords_and_durations())
    # print(hrhythm.get_chords_and_durations())


