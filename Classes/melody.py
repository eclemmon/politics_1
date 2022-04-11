from Classes.harmonic_rhythm import HarmonicRhythm
from Classes.chord_progression import ChordProgression
from Classes.scale import Scale
from Classes.meter import *
from Classes.note import Note
from Classes.chord import Chord
import random


class Melody:
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        self.harmonic_rhythm = harmonic_rhythm
        self.scale = scale
        self.notes_and_durations = self.build_notes_and_durations()

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
        """
        Helper function that determines whether a rest is constructed based on a passed in probability.
        :param probability: Float less than one.
        :return: Boolean
        """
        assert 0 <= probability <= 1, "Probability must be greater than or equal to 0 and less than or equal to 1."
        return random.random() < probability

    def make_note_or_rest(self, duration=1, probability=0.50):
        """
        Helper function that makes a note or a rest depending on the probability in self.is_rest.
        :param duration: Integer or float.
        :param probability: Float between 0 and 1
        :return: String ('/r1.5'), integer or float.
        """
        try:
            if self.is_rest(probability):
                return self.build_rest(duration)
            else:
                return duration
        except AssertionError as msg:
            print(msg)
        finally:
            # make a really short note and pray
            return 0.25

    def build_notes_and_durations(self):
        pass

    def appoggiatura(self, chord_and_duration_block):
        """
        Makes an appoggiatura based on the entire duration of the chord and duration block. Can be an accented
        upper or lower neighbor.
        :param chord_and_duration_block: Tuple of (Chord, float || int)
        :return: Tuple of (List of Notes, List of float || int, float || int),
        """
        notes = []
        durations = []
        # get a chord tone
        chord_tone = random.choice(chord_and_duration_block[0].notes)
        # appoggiatura is an accented neighbor
        appoggiatura_note = self.get_closest_scale_tone_to_note(chord_tone)
        while appoggiatura_note == chord_tone:
            appoggiatura_note = self.get_random_neighbor(chord_tone)
        notes.append(appoggiatura_note)
        # it must resolve to a chord tone
        notes.append(chord_tone)
        # duration of the appoggiatura is usually less than the length of the harmonic rhythm unit
        appoggiatura_duration = self.get_random_duration()
        while appoggiatura_duration > chord_and_duration_block[1]:
            appoggiatura_duration = self.get_random_duration()
        durations.append(appoggiatura_duration)
        # make duration of resolution note
        # if remaining duration is less than minimum duration amount, resolution_duration is remainder. Otherwise
        # get a random duration smaller than the remainder
        remaining_duration = chord_and_duration_block[1] - appoggiatura_duration
        if remaining_duration <= 0.25:
            resolution_duration = remaining_duration
        else:
            resolution_duration = self.get_random_duration()
            while resolution_duration > remaining_duration:
                resolution_duration = self.get_random_duration()
        durations.append(resolution_duration)
        # get remaining duration in chord and dur block
        remaining_duration = remaining_duration - resolution_duration
        return notes, durations, remaining_duration

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
            suspension_note = self.get_closest_scale_tone_to_note(next_chord_tone)
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

    def mordent(self, chord_and_duration_block, upper_mordent: bool = False):
        """
        Makes a mordent based on the chord_and_duration block given.
        :param chord_and_duration_block: tuple of (Chord, int || float)
        :param upper_mordent: boolean, defaults to False as lower mordents are more common
        :return: tuple of (List of Notes, List of float || int, float || int)
        """
        notes = []
        durations = []
        # get random indicated note
        indicated_note = random.choice(chord_and_duration_block[0].notes)
        # upper_mordent input determines whether its a lower mordent or upper mordent
        if upper_mordent:
            neighbor = self.scalar_upper_neighbor(indicated_note)
        else:
            neighbor = self.scalar_lower_neightbor(indicated_note)
        # add all notes to notes list
        notes += [indicated_note, neighbor, indicated_note]
        # add ornamental notes to durations
        durations += [0.125, 0.125]
        # build resolution duration and append to durations
        resolution_duration = self.get_random_duration()
        while resolution_duration > chord_and_duration_block[1] - 0.25:
            resolution_duration = self.get_random_duration()
        durations.append(resolution_duration)
        # Get the remaining duration in the harmonic rhythm subunit
        remaining_duration = chord_and_duration_block[1] - sum(durations)
        return notes, durations, remaining_duration

    def turn(self, chord_and_duration_block, current_duration_left, chromatic: bool = False):
        notes = []
        # get random indicated note
        indicated_note = random.choice(chord_and_duration_block[0].notes)
        # get upper and lower neighbor
        if chromatic:
            ln = self.chromatic_lower_neighbor(indicated_note)
            un = self.chromatic_upper_neighbor(indicated_note)
        else:
            ln = self.scalar_lower_neightbor(indicated_note)
            un = self.scalar_upper_neighbor(indicated_note)
        # put turn into notes list
        notes += [un, indicated_note, ln, indicated_note]
        # get durations
        total_duration = self.get_random_duration()
        while total_duration > current_duration_left:
            total_duration = self.get_random_duration()
        durations = [total_duration / len(notes) for _ in range(len(notes))]
        remaining_duration = current_duration_left - total_duration
        return notes, durations, remaining_duration

    def set_scale(self, scale: Scale):
        """
        Setter function to change the scale as needed.
        :param scale: Scale object
        :return: None
        """
        self.scale = scale

    def get_closest_scale_tone_to_note(self, note: Note):
        """
        Gets the closest scalar note to a given note.
        :param note: Note
        :return: Note
        """
        closest_tone = self.scale.notes[0]
        for tone in self.scale.notes:
            if abs(note.midi_note_number - tone.midi_note_number) < (
                    note.midi_note_number - closest_tone.midi_note_number):
                closest_tone = tone
        return closest_tone

    def scalar_upper_neighbor(self, note: Note):
        """
        Gets the scalar upper neighbor to a given note.
        :param note: Note
        :return: Note
        """
        note_index = self.scale.notes.index(note)
        return self.scale.notes[(note_index + 1) % len(self.scale.notes)]

    def scalar_lower_neightbor(self, note: Note):
        """
        Get the scalar lower neighbor to a given note.
        :param note: Note
        :return: Note
        """
        note_index = self.scale.notes.index(note)
        return self.scale.notes[(note_index - 1) % len(self.scale.notes)]

    def chromatic_upper_neighbor(self, note: Note):
        """
        Get the chromatic upper neighbor to a given note.
        :param note: Note
        :return: Note
        """
        return Note(note.midi_note_number + 1)

    def chromatic_lower_neighbor(self, note: Note):
        """
        get the chromatic lower neighbor to a given note.
        :param note: Note
        :return: Note
        """
        return Note(note.midi_note_number - 1)

    def get_random_neighbor(self, note: Note):
        """
        Get a random neighbor to a given note.
        :param note: Note
        :return: Note
        """
        return random.choice([
            self.scalar_upper_neighbor,
            self.scalar_lower_neightbor,
            self.chromatic_upper_neighbor,
            self.chromatic_lower_neighbor
        ])(note)

    def get_random_duration(self):
        """
        Get a random duration between 0.25 and 2 beats.
        :return: float || int
        """
        return random.choice([0.25, 1 / 3, 0.5, 2 / 3, 0.75, 1, 1.25, 1.5, 1.75, 2])

    def get_random_chord_tone(self, chord: Chord):
        """
        Get a random chord tone from a given chord.
        :param chord: Chord
        :return: Note
        """
        return random.choice(chord.notes)

    def get_closest_chord_tone_to_note(self, note: Note, chord: Chord):
        """
        Gets the closest tone in a chord to a given note.
        :param note: Note
        :param chord: Chord
        :return: Note
        """
        closest_tone = chord.notes[0]
        for tone in chord.notes:
            if abs(note.midi_note_number - tone.midi_note_number) < (note.midi_note_number - closest_tone.midi_note_number):
                closest_tone = tone
        return closest_tone

    def is_tuplet(self, duration):
        """
        Helper function to determine whether a duration is a tuplet
        :param duration: int or float
        :return: boolean
        """
        if duration % 1/3 == 0:
            return True
        else:
            return False

    def is_sustainable(self, next_chord_and_dur_block, current_chord_and_dur_block=None,
                       current_note_and_dur_block=None):
        """
        Tests to see if the current note or chord is sustainable to the next chord and dur block.
        :param next_chord_and_dur_block: tuple of (Chord, int || float)
        :param current_chord_and_dur_block: tuple of (Chord, int || float)
        :param current_note_and_dur_block: tuple of (Note, int || float)
        :return: boolean
        """
        c2 = next_chord_and_dur_block[0]
        assert current_note_and_dur_block is not None or current_chord_and_dur_block is not None, "You must pass " \
                                                                                                  "either a note or " \
                                                                                                  "a chord. Try " \
                                                                                                  "declaring only " \
                                                                                                  "one explicitly "

        if current_chord_and_dur_block is not None:
            c1 = current_chord_and_dur_block[0]
            for note1 in c1.notes:
                for note2 in c2.notes:
                    if note1 == note2:
                        return True
            return False

        if current_note_and_dur_block is not None:
            note1 = current_note_and_dur_block[0]
            for note2 in c2.notes:
                if note1 == note2:
                    return True
            return False

    def sustain_across_chord_and_dur_block(self, current_chord_and_dur_block, next_chord_and_dur_block):
        """
        Sustains the current chord_and_dur_block to the next chord and dur block
        :param current_chord_and_dur_block: tuple of (Chord, int || float)
        :param next_chord_and_dur_block: tuple of (Chord, int || float)
        :return: tuple of (Note, int || float)
        """
        # get the current chords
        c1 = current_chord_and_dur_block[0]
        c2 = next_chord_and_dur_block[0]
        # Loop through them and return the note and the added durational values
        for note1 in c1.notes:
            for note2 in c2.notes:
                if note1 == note2:
                    return note1, current_chord_and_dur_block[1] + next_chord_and_dur_block[1]

    def sustain_across_note_to_chord_and_dur_block(self, note_and_duration, next_chord_and_dur_block):
        # get note
        note1 = note_and_duration[0]
        # get chord
        c2 = next_chord_and_dur_block[0]
        for note2 in c2.notes:
            if note1 == note2:
                return note1, note_and_duration[1] + next_chord_and_dur_block[1]


