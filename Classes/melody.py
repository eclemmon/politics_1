from Classes.harmonic_rhythm import HarmonicRhythm
from Classes.chord_progression import ChordProgression
from Classes.scale import Scale
from Classes.meter import *
from Classes.note import Note
from Classes.chord import Chord
from typing import Union
from Rhythm_Generators.subdivision_generator import subdivide_meter_into_polyrhythm
import random


class Melody:
    """
    Melody superclass for constructing melodies.
    """

    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale, transposition=5):
        """
        Intialization of Melody class.
        :param harmonic_rhythm: HarmonicRhythm
        :param scale: Scale
        :param transposition: int
        """
        self.harmonic_rhythm = harmonic_rhythm
        self.scale = scale
        self.notes_and_durations = self.build_notes_and_durations()
        self.transpose_self_to_range(transposition)

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

    def sum_with_rests(self, durations: list):
        """
        A helper testing function for checking the sum of durations generated when constructing the melody class.
        :param durations: list
        :return: float or int
        """
        res = []
        for dur in durations:
            if type(dur) == str:
                res.append(float(dur[2:]))
            else:
                res.append(dur)
        return sum(res)

    def build_notes_and_durations(self):
        """
        Template for build_notes_and_durations
        :return: None
        """
        pass

    def get_next_note_and_dur(self):
        """
        Template for get_next_note_and_dur
        :return: None
        """
        pass

    def transpose_self_to_range(self, transposition: int):
        """
        A helper function to transpose the notes in the melody to a particular range.
        :param transposition: int of num octaves to add to note
        :return: None
        """
        for i in range(len(self.notes_and_durations[0])):
            # tuples are immutable — so please don't transpose the same note over and over!
            self.notes_and_durations[0][i] = Note(self.notes_and_durations[0][i].midi_note_number)
            self.notes_and_durations[0][i].transpose(transposition)

    def get_durations(self):
        """
        Getter function to get the durations of the melody.
        :return: list of durations (floats || ints)
        """
        return self.notes_and_durations[1]

    def get_notes(self):
        """
        Getter function to get the notes of the melody.
        :return: list of Notes
        """
        return self.notes_and_durations[0]

    def appoggiatura(self, chord_and_duration_block: tuple, remaining_duration: Union[float, int]):
        """
        Makes an appoggiatura based on the entire duration of the chord and duration block. Can be an accented
        upper or lower neighbor.
        :param remaining_duration: flaot or int
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
        # duration of the appoggiatura and resolution must be less than or equal to remaining duration
        if remaining_duration <= 0.25:
            total_appoggiatura_duration = remaining_duration
        else:
            total_appoggiatura_duration = self.get_random_duration()
            while total_appoggiatura_duration > remaining_duration:
                total_appoggiatura_duration = self.get_random_duration()
        durations += [total_appoggiatura_duration / 2, total_appoggiatura_duration / 2]
        # make duration of resolution note
        # if remaining duration is less than minimum duration amount, resolution_duration is remainder. Otherwise
        # get a random duration smaller than the remainder
        remaining_duration = remaining_duration - total_appoggiatura_duration
        return notes, durations, remaining_duration

    def suspension(self, current_duration_left: Union[float, int], current_chord_and_duration_block: tuple,
                   next_chord_and_duration_block: tuple):
        """
        Makes a suspension between the current chord and duration block and the next chord and duration block.
        :param current_duration_left: int || float
        :param current_chord_and_duration_block: tuple of (Chord, int)
        :param next_chord_and_duration_block: tuple of (Chord, int)
        :return: tuple of (List, List, int || float)
        """
        notes = []
        durations = []
        # suspension holds note over a harmonic change
        # it usually resolves to a chord tone (eventually)
        # get next chord tone to resolve into
        next_chord_tone = random.choice(next_chord_and_duration_block[0].notes[:])
        # if the chords are the same, suspension note is a random neighbor to next chord tone
        # (more like a neighbor note). Else suspension is closest scale tone to the selected next chord tone
        if current_chord_and_duration_block[0] == next_chord_and_duration_block[0]:
            suspension_note = self.get_random_neighbor(next_chord_tone)
        else:
            suspension_note = self.get_closest_scale_tone_to_note(next_chord_tone)
        # while suspension is same as the next chord tone, make a new next chord tone and get another suspension.
        # solve edge cases where suspension is same as next chord
        while suspension_note == next_chord_tone:
            next_chord_tone = random.choice(next_chord_and_duration_block[0].notes[:])
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

    def mordent(self, chord_and_duration_block: tuple, current_duration_left: Union[int, float],
                upper_mordent: bool = False):
        """
        Makes a mordent based on the chord_and_duration block given.
        :param current_duration_left: int || float
        :param chord_and_duration_block: tuple of (Chord, int || float)
        :param upper_mordent: boolean, defaults to False as lower mordents are more common
        :return: tuple of (List of Notes, List of float || int, float || int)
        """
        notes = []
        durations = []
        # get random indicated note
        indicated_note = random.choice(chord_and_duration_block[0].notes[:])
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
        if current_duration_left - 0.25 <= 0.25:
            resolution_duration = current_duration_left - 0.25
            durations.append(resolution_duration)
        else:
            resolution_duration = self.get_random_duration(tuples_allowed=False)
            while resolution_duration > current_duration_left - 0.25:
                resolution_duration = self.get_random_duration(tuples_allowed=False)
            durations.append(resolution_duration)
        # Get the remaining duration in the harmonic rhythm subunit
        remaining_duration = current_duration_left - sum(durations)
        return notes, durations, remaining_duration

    def turn(self, chord_and_duration_block: tuple, current_duration_left: Union[float, int], chromatic: bool = False):
        """
        Makes a 'turn' ornamentation. Usually, this consists of an accented upper neighbor, the primary indicated note,
        a lower neighbor, and then back to the indicated ote.
        :param chord_and_duration_block: tuple (Chord, float || int)
        :param current_duration_left: float || int
        :param chromatic: boolean
        :return: tuple of (list, list, float || int)
        """
        notes = []
        # get random indicated note
        indicated_note = random.choice(chord_and_duration_block[0].notes[:])
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

    def trill(self, chord_and_duration_block, current_duration_left,
              lower_trill: bool = False, chromatic_trill: bool = False):
        notes = []
        # get random indicated note
        indicated_note = random.choice(chord_and_duration_block[0].notes[:])
        # get upper or lower neighbor
        if lower_trill:
            if chromatic_trill:
                n = self.chromatic_lower_neighbor(indicated_note)
            else:
                n = self.scalar_lower_neightbor(indicated_note)
        else:
            if chromatic_trill:
                n = self.chromatic_upper_neighbor(indicated_note)
            else:
                n = self.scalar_upper_neighbor(indicated_note)
        # get durations
        total_duration = self.get_random_duration(tuples_allowed=False)
        while total_duration > current_duration_left:
            if total_duration < 0.25:
                total_duration = current_duration_left
                break
            else:
                total_duration = self.get_random_duration(tuples_allowed=False)
        if total_duration == current_duration_left:
            durations = [total_duration]
        else:
            durations = [0.125 for _ in range(int(total_duration / 0.125))]
        # get remaining duration
        remaining_duration = current_duration_left - total_duration
        # Start trill from the top
        trill = 0
        for _ in durations:
            if trill % 2 == 0:
                notes.append(n)
            else:
                notes.append(indicated_note)
            trill += 1
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
        # get closest scale tone to note for safety
        note = self.get_closest_scale_tone_to_note(note)
        # get index
        note_index = self.scale.notes.index(note)
        # get upper neighbor
        return self.scale.notes[(note_index + 1) % len(self.scale.notes)]

    def scalar_lower_neightbor(self, note: Note):
        """
        Get the scalar lower neighbor to a given note.
        :param note: Note
        :return: Note
        """
        # get closest scale tone to note for safety
        note = self.get_closest_scale_tone_to_note(note)
        # get index
        note_index = self.scale.notes.index(note)
        # get upper neighbor
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

    def get_random_duration(self, tuples_allowed: bool = True):
        """
        Gets a random duration. If tuples allowed, can return values 1/3 and 2/3
        :param tuples_allowed: boolean
        :return: int || float
        """
        if tuples_allowed:
            return random.choice([0.25, 1 / 3, 0.5, 2 / 3, 0.75, 1, 1.25, 1.5, 1.75, 2])
        else:
            return random.choice([0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2])

    def get_random_chord_tone(self, chord: Chord):
        """
        Get a random chord tone from a given chord.
        :param chord: Chord
        :return: Note
        """
        return random.choice(chord.notes)

    def get_random_scale_tone(self, scale: Scale):
        """
        Get a random note from a given scale.
        :param scale: Scale
        :return: Note
        """
        return random.choice(scale.notes)

    def get_random_scale_note_and_dur(self):
        """
        Gets a random scale tone and duration
        :return: tuple (Note, int || float)
        """
        note = self.get_random_scale_tone(self.scale)
        duration = self.get_random_duration()
        return note, duration

    def get_closest_chord_tone_to_note(self, note: Note, chord: Chord):
        """
        Gets the closest tone in a chord to a given note.
        :param note: Note
        :param chord: Chord
        :return: Note
        """
        closest_tone = chord.notes[0]
        for tone in chord.notes:
            closest_tone_distance = abs(note.midi_note_number - closest_tone.midi_note_number)
            tone_distance = abs(note.midi_note_number - tone.midi_note_number)
            if tone_distance < closest_tone_distance:
                closest_tone = tone
        return closest_tone

    @staticmethod
    def is_tuplet(duration: Union[int, float]):
        """
        Helper function to determine whether a duration is a tuplet
        :param duration: int or float
        :return: boolean
        """
        if duration % 1 / 3 == 0:
            return True
        else:
            return False

    @staticmethod
    def is_sustainable(next_chord_and_dur_block: tuple, current_chord_and_dur_block: Union[tuple, None] = None,
                       current_note_and_dur_block: Union[tuple, None] = None):
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

    @staticmethod
    def sustain_across_chord_and_dur_block(current_chord_and_dur_block: tuple, next_chord_and_dur_block: tuple):
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

    @staticmethod
    def sustain_across_note_to_chord_and_dur_block(note_and_duration: tuple, next_chord_and_dur_block: tuple):
        """
        Sustains the current note and duration over to the next chord and duration block.
        :param note_and_duration: tuple of (Note, int || float)
        :param next_chord_and_dur_block: tuple of (Chords, int || float)
        :return: tuple of (Note, int || float)
        """
        # get note
        note1 = note_and_duration[0]
        # get chord
        c2 = next_chord_and_dur_block[0]
        for note2 in c2.notes:
            if note1 == note2:
                return note1, note_and_duration[1] + next_chord_and_dur_block[1]


class SustainedMelody(Melody):
    """
    SustainedMelody Class. Sustains the melody notes as much as possible
    """

    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        """
        Initialization for SustainedMelody
        :param harmonic_rhythm: HarmonicRhythm
        :param scale: Scale
        """
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        """
        Builds notes and durations for the SustainedMelody class. Relies heavily on logic from:
        > Melody.sustain_across_note_to_chord_and_dur_block, and
        > Melody.sustain_across_chord_and_dur_block
        :return: list of lists [list, list]
        """
        notes = []
        durations = []
        chords_and_durations = self.harmonic_rhythm.get_zipped_hr_chords_and_durations()
        i = 0
        while i < len(chords_and_durations):
            # Get the first chord and compare it to the next chord.
            if i == 0:
                # if it is sustainable
                sustainable_note_and_duration = self.get_next_note_and_dur(
                    next_chord_and_dur_block=chords_and_durations[i + 1],
                    current_chord_and_dur_block=chords_and_durations[i]
                )
                notes.append(sustainable_note_and_duration[0])
                durations.append(chords_and_durations[i][1])
            else:
                # The note and duration is the previously appended note and duration
                # The previously appended note and duration is the note and duration to check whether it is sustainable
                # the current chord in the loop, starting from 1..n is the chord to be compared to
                check_note_and_dur_block = notes[-1], durations[-1]
                # check to see if the current note and duration is sustainable
                if self.is_sustainable(next_chord_and_dur_block=chords_and_durations[i],
                                       current_note_and_dur_block=check_note_and_dur_block):
                    # if it is sustainable sustain it
                    note_and_duration = self.get_next_note_and_dur(chords_and_durations[i],
                                                                   current_note_and_dur_block=check_note_and_dur_block)
                    # replace the previous values in the durations array so that the extended duration is given
                    durations[-1] = note_and_duration[1]
                else:
                    # if the note and duration is not sustainable, the function will get a random chord note
                    # from the current block add it to the notes and durations
                    notes.append(self.get_random_chord_tone(chords_and_durations[i][0]))
                    durations.append(chords_and_durations[i][1])
            i += 1
        return [notes, durations]

    def get_next_note_and_dur(self, next_chord_and_dur_block: tuple,
                              current_chord_and_dur_block: Union[tuple, None] = None,
                              current_note_and_dur_block: Union[tuple, Note] = None):
        """
        Gets the next note and duration, either by generating a summed durational value of the existing, sustained note,
        or by getting a new, random chord note. WARNING: GOBBLETIGOOK AND REDUNDANCIES BELOW
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
        # If the note is sustainable to the next chord
        if self.is_sustainable(next_chord_and_dur_block, current_chord_and_dur_block=current_chord_and_dur_block,
                               current_note_and_dur_block=current_note_and_dur_block):
            # Sustain the chord or note across to the next chord and duration
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


