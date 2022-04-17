import numpy as np

from Classes.meter import *
from Classes.chord_progression import ChordProgression
from Classes.chord import Chord
from Classes.note import Note


def split_off_duration(durations, index, amount=1):
    durations[index] = durations[index] - amount
    durations.insert(index+1, amount)
    return durations


def recursive_split_meter(meter_subdivision, n_splits, n_recusions=0):
    if all(i == 1 for i in meter_subdivision):
        return [1 for _ in range(sum(meter_subdivision))]
    elif n_recusions > n_splits >= 0:
        return [sum(meter_subdivision)]
    elif n_recusions == n_splits:
        return meter_subdivision
    else:
        greatest_index = 0
        for count, value in enumerate(meter_subdivision):
            if value >= meter_subdivision[greatest_index]:
                greatest_index = count
        meter_subdivision_copy = meter_subdivision[:]
        new_meter_subdivision = split_off_duration(meter_subdivision_copy, greatest_index)
        # print(new_meter_subdivision)
        return recursive_split_meter(new_meter_subdivision, n_splits, n_recusions + 1)


def chords_in_bar_equal_subdivisions(subdivisions):
    return subdivisions


def chords_in_bar_less_than_subdivisions(num_chords, subdivisions):
    return [sum(subdivisions[:len(subdivisions)-num_chords+1])] + subdivisions[len(subdivisions)-num_chords+1:]


def chords_in_bar_greater_than_subdivisions(num_chords, subdivisions):
    return recursive_split_meter(subdivisions, num_chords)


def generate_beat_subdivisions_for_chords(num_chords, subdivisions):
    if num_chords == len(subdivisions):
        return chords_in_bar_equal_subdivisions(subdivisions)
    elif num_chords < len(subdivisions):
        return chords_in_bar_less_than_subdivisions(num_chords, subdivisions)
    else:
        return chords_in_bar_greater_than_subdivisions(num_chords, subdivisions)


def fill_chords_to_number_of_bars(progression, num_bars):
    res = progression.chords
    while len(res) < num_bars:
        for chord in range(num_bars-len(progression.chords)):
            res = res[:chord] + [progression.chords[chord]] + res[chord:]
            if len(progression.chords) >= num_bars:
                break
    return res


class HarmonicRhythm:
    def __init__(self, meter, progression, num_bars=4, hr_durations=None):
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
        # split progression across num_bars number of bars
        chords = np.array_split(self.progression.chords, self.num_bars)
        # split the remaining progression amongst by strong metrical subdivisions within the bar
        res = []
        for i in chords:
            chords_subdivided_into_bar = i.tolist()
            chords_durations = generate_beat_subdivisions_for_chords(len(chords_subdivided_into_bar), self.meter.subdivisions)
            res.append(chords_durations)
        return res

    def get_zipped_hr_chords_and_durations(self):
        return [i for i in zip(self.progression.chords, self.flattened_hr_durations)]

    def get_chords_and_durations(self):
        return [self.progression.chords, self.flattened_hr_durations]

    def transpose_return_new(self, num):
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


