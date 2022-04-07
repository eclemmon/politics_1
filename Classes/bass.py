from Classes.harmonic_rhythm import HarmonicRhythm
from Classes.chord_progression import ChordProgression
from Classes.scale import Scale
from Classes.meter import *
from Classes.note import Note
import random

from Classes.chord import Chord


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


class PadsBass(Bass):
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        notes = []
        durations = []
        print(self.harmonic_rhythm.hr_durations)

        for i, chord in enumerate(self.harmonic_rhythm.progression.chords):
            print(i, chord)
            notes.append(self.harmonic_rhythm.progression.chords[i].get_bass_note())
            print(self.harmonic_rhythm.flattened_hr_durations[i])
            durations.append(self.harmonic_rhythm.flattened_hr_durations[i])
        return [notes, durations]

if __name__ == "__main__":
    meter = ComplexMeter(7, [3, 1, 2, 1, 1, 2, 1], [2, 3, 2])
    scale = Scale(Note(0), Note(2), Note(4), Note(5), Note(7), Note(9), Note(11))
    c_major = Chord(Note(0), Note(4), Note(7))
    CM7 = Chord(Note(0), Note(4), Note(7), Note(11))
    Cmm7 = Chord(Note(0), Note(3), Note(7), Note(10))
    a = Chord(Note(9), Note(0), Note(4))
    G7 = Chord(Note(7), Note(11), Note(14), Note(17))
    harmony = ChordProgression([c_major, CM7, Cmm7, G7, a])
    hr = HarmonicRhythm(meter, harmony)
    ab = PadsBass(hr, scale)
    print(ab.notes_and_durations)
    # ab.build_notes_and_durations()


