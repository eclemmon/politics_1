from Classes.harmonic_rhythm import HarmonicRhythm
from Classes.chord_progression import ChordProgression
from Classes.scale import Scale
from Classes.meter import *
from Classes.note import Note
import random

from Classes.chord import Chord


def subdivide_meter_into_polyrhythm(num_beats, subdivided_by):
    return [num_beats * 0.25 * 4 / subdivided_by for _ in range(subdivided_by)]


class Bass:
    def __init__(self, harmonic_rhythm, scale):
        self.harmonic_rhythm = harmonic_rhythm
        self.scale = scale
        self.notes_and_durations = self.build_notes_and_durations()

    def get_next_note(self):
        pass

    def build_bass_line(self):
        pass

    @staticmethod
    def build_rest(duration=1):
        return '/r' + str(duration)

    @staticmethod
    def is_rest(probability=0.50):
        return random.random() < probability

    def make_note_or_rest(self, duration=1, probability=0.50):
        if self.is_rest(probability):
            return self.build_rest(duration)
        else:
            return duration

    def build_notes_and_durations(self):
        pass


class AlbertiBass(Bass):
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale, note_duration=0.25):
        self.note_duration = note_duration
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        notes = []
        durations = []
        beat_in_meter_count = 0
        for count, duration in enumerate(self.harmonic_rhythm.flattened_hr_durations):
            for num_beats in range(duration):
                beat_in_meter = beat_in_meter_count % self.harmonic_rhythm.meter.num_beats
                chord = self.harmonic_rhythm.progression.chords[count]
                accent_weight = self.harmonic_rhythm.meter.accent_weights[beat_in_meter]
                notes.append(self.get_next_note(chord, accent_weight, beat_in_meter))
                durations.append(self.note_duration)
                beat_in_meter_count += 1
        return [notes, durations]

    def get_next_note(self, chord: Chord, accent_weight, beat_in_meter):
        if accent_weight == 3:
            try:
                return chord.get_bass_note()
            except Exception as e:
                print("Had an issue getting the bass note of this chord: ", e)
        else:
            return self.get_next_upper_alberti_note(chord, beat_in_meter=beat_in_meter)

    def get_next_upper_alberti_note(self, chord: Chord, beat_in_meter):
        if len(chord.notes) == 1:
            return chord.notes[0]
        elif len(chord.notes) == 2:
            sl = [0, 1][beat_in_meter % 2]
            return chord.notes[sl]
        elif len(chord.notes) == 3:
            sl = [1, 2][beat_in_meter % 2]
            return chord.notes[sl]
        elif len(chord.notes) == 4:
            sl = [1, 3, 1, 3][beat_in_meter % 4]
            return chord.notes[sl]
        else:
            sl = [note_index for note_index in range(len(chord.notes), 0)][beat_in_meter % len(chord.notes)]
            return chord.notes[sl]


class SustainedBass(Bass):
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        notes = []
        durations = []

        for i, chord in enumerate(self.harmonic_rhythm.progression.chords):
            notes.append(self.harmonic_rhythm.progression.chords[i].get_bass_note())
            durations.append(self.harmonic_rhythm.flattened_hr_durations[i])
        return [notes, durations]


class RandomBass(Bass):
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        notes = []
        durations = []

        for chord_and_dur_block in self.harmonic_rhythm.get_zipped_hr_chords_and_durations():
            duration_left = chord_and_dur_block[1]
            while duration_left > 0:
                duration = random.uniform(0.05, duration_left)
                durations.append(self.make_note_or_rest(duration, 0.25))
                duration_left -= duration
                notes.append(chord_and_dur_block[0].get_bass_note())
        return [notes, durations]


class PolyrhythmicBass(Bass):
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        notes = []
        durations = []

        for chord_and_dur_block in self.harmonic_rhythm.get_zipped_hr_chords_and_durations():
            durations += subdivide_meter_into_polyrhythm(chord_and_dur_block[1], random.randint(3, 7))
            notes += [chord_and_dur_block[0].get_bass_note() for _ in range(len(durations))]

        durations = [self.make_note_or_rest(duration) for duration in durations]
        return [notes, durations]


