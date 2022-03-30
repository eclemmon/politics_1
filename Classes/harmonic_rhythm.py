from Classes.meter import *
from Classes.harmony import Harmony
from Classes.chord import Chord
from Classes.note import Note


def split_off_duration(durations, index, amount=1):
    durations[index] = durations[index] - amount
    durations.insert(index+1, amount)
    return durations


def recursive_split_meter(meter_subdivision, n_splits, n_recusions=0):
    if all(i == 1 for i in meter_subdivision):
        return [1 for _ in range(sum(meter_subdivision))]
    elif n_recusions == n_splits:
        return meter_subdivision
    else:
        greatest_index = 0
        for count, value in enumerate(meter_subdivision):
            if value >= meter_subdivision[greatest_index]:
                greatest_index = count
        new_meter_subdivision = split_off_duration(meter_subdivision, greatest_index)
        return recursive_split_meter(new_meter_subdivision, n_splits, n_recusions + 1)


class HarmonicRhythm:
    def __init__(self, meter, harmony, num_bars=4):
        self.meter = meter
        self.harmony = harmony
        self.num_bars = num_bars
        self.hr_durations = self.get_hr_durations()

    def get_hr_durations(self):
        return recursive_split_meter(self.meter.subdivisions, len(self.harmony.chords) - len(self.meter.subdivisions))

    def get_zipped_hr_chords_and_durations(self):
        return [i for i in zip(self.harmony.chords, self.hr_durations)]

    def get_chords_and_durations(self):
        return [self.harmony.chords, self.hr_durations]


if __name__ == "__main__":
    meter = SimpleDuple(num_beats=4)
    c_major = Chord(Note(0), Note(4), Note(7))
    CM7 = Chord(Note(0), Note(4), Note(7), Note(11))
    Cmm7 = Chord(Note(0), Note(3), Note(7), Note(10))
    G7 = Chord(Note(7), Note(11), Note(14), Note(17))
    harmony = Harmony([c_major, CM7, Cmm7, G7])
    hrhythm = HarmonicRhythm(meter, harmony)
    print(hrhythm.get_zipped_hr_chords_and_durations())
    print(hrhythm.get_chords_and_durations())

    five = ComplexMeter(5, [3, 1, 2, 1, 1], [2, 3])
    fhrhythm = HarmonicRhythm(five, harmony)
    print(fhrhythm.get_zipped_hr_chords_and_durations())
    print(fhrhythm.get_chords_and_durations())
    # print(hrhythm.build_phrase_accents_one())
    # print(hrhythm.base_case_one_chord())
    # print(hrhythm.base_case_two_chords())