class SustainedMelody(Melody):
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        notes = []
        durations = []
        chords_and_durations = self.harmonic_rhythm.get_zipped_hr_chords_and_durations()
        i = 0
        while i < len(chords_and_durations) - 1:
            if i == 0:
                note_and_duration = self.get_next_note_and_dur(next_chord_and_dur_block=chords_and_durations[i + 1],
                                                               current_chord_and_dur_block=chords_and_durations[i])
                notes.append(note_and_duration[0])
                durations.append(note_and_duration[1])
            else:
                print(i, notes, durations)
                current_note_and_dur_block = notes[-1], durations[-1]
                if self.is_sustainable(next_chord_and_dur_block=chords_and_durations[i + 1],
                                       current_note_and_dur_block=current_note_and_dur_block):
                    note_and_duration = self.get_next_note_and_dur(chords_and_durations[i + 1],
                                                                   current_note_and_dur_block=current_note_and_dur_block)
                    notes[-1], durations[-1] = note_and_duration[0], note_and_duration[1]
                else:
                    note_and_duration = self.get_next_note_and_dur(chords_and_durations[i + 1],
                                                                   current_chord_and_dur_block=chords_and_durations[i])
                    notes.append(note_and_duration[0])
                    durations.append(note_and_duration[1])
            i += 1
        return [notes, durations]

    def get_next_note_and_dur(self, next_chord_and_dur_block,
                              current_chord_and_dur_block=None,
                              current_note_and_dur_block=None):
        """
        Gets the next note and duration, either by generating a summed durational value of the existing, sustained note,
        or by getting a new, random chord note.
        :param next_chord_and_dur_block: tuple (Chord, int || float)
        :param current_chord_and_dur_block: tuple (Chord, int || float)
        :param current_note_and_dur_block: tuple (Note, int || float)
        :return: tuple (Note, int || float)
        """
        assert current_note_and_dur_block is not None or current_chord_and_dur_block is not None, "You must pass " \
                                                                                                  "either a note or " \
                                                                                                  "a chord. Try " \
                                                                                                  "declaring only " \
                                                                                                  "one explicitly "
        if self.is_sustainable(next_chord_and_dur_block, current_chord_and_dur_block=current_chord_and_dur_block,
                               current_note_and_dur_block=current_note_and_dur_block):
            try:
                if current_chord_and_dur_block is not None:
                    return self.sustain_across_chord_and_dur_block(current_chord_and_dur_block,
                                                                   next_chord_and_dur_block)
                if current_note_and_dur_block is not None:
                    return self.sustain_across_note_to_chord_and_dur_block(current_note_and_dur_block,
                                                                           next_chord_and_dur_block)
            except RuntimeError as e:
                print("Somehow this was considered sustainable, but none of the possible sustain conditions ran...", e)
        else:
            try:
                if current_chord_and_dur_block is not None:
                    # get closest closest tone to last note
                    return self.get_random_chord_tone(current_chord_and_dur_block[0]), current_chord_and_dur_block[1]
                if current_note_and_dur_block is not None:
                    return current_note_and_dur_block
            except RuntimeError as e:
                print("Somehow you didn't return a tuple at all?", e)


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
    hr = HarmonicRhythm(meter, harmony)
    melody = Melody(hr, scale)
    sm = SustainedMelody(hr, scale)
    # print(melody.get_closest_scale_tone_to_chord_tone(Note(8)))
    # print(sm.sustain_across_chord_and_dur_block((a, 2), (b, 2)))
    # print(sm.get_next_note_and_dur((a, 2), current_note_and_dur_block=(Note(4), 7)))
    print(sm.notes_and_durations)
    # print(sm.get_next_note_and_dur((a, 2), (CM7, 2), (Cmm7, 4)))
    # for i in range(100):
    #     print(melody.appoggiatura((b, 2)))
    #     print(melody.suspension(1, (b, 2), (a, 2)))
    #     print(melody.turn((b, 2), 2))