class OnBeatBass(Bass):
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        notes = []
        durations = []

        for chord_and_dur_block in self.harmonic_rhythm.get_zipped_hr_chords_and_durations():
            durations.append(1)
            if chord_and_dur_block[1] - 1 > 0:
                durations.append(self.build_rest(chord_and_dur_block[1] - 1))
            notes.append(chord_and_dur_block[0].get_bass_note())
        return [notes, durations]


class WalkingBass(Bass):
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        super().__init__(harmonic_rhythm, scale)

    def get_shortest_distance_data_chromatic(self, bn1: Note, bn2: Note):
        untransposed = bn2.midi_note_number - bn1.midi_note_number
        transposed = bn1.midi_note_number + 12 - bn2.midi_note_number
        if untransposed <= transposed:
            return {'ascending': True, 'steps': bn2.midi_note_number - bn1.midi_note_number}
        else:
            return {'ascending': False, 'steps': -(bn1.midi_note_number + 12 - bn2.midi_note_number)}

    def get_shortest_distance_data_scalar(self, bn1: Note, bn2: Note):
        index_1 = self.scale.notes.index(bn1)
        index_2 = self.scale.notes.index(bn2)
        untransposed = index_1 - index_2
        transposed = index_1 + len(self.scale.notes) - index_2
        if abs(untransposed) <= abs(transposed):
            return {'ascending': True, 'steps': index_2 - index_1}
        else:
            return {'ascending': False, 'steps': -(index_1 + len(self.scale.notes) - index_2)}

    def step_between_notes_scalar(self, bn1, distance_data):
        current_index = self.scale.notes.index(bn1)
        if distance_data['ascending']:
            return [self.scale.notes[current_index + i] for i in range(0, distance_data['steps'])]
        else:
            return [self.scale.notes[current_index + i] for i in range(0, distance_data['steps'], -1)]

    def step_between_notes_chromatic(self, bn1, distance_data):
        if distance_data['ascending']:
            return [Note(bn1.midi_note_number + i) for i in range(0, distance_data['steps'])]
        else:
            return [Note(bn1.midi_note_number + i) for i in range(0, distance_data['steps'], -1)]

    def build_notes_and_durations(self):
        chords_and_durations = self.harmonic_rhythm.get_zipped_hr_chords_and_durations()

    def step_chromatic_or_scalar(self, probability):
        return random.random() < probability

    def next_beat_fourth_down_tonicization(self, duration, next_note):
        return (next_note - 7, duration)

    def next_beat_leading_tone_tonicization(self, duration, next_note):
        return (next_note - 1, duration)

    def next_beat_chromatic_upper_neighbor_tonicization(self, duration, next_note):
        return (next_note + 1, duration)

    def build_notes_for_current_subdivision(self, current_chord_and_dur_block, next_chord_and_dur_block):
        # choose between scalar and chromatic
        pass


if __name__ == "__main__":
    meter = ComplexMeter(7, [3, 1, 2, 1, 1, 2, 1], [2, 3, 2])
    scale = Scale(Note(0), Note(2), Note(4), Note(5), Note(7), Note(9), Note(11))
    c_major = Chord(Note(0), Note(4), Note(7))
    CM7 = Chord(Note(0), Note(4), Note(7), Note(11))
    Cmm7 = Chord(Note(0), Note(3), Note(7), Note(10))
    a = Chord(Note(9), Note(0), Note(4))
    G7 = Chord(Note(7), Note(11), Note(14), Note(17))
    harmony = ChordProgression([c_major, G7, a, c_major, a, G7])
    hr = HarmonicRhythm(meter, harmony)
    ab = SustainedBass(hr, scale)
    rb = RandomBass(hr, scale)
    pr = PolyrhythmicBass(hr, scale)
    obb = OnBeatBass(hr, scale)
    wb = WalkingBass(hr, scale)
    # print(rb.notes_and_durations)
    # print(pr.notes_and_durations)
    chrom = wb.get_shortest_distance_data_chromatic(c_major.get_bass_note(), a.get_bass_note())
    scalar = wb.get_shortest_distance_data_scalar(c_major.get_bass_note(), a.get_bass_note())
    steps_chrom = wb.step_between_notes_chromatic(c_major.get_bass_note(), chrom)
    print(steps_chrom)
    steps_scalar = wb.step_between_notes_scalar(c_major.get_bass_note(), scalar)
    print(steps_scalar)
    # ab.build_notes_and_durations()