class RandomMelody(Melody):
    """
    RandomMelody class. Generates a melody randomly, by selecting notes and durations randomly as long as there is
    space in the total duration left.
    """
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        """
        Initialization for RandomMelody
        :param harmonic_rhythm: HarmonicRhythm
        :param scale: Scale
        """
        super().__init__(harmonic_rhythm, scale)

    def get_next_note_and_dur(self):
        """
        Gets a random scale tone and a random duration and returns
        :return: tuple of (Note, float || int)
        """
        return self.get_random_scale_tone(self.scale), self.get_random_duration()

    def build_notes_and_durations(self):
        """
        Builds notes and durations for RandomMelody class. While sum(durations) < total_duration, adds random notes
        and duration values to notes list and durations list.
        :return: list of lists [list, list]
        """
        notes = []
        durations = []
        total_duration = self.harmonic_rhythm.meter.num_beats * self.harmonic_rhythm.num_bars
        while total_duration > 0:
            note_and_dur = self.get_next_note_and_dur()
            if note_and_dur[1] >= total_duration:
                notes.append(note_and_dur[0])
                durations.append(total_duration)
                break
            else:
                notes.append(note_and_dur[0])
                durations.append(note_and_dur[1])
                total_duration -= note_and_dur[1]
        return [notes, durations]


class LeapyMelody(Melody):
    """
    LeapyMelody class. Generates a melody that jumps around between three upper octaves. Selects from either getting
    a random note and duration, or generating a random appoggiatura.
    """
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        """
        Initialization for LeapyMelody class.
        :param harmonic_rhythm: HarmonicRhythm
        :param scale: Scale
        """
        super().__init__(harmonic_rhythm, scale)

    def get_next_note_and_dur(self, current_duration_left: Union[float, int], current_chord_and_dur: tuple):
        """
        Function to get the next note and duration for build_notes_and_durations function.
        :param current_duration_left: float || int
        :param current_chord_and_dur: tuple (Chord, float || int)
        :return: tuple of (List, List, float || int)
        """
        r = random.randint(0, 1)
        if r == 0:
            appoggiatura = self.appoggiatura(current_chord_and_dur, current_duration_left)
            return appoggiatura
        elif r == 1:
            note = self.get_random_scale_tone(self.scale)
            if current_duration_left <= 0.25:
                duration = self.make_note_or_rest(current_duration_left)
                duration_left = 0
            else:
                duration = self.get_random_duration(tuples_allowed=True)
                while duration > current_duration_left:
                    duration = self.get_random_duration(tuples_allowed=True)
                duration_left = current_duration_left - duration
                duration = self.make_note_or_rest(duration)
            return [note], [duration], duration_left

    def build_notes_and_durations(self):
        """
        Builds notes and durations for the LeapuMelody class. Builds the notes and durations and then
        randomly transposes the notes.
        :return: list of lists [Notes, Durations]
        """
        notes = []
        durations = []

        chord_and_dur_blocks = self.harmonic_rhythm.get_zipped_hr_chords_and_durations()
        for i in range(len(chord_and_dur_blocks)):
            current_duration_left = chord_and_dur_blocks[i][1]
            while current_duration_left > 0:
                notes_and_durs = self.get_next_note_and_dur(current_duration_left, chord_and_dur_blocks[i])
                notes += notes_and_durs[0]
                durations += notes_and_durs[1]
                current_duration_left = notes_and_durs[2]
        for i in range(len(notes)):
            # tuples are immutable — so please don't transpose the same note over and over!
            transposition = random.choice([0, 1, 2])
            notes[i] = Note(notes[i].midi_note_number)
            notes[i].transpose(transposition)
        return [notes, durations]


class ChoppyMelody(Melody):
    """
    ChoppyMelody class. Using a stochastic algorithm and short note durations, generates a choppy melody.
    """
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        """
        Initialization for ChoppyMelody class.
        :param harmonic_rhythm: HarmonicRhythm
        :param scale: Scale
        """
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        """
        Builts notes and durations for Choppy Melody
        :return: List of Lists [[Notes], [floats]]
        """
        note_duration_values = [0.25, 0.5, 0.75]
        notes = []
        durations = []

        for chord_and_dur_block in self.harmonic_rhythm.get_zipped_hr_chords_and_durations():
            duration_left = chord_and_dur_block[1]
            # While there is duration in the chord left, make new notes and durations before moving onto next iteration.
            while duration_left > 0:
                duration = random.choice(note_duration_values)
                # If the duration is longer than the duration left, get a new duration
                while duration > duration_left:
                    duration = random.choice(note_duration_values)
                # Duration
                durations.append(self.make_note_or_rest(duration, 0.5))
                # Note
                chord_tone = self.get_random_chord_tone(chord_and_dur_block[0])
                scale_tone = self.get_random_scale_tone(self.scale)
                note = random.choice([chord_tone, scale_tone])
                notes.append(note)
                # Update duration left
                duration_left -= duration
        return [notes, durations]


