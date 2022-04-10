from Classes.harmonic_rhythm import HarmonicRhythm
from Classes.chord_progression import ChordProgression
from Classes.scale import Scale
from Classes.meter import *
from Classes.note import Note
from Classes.chord import Chord
import random


class Melody:
    def __init__(self, harmonic_rhythm, scale):
        self.harmonic_rhythm = harmonic_rhythm
        self.scale = scale

    @staticmethod
    def build_rest(duration=1):
        """
        Helper function that builds a rest out of a given duration.
        :param duration: Integer or float
        :return: String of '/r' key + a cocatenated duration
        """
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

    def appoggiatura(self, chord_and_duration_block):
        notes = []
        durations = []
        # get a chord tone
        chord_tone = random.choice(chord_and_duration_block[0].notes)
        # appoggiatura is an accented neighbor
        appoggiatura_note = self.get_closest_scale_tone_to_chord_tone(chord_tone)
        while appoggiatura_note == chord_tone:
            appoggiatura_note = self.get_random_neighbor(chord_tone)
        notes.append(appoggiatura_note)
        # # appoggiatura resolves
        # notes.append(self.get_closest_scale_tone_to_chord_tone(chord_tone))
        # it must resolve to a chord tone
        notes.append(chord_tone)
        # duration of the appoggiatura is usually less than the length of the harmonic rhythm unit
        appoggiatura_duration = self.get_random_duration()
        while appoggiatura_duration >= chord_and_duration_block[1]:
            appoggiatura_duration = self.get_random_duration()
        durations.append(appoggiatura_duration)
        # duration of resolution note fills rest of duration
        durations.append(chord_and_duration_block[1]-appoggiatura_duration)
        return notes, durations

    def suspension(self, current_duration_left, current_chord_and_duration_block, next_chord_and_duration_block):
        notes = []
        durations = []
        # suspension holds note over a harmonic change
        # it usually resolves to a chord tone (eventually)
        # get next chord tone to resolve into
        next_chord_tone = random.choice(next_chord_and_duration_block[0].notes)
        # if the chords are the same, suspension note is a random neighbor to next chord tone
        # (more like a neighbor note). Else suspension is closest scale tone to the selected next chord tone
        if current_chord_and_duration_block[0] == next_chord_and_duration_block[0]:
            suspension_note = self.get_random_neighbor(next_chord_tone)
        else:
            suspension_note = self.get_closest_scale_tone_to_chord_tone(next_chord_tone)
        # while suspension is same as the next chord tone, make a new next chord tone and get another suspension.
        # solve edge cases where suspension is same as next chord
        while suspension_note == next_chord_tone:
            next_chord_tone = random.choice(next_chord_and_duration_block[0].notes)
            suspension_note = self.get_random_neighbor(next_chord_tone)
        # add suspension, resolution to notes
        notes += [suspension_note, next_chord_tone]
        # add current_duration_left and random duration less than duration of next_chord_duration
        sus_part_2_duration = self.get_random_duration()
        # hardcoded 1.5 duration to remove the possibility that the next while loop could get stuck in infinite loop
        while sus_part_2_duration >= 1.5:
            sus_part_2_duration = self.get_random_duration()
        suspension_duration = current_duration_left + sus_part_2_duration
        # resolution duration is some remaining length of the
        resolution_duration = self.get_random_duration()
        while resolution_duration >= next_chord_and_duration_block[1] - sus_part_2_duration:
            resolution_duration = self.get_random_duration()
        durations += [suspension_duration, resolution_duration]
        # get remaining duration in next chord_and_duration_block for constructing other notes
        remaining_duration = (current_chord_and_duration_block[1] + next_chord_and_duration_block[1]) - sum(durations)
        return notes, durations, remaining_duration

    def upper_mordent(self):
        pass

    def set_scale(self, scale: Scale):
        """
        Setter function to change the scale as needed.
        :param scale: Scale object
        :return: None
        """
        self.scale = scale

    def get_closest_scale_tone_to_chord_tone(self, chord_note: Note):
        closest_tone = self.scale.notes[0]
        for tone in self.scale.notes:
            if abs(chord_note.midi_note_number - tone.midi_note_number) < (chord_note.midi_note_number - closest_tone.midi_note_number):
                closest_tone = tone
        return closest_tone

    def scalar_upper_neighbor(self, note: Note):
        note_index = self.scale.notes.index(note)
        return self.scale.notes[(note_index + 1) % len(self.scale.notes)]

    def scalar_lower_neightbor(self, note: Note):
        note_index = self.scale.notes.index(note)
        return self.scale.notes[(note_index - 1) % len(self.scale.notes)]

    def chromatic_upper_neighbor(self, note: Note):
        return Note(note.midi_note_number + 1)

    def chromatic_lower_neighbor(self, note: Note):
        return Note(note.midi_note_number - 1)

    def get_random_neighbor(self, note: Note):
        return random.choice([
            self.scalar_upper_neighbor,
            self.scalar_lower_neightbor,
            self.chromatic_upper_neighbor,
            self.chromatic_lower_neighbor
        ])(note)

    def get_random_duration(self):
        return random.choice([0.25, 1/3, 0.5, 2/3, 0.75, 1, 1.25, 1.5, 1.75, 2])

    def get_random_chord_tone(self, chord: Chord):
        return random.choice(chord.notes)

    def is_tuplet(self, duration):
        if duration == 1/3:
            return True
        else:
            return False


class SustainedMelody(Melody):
    def __init__(self, harmonic_rhythm, scale):
        super().__init__(harmonic_rhythm, scale)


if __name__ == "__main__":
    meter = ComplexMeter(7, [3, 1, 2, 1, 1, 2, 1], [2, 3, 2])
    duple = SimpleDuple(4)
    scale = Scale(Note(0), Note(2), Note(4), Note(5), Note(7), Note(9), Note(11))
    c_major = Chord(Note(0), Note(4), Note(7))
    CM7 = Chord(Note(0), Note(4), Note(7), Note(11))
    Cmm7 = Chord(Note(0), Note(3), Note(7), Note(10))
    a = Chord(Note(9), Note(0), Note(4))
    G7 = Chord(Note(7), Note(11), Note(14), Note(17))
    e = Chord(Note(4), Note(7), Note(11))
    b = Chord(Note(11), Note(2), Note(5))
    harmony = ChordProgression([c_major, G7, a, c_major, a, G7, e])
    hr = HarmonicRhythm(duple, harmony)
    melody = Melody(hr, scale)
    # print(melody.get_closest_scale_tone_to_chord_tone(Note(8)))
    print(melody.appoggiatura((b, 2)))
    # for i in range(100):
    #     print(melody.suspension(1, (b, 2), (a, 2)))