class PolyrhythmicMelody(Melody):
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        notes = []
        durations = []

        for chord_and_dur_block in self.harmonic_rhythm.get_zipped_hr_chords_and_durations():
            polyrhythm = subdivide_meter_into_polyrhythm(chord_and_dur_block[1], random.randint(3, 7))
            durations += polyrhythm
            notes += [self.get_random_chord_or_scale_tone(self.scale, chord_and_dur_block[0]) for _ in
                      range(len(polyrhythm))]

        durations = [self.make_note_or_rest(duration) for duration in durations]

        return [notes, durations]

    def get_random_chord_or_scale_tone(self, scale, chord):
        return random.choice([self.get_random_chord_tone(chord), self.get_random_scale_tone(scale)])


class MaxOrnamentationMelody(Melody):
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        notes = []
        durations = []

        for chord_and_duration in self.harmonic_rhythm.get_zipped_hr_chords_and_durations():
            current_duration_left = chord_and_duration[1]
            while current_duration_left > 0:
                if current_duration_left <= 0.25:
                    notes.append(self.get_random_scale_tone(self.scale))
                    durations.append(current_duration_left)
                    current_duration_left = 0
                else:
                    notes_durations_remainder = self.get_random_ornamentation(chord_and_duration, current_duration_left)
                    notes += notes_durations_remainder[0]
                    durations += notes_durations_remainder[1]
                    current_duration_left = notes_durations_remainder[2]
        return notes, durations

    def get_random_ornamentation(self, chord_and_duration, current_duration_left):
        r = random.randint(0, 3)
        if r == 0:
            return self.appoggiatura(chord_and_duration, current_duration_left)
        elif r == 1:
            return self.mordent(chord_and_duration, current_duration_left, random.choice([True, False]))
        elif r == 2:
            return self.turn(chord_and_duration, current_duration_left, random.choice([True, False]))
        else:
            return self.trill(chord_and_duration, current_duration_left,
                              random.choice([True, False]), random.choice([True, False]))


if __name__ == "__main__":

    from a2_Cybernetic_Republic.python_files.send_to_sc_functions import *
    from pythonosc import udp_client

    sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)


    def sum_with_rests(durations):
        res = []
        for dur in durations:
            if type(dur) == str:
                res.append(float(dur[2:]))
            else:
                res.append(dur)
        return sum(res)


    meter1 = ComplexMeter(7, [3, 1, 2, 1, 1, 2, 1], [2, 3, 2])
    meter2 = CompoundMeter(9, [3, 1, 1, 2, 1, 1, 2, 1, 1], [3, 3, 3])
    meter3 = SimpleDuple(4)
    scale = Scale(Note(0), Note(2), Note(4), Note(5), Note(7), Note(9), Note(11))
    c_major = Chord(Note(0), Note(4), Note(7))
    CM7 = Chord(Note(0), Note(4), Note(7), Note(11))
    Cmm7 = Chord(Note(0), Note(3), Note(7), Note(10))
    a = Chord(Note(9), Note(0), Note(4))
    G7 = Chord(Note(7), Note(11), Note(14), Note(17))
    e = Chord(Note(4), Note(7), Note(11))
    b = Chord(Note(11), Note(2), Note(5))
    B = Chord(Note(11), Note(3), Note(6))
    chords = [c_major, CM7, a, G7, e, b, B]
    random.shuffle(chords)
    prog = ChordProgression(chords)
    hr = HarmonicRhythm(random.choice([meter1, meter2, meter3]), prog)
    m = SustainedMelody(hr, scale)
    send_bass_or_melody_notes_to_sc(m, sc_client, "/melody_notes")
    send_bass_or_melody_durations_to_sc(m, sc_client, '/melody_durations')
    send_bass_or_melody_initialization_to_sc(0, sc_client, '/melody_init')
    # for i in range(100):
    #     random.shuffle(chords)
    #     prog = ChordProgression(chords)
    #     hr = HarmonicRhythm(random.choice([meter1, meter2, meter3]), prog)
    #     # melody = Melody(hr, scale)
    #     sm = SustainedMelody(hr, scale)
    #     rm = RandomMelody(hr, scale)
    #     cm = ChoppyMelody(hr, scale)
    #     prm = PolyrhythmicMelody(hr, scale)
    #     ornm = MaxOrnamentationMelody(hr, scale)
    #     lm = LeapyMelody(hr, scale)
    #     for i in [sm, rm, cm, prm, ornm, lm]:
    #         print("name: {}, sum durations: {}, total beats: {}, meter beats: {}".format(i.__class__.__name__,
    #                                                                     sum_with_rests(i.notes_and_durations[1]),
    #                                                                     i.harmonic_rhythm.meter.num_beats * i.harmonic_rhythm.num_bars,
    #                                                                                      i.harmonic_rhythm.meter.num_beats)
    #               )
    # print(sum(sm.notes_and_durations[1]), )
    # print(sum(rm.notes_and_durations[1]))
    # print(sum(cm.notes_and_durations[1]))
    # print(sum(prm.notes_and_durations[1]))
    # print(sum(ornm.notes_and_durations[1]))
    # print(sum(lm.notes_and_durations[1]))
    # print(lm.notes_and_durations[0])
