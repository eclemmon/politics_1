import random

from Classes.chord import Chord
from Classes.chord_progression import ChordProgression
from Classes.harmonic_rhythm import HarmonicRhythm
from Classes.meter import *
from Classes.note import Note
from Classes.scale import Scale
from Rhythm_Generators.subdivision_generator import subdivide_meter_into_polyrhythm


class Bass:
    """
    Bass superclass for musical generation.
    """
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale, transposition: int = 2):
        """
        Intializes Bass class.
        :param harmonic_rhythm: HarmonicRhythm
        :param scale: Scale
        :param transposition: int
        """
        self.harmonic_rhythm = harmonic_rhythm
        self.scale = scale
        self.notes_and_durations = self.build_notes_and_durations()
        self.transpose_self_to_range(transposition)

    def get_next_note(self):
        """
        Template method for getting the next note.
        :return: None
        """
        pass

    def build_bass_line(self):
        """
        Template method for building the bass line
        :return: None
        """
        pass

    def build_notes_and_durations(self):
        """
        Template method for building the bass line
        :return: None
        """
        pass

    @staticmethod
    def build_rest(duration: float = 1):
        """
        Static method for building rests by prepending a float || int durations with the key '/r'
        :param duration: float || int
        :return: String
        """
        return '/r' + str(duration)

    @staticmethod
    def is_rest(probability: float = 0.50):
        """
        Static method for determining whether a duration is a note or a rest via probability and random number
        generation.
        :param probability: float || int
        :return: Boolean
        """
        return random.random() < probability

    def make_note_or_rest(self, duration: float = 1, probability: float = 0.50):
        """
        Builds on self.build_rest and self.is_rest to return either a float || int duration or a str '/r' prepended
        duration.
        :param duration: float || int
        :param probability: float || int
        :return: str || float || int
        """
        if self.is_rest(probability):
            return self.build_rest(duration)
        else:
            return duration

    @staticmethod
    def sum_with_rests(durations: list):
        """
        A function to help with testing. To be deprecated and moved into a testing suite.
        :param durations: List of durations
        :return: float || int total of durations
        """
        res = []
        for dur in durations:
            if type(dur) == str:
                res.append(float(dur[2:]))
            else:
                res.append(dur)
        return sum(res)

    def transpose_self_to_range(self, transposition: int):
        """
        Transposes the notes in self.notes_and_durations into a new range. Since the Note class implements
        some stronger object identity functionality, it builds new Note objects to transpose.
        :param transposition: int, number of octaves to transpose
        :return: None
        """
        for i in range(len(self.notes_and_durations[0])):
            # tuples are immutable — so please don't transpose the same note over and over!
            self.notes_and_durations[0][i] = Note(self.notes_and_durations[0][i].midi_note_number)
            self.notes_and_durations[0][i].transpose(transposition)


class AlbertiBass(Bass):
    """
    AlbertiBass class. Generates an imitation of the common, classically-styled alberti bass.
    """
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale, note_duration: float = 0.5):
        """
        Initializes the AlbertiBass class.
        :param harmonic_rhythm: HarmonicRhythm
        :param scale: Scale
        :param note_duration: int || float
        """
        self.note_duration = note_duration
        super().__init__(harmonic_rhythm, scale)

    # TODO: The logic here is sort of incorrect, but good enough. Also should defer choice of note duration length to
    # how fast the harmonic rhythm actually is...
    def build_notes_and_durations(self):
        """
        Builds notes and durations for the Alberti Bass Class
        :return: List of Lists: [List of Notes, List of durations]
        """
        notes = []
        durations = []
        chord_and_dur_blocks = self.harmonic_rhythm.get_zipped_hr_chords_and_durations()
        beat_in_meter = 0
        for chord_and_dur_block_index in range(len(chord_and_dur_blocks)):
            for num_beats in range(chord_and_dur_blocks[chord_and_dur_block_index][1]):
                chord = chord_and_dur_blocks[chord_and_dur_block_index][0]
                accent_weight = self.harmonic_rhythm.meter.accent_weights[beat_in_meter]
                notes.append(self.get_next_note(chord, accent_weight, beat_in_meter))
                durations.append(self.note_duration)
                beat_in_meter = (beat_in_meter + 1) % self.harmonic_rhythm.meter.num_beats
        return [notes, durations]

    def get_next_note(self, chord: Chord, accent_weight: int, beat_in_meter: int):
        """
        Gets the next note in the alberti bass sequence based on the chord and the accent weight of the beat the
        note is falling on.
        :param chord: Chord
        :param accent_weight: int
        :param beat_in_meter: int
        :return: Note
        """
        if accent_weight == 3:
            try:
                return chord.get_bass_note()
            except Exception as error:
                print("Had an issue getting the bass note of this chord: ", error)
        else:
            return self.get_next_upper_alberti_note(chord, beat_in_meter=beat_in_meter)

    @staticmethod
    def get_next_upper_alberti_note(chord: Chord, beat_in_meter: int):
        """
        Helper function that slices for notes at specific indexes of chords based on the beat in the meter.
        :param chord: Chord
        :param beat_in_meter: int
        :return: Note
        """
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
    """
    SustainedBass class. Generates a bass line whose notes start at the beginning of each durational block associated
    with a chord in the input HarmonicRhythm object. Holds the note until a change in the harmonic rhythm.
    """
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        """
        Initializes SustainedBass class.
        :param harmonic_rhythm: HarmonicRhythm
        :param scale: Scale
        """
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        """
        Builds notes and durations for SustainedBass class.
        :return: List of Lists: [List of Notes, List of durations]
        """
        notes = []
        durations = []

        for i, chord in enumerate(self.harmonic_rhythm.progression.chords):
            notes.append(self.harmonic_rhythm.progression.chords[i].get_bass_note())
            durations.append(self.harmonic_rhythm.flattened_hr_durations[i])
        return [notes, durations]


class RandomBass(Bass):
    """
    RandomBass class. Generates a bass line whose durations are randomly selected (between 0.25 and 2 beats) for each
    chord and duration block in the HarmonicRhythm. The notes are always the bass note of the chord in the chord
    and duration block.
    """
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        """
        Initializes RandomBass music generator.
        :param harmonic_rhythm: HarmonicRhythm
        :param scale: Scale
        """
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        """
        Builds notes and durations for RandomBass class.
        :return: List of Lists: [List of Notes, List of durations]
        """
        notes = []
        durations = []

        for chord_and_dur_block in self.harmonic_rhythm.get_zipped_hr_chords_and_durations():
            duration_left = chord_and_dur_block[1]
            while duration_left > 0:
                if duration_left <= 0.05:
                    duration = duration_left
                else:
                    duration = random.uniform(0.05, duration_left)
                durations.append(self.make_note_or_rest(duration, 0.25))
                duration_left -= duration
                notes.append(chord_and_dur_block[0].get_bass_note())
        return [notes, durations]


class PolyrhythmicBass(Bass):
    """
    PolyrhythmicBass class. Builds a bassline by subdividing each chord and duration block into a random subdivision of
    durations as notes or rests. If the total duration of the chord and duration block is 2 and the subdivision is 5,
    each of the notes or rests will last 2/5 of a beat. Bass notes are selected as the bass note of the given chord
    from the chord and duration block.
    """
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        """
        Initialization for PolyrhythmicBass class
        :param harmonic_rhythm: HarmonicRhythm
        :param scale: Scale
        """
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        """
        Builds notes and durations for PolyrhythmicBass class.
        :return: List of Lists: [List of Notes, List of durations]
        """
        notes = []
        durations = []

        for chord_and_dur_block in self.harmonic_rhythm.get_zipped_hr_chords_and_durations():
            polyrhythm = subdivide_meter_into_polyrhythm(chord_and_dur_block[1], random.randint(3, 7))
            durations += polyrhythm
            notes += [chord_and_dur_block[0].get_bass_note() for _ in range(len(polyrhythm))]

        durations = [self.make_note_or_rest(duration) for duration in durations]
        return [notes, durations]


class OnBeatBass(Bass):
    """
    OnBeatBass class. Builds a bass line where each note lasts one beat, and attacks each time there is a change in the
    HarmonicRhythm chord and duration block.
    """
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        """
        Initialization for OnBeatBass class.
        :param harmonic_rhythm: HarmonicRhythm
        :param scale: Scale
        """
        super().__init__(harmonic_rhythm, scale)

    def build_notes_and_durations(self):
        """
        Builds notes and durations for OnBeatBass class.
        :return: List of Lists: [List of Notes, List of durations]
        """
        notes = []
        durations = []

        for chord_and_dur_block in self.harmonic_rhythm.get_zipped_hr_chords_and_durations():
            durations.append(1)
            if chord_and_dur_block[1] - 1 > 0:
                durations.append(self.build_rest(chord_and_dur_block[1] - 1))
            notes.append(chord_and_dur_block[0].get_bass_note())
        return [notes, durations]


class WalkingBass(Bass):
    """
    WalkingBass class. Builds a bass line by walking between the bass notes of each chord and duration block from
    the HarmonicRhythm. Walks either by chromatic step or scalar. On the anacrusis, will add in various tonicizations
    and extra rhythmic values to imitate improvisational playing.
    """
    def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
        """
        Initialization for WalkingBass class
        :param harmonic_rhythm: HarmonicRhythm
        :param scale: Scale
        """
        super().__init__(harmonic_rhythm, scale)

    @staticmethod
    def get_shortest_distance_data_chromatic(bn1: Note, bn2: Note):
        """
        Gets the shortest distance between two bass notes via chromatic step. Returns a dictionary with information
        that relates whether the bass line is ascending or descending, as well as the number of chromatic steps
        :param bn1: Note
        :param bn2: Note
        :return: Dict {str: boolean, str: int}
        """
        untransposed = bn2.midi_note_number - bn1.midi_note_number
        transposed = bn1.midi_note_number + 12 - bn2.midi_note_number
        if untransposed <= transposed:
            return {'ascending': True, 'steps': abs(bn2.midi_note_number - bn1.midi_note_number)}
        else:
            return {'ascending': False, 'steps': -(bn1.midi_note_number + 12 - bn2.midi_note_number)}

    def get_shortest_distance_data_scalar(self, bn1: Note, bn2: Note):
        """
        Gets the shortest distance between two bass notes via scalar step. If one of the bass notes is not in the scale
        step chromatically. Returns a dictionary with information that relates whether the bass line is ascending
        or descending, as well as the number of scalar steps.
        :param bn1: Note
        :param bn2: Note
        :return: Dict {str: boolean, str: int}
        """
        # TODO: Instead of stepping chromatically, get closest scalar note and step from there!
        if bn1 not in self.scale.notes or bn2 not in self.scale.notes:
            return self.get_shortest_distance_data_chromatic(bn1, bn2)
        if bn1 <= bn2:
            index_1 = self.scale.notes.index(bn1)
            index_2 = self.scale.notes.index(bn2)
        else:
            index_1 = self.scale.notes.index(bn2)
            index_2 = self.scale.notes.index(bn1)

        untransposed = index_1 - index_2
        transposed = index_1 + len(self.scale.notes) - index_2
        if abs(untransposed) <= abs(transposed):
            return {'ascending': True, 'steps': index_2 - index_1}
        else:
            return {'ascending': False, 'steps': -(index_1 + len(self.scale.notes) - index_2)}

    def step_between_notes_scalar(self, bn1: Note, distance_data: dict):
        """
        Steps between notes scale-wise. If there is an error and bassnote-1 is note in the scale, steps chromatically
        as a failsafe.
        :param bn1: Note
        :param distance_data: Dict {str: boolean, str: int}
        :return: List of Notes
        """
        if bn1 not in self.scale.notes:
            return self.step_between_notes_chromatic(bn1, distance_data)
        current_index = self.scale.notes.index(bn1)
        if distance_data['ascending']:
            return [self.scale.notes[(current_index + i) % len(self.scale.notes)] for i in
                    range(0, distance_data['steps'])]
        else:
            return [self.scale.notes[(current_index + i) % len(self.scale.notes)] for i in
                    range(0, distance_data['steps'], -1)]

    @staticmethod
    def step_between_notes_chromatic(bn1: Note, distance_data: dict):
        """
        Steps between notes chromatically.
        :param bn1: Note
        :param distance_data: Dict {str: boolean, str: int}
        :return: List of notes
        """
        if distance_data['ascending']:
            return [Note(bn1.midi_note_number + i) for i in range(0, distance_data['steps'])]
        else:
            return [Note(bn1.midi_note_number + i) for i in range(0, distance_data['steps'], -1)]

    def build_notes_and_durations(self):
        """
        Builds the notes and durations for the walking bass line. Algorithm loops through chords and durations,
        building notes by constructing step wise motion between bass notes of each chord and duration block in the
        harmonic rhythm.
        :return: List of Lists: [List of Notes, List of durations]
        """
        chords_and_durations = self.harmonic_rhythm.get_zipped_hr_chords_and_durations()

        notes = []
        durations = []
        # loop through chords and durations
        for count, chord_and_duration in enumerate(chords_and_durations):
            if count == len(chords_and_durations) - 1:
                # if count is length of array wrap up by calling end and beginning on progression
                notes_and_durations = self.build_notes_for_current_subdivision(chord_and_duration,
                                                                               chords_and_durations[0])
            else:
                notes_and_durations = self.build_notes_for_current_subdivision(chord_and_duration,
                                                                               chords_and_durations[count + 1])
            notes += notes_and_durations[0]
            durations += notes_and_durations[1]
        return [notes, durations]

    def choose_between_chromatic_and_scalar(self, chromatic_step: dict, scalar_step: dict, bn1: Note,
                                            chord_and_dur_block_duration: int, probability: float = 0.1):
        """
        Chooses between chromatic steps and scalar steps based on a probabilistic model. If the number of
        scalar steps is less than the duration of the chord and dur blocks, it is likely that the algorithm will
        then step chromatically (and vice-versa for when the scalar steps is greater than the duration of the
        chord and dur blocks).
        :param chromatic_step: int number of chromatic steps
        :param scalar_step: int number of scalar steps
        :param bn1: Note of bass note 1
        :param chord_and_dur_block_duration: int of duration from chord_and_dur_block
        :param probability: float
        :return: List of Notes
        """
        if abs(scalar_step['steps']) < chord_and_dur_block_duration:
            if random.random() < probability:
                return self.step_between_notes_scalar(bn1, scalar_step), 'scalar'
            else:
                return self.step_between_notes_chromatic(bn1, chromatic_step), 'chromatic'
        else:
            if random.random() < probability:
                return self.step_between_notes_chromatic(bn1, chromatic_step), 'chromatic'
            else:
                return self.step_between_notes_scalar(bn1, scalar_step), 'scalar'

    @staticmethod
    def next_beat_fourth_down_tonicization(duration: float, next_note: Note):
        """
        By looking ahead to the next note, inserts a note beforehand of *duration* value that is a fourth below
        the next note.
        :param duration: float || int
        :param next_note: Note
        :return: Tuple (Note, float || int)
        """
        return next_note - 5, duration

    @staticmethod
    def next_beat_leading_tone_tonicization(duration: float, next_note: Note):
        """
        By looking ahead to the next note, inserts a note beforehand of *duration* value that is a semitone below
        the next note.
        :param duration: float || int
        :param next_note: Note
        :return: Tuple (Note, float || int)
        """
        return next_note - 1, duration

    @staticmethod
    def next_beat_chromatic_upper_neighbor_tonicization(duration: float, next_note: Note):
        """
        By looking ahead to the next note, inserts a note beforehand of *duration* value that is a semitone above
        the next note.
        :param duration: float || int
        :param next_note: Note
        :return: Tuple (Note, float || int)
        """
        return next_note + 1, duration

    @staticmethod
    def next_beat_pass(duration: float, next_note: Note):
        """
        Conforms to the template by taking in duration and next_note and does nothing. Might be a better way to do
        this?
        :param duration: float || int
        :param next_note: Note
        :return: None
        """
        return None

    def build_notes_for_current_subdivision(self, current_chord_and_dur_block: tuple, next_chord_and_dur_block: tuple):
        """
        Builds the notes and durations for the current chord and dur block by looking ahead to the next
        chord and dur block.
        :param current_chord_and_dur_block: tuple (Chord, int)
        :param next_chord_and_dur_block: tuple (Chord, int)
        :return: List of Lists: [List of Notes, List of durations]
        """
        # choose between scalar and chromatic
        harmonic_rhythm_length = current_chord_and_dur_block[1]
        bn1 = current_chord_and_dur_block[0].get_bass_note()
        bn2 = next_chord_and_dur_block[0].get_bass_note()
        if bn1 == bn2:
            return self.same_chords(bn1, harmonic_rhythm_length)
        else:
            chrom = self.get_shortest_distance_data_chromatic(bn1, bn2)
            scalar = self.get_shortest_distance_data_scalar(bn1, bn2)
            steps = self.choose_between_chromatic_and_scalar(chrom, scalar, bn1, harmonic_rhythm_length, 0.2)
            notes = steps[0]
            durations = self.split_or_add_note_durations_by_duple_subdivisions(notes, harmonic_rhythm_length)
            # get last step in subdivision
            last_step = notes[-1]
            last_step_anacrusis = self.get_tonicization_function(last_step, bn2)(0.25, bn2)
            if last_step_anacrusis is not None:
                durations[-1] = durations[-1] - last_step_anacrusis[1]
                notes.append(last_step_anacrusis[0])
                durations.append(last_step_anacrusis[1])
            return notes, durations

    @staticmethod
    def split_or_add_note_durations_by_duple_subdivisions(steps: int, harmonic_rhythm_length: int):
        """
        Splits note durations or adds to them. When splitting a subdivisions, halves notes values until the value
        of sum(n_note_durations) == harmonic_rhythm_length. When adding value to the duration of each step,
        adds one quarter note in value to each duration until sum(n_note_durations) == harmonic_rhythm_length
        :param steps: int number of steps
        :param harmonic_rhythm_length: int duration of a chord and duration block
        :return: List of durations
        """
        n_note_durations = [1 for _ in range(len(steps))]
        if sum(n_note_durations) == harmonic_rhythm_length:
            return n_note_durations
        elif sum(n_note_durations) < harmonic_rhythm_length:
            i = 0
            while sum(n_note_durations) < harmonic_rhythm_length:
                n_note_durations[i] = n_note_durations[i] + 1
                i = (i + 1) % len(n_note_durations)
            return n_note_durations
        else:
            i = 0
            while sum(n_note_durations) > harmonic_rhythm_length:
                n_note_durations[i] = n_note_durations[i] / 2
                i = (i + 1) % len(n_note_durations)
            return n_note_durations

    @staticmethod
    def same_chords(bass_note: Note, harmonic_rhythm_length: int):
        """
        Returns n notes and durations of the same note when called.
        :param bass_note: Note
        :param harmonic_rhythm_length: int duration
        :return: List of Lists: [List of Notes, List of durations]
        """
        return [bass_note for _ in range(harmonic_rhythm_length)], [1 for _ in range(harmonic_rhythm_length)]

    def get_tonicization_function(self, last_step: Note, next_step: Note):
        """
        Gets a tonicization function based on a distributed weight. Weights are determined by some common gestures
        depending on the motion of the bass line. For steps l and n, if l > n, there is a possibility that the
        bass line will chromatically step down into n. This anacrusis, chromatic upper neighbor doesn't happen
        very often if the bass line is walking up.
        :param last_step: Note
        :param next_step: Note
        :return: function
        """
        if last_step > next_step:
            return random.choices(
                population=[
                    self.next_beat_fourth_down_tonicization,
                    self.next_beat_leading_tone_tonicization,
                    self.next_beat_chromatic_upper_neighbor_tonicization,
                    self.next_beat_pass
                ],
                weights=[20, 10, 15, 55],
                k=100
            )[0]
        else:
            return random.choices(
                population=[
                    self.next_beat_leading_tone_tonicization,
                    self.next_beat_fourth_down_tonicization,
                    self.next_beat_pass
                ],
                weights=[10, 10, 80],
                k=100
            )[0]

# TODO: Implement funk bass
# class FunkBass(Bass):
#     def __init__(self, harmonic_rhythm: HarmonicRhythm, scale: Scale):
#         super().__init__(harmonic_rhythm, scale)
#
#     def major3_to_5_chromatic(self):
#         tonic = self.scale.notes[0]
#         M3 = Note(tonic.midi_note_number + 4)
#         return [Note(i) for i in range(M3.midi_note_number, M3.midi_note_number + 3)]
#
#     def major6_to_8_chromatic(self):
#         tonic = self.scale.notes[0]
#         M6 = Note(tonic.midi_note_number + 9)
#         return [Note(i) for i in range(M6.midi_note_number, M6.midi_note_number + 3)]
#
#     def flat7_to_6(self):
#         tonic = self.scale.notes[0]
#         b7 = Note(tonic.midi_note_number + 10)
#         M6 = Note(tonic.midi_note_number +9)
#         return [b7, M6]
#
#     def major6_to_flat7(self):
#         tonic = self.scale.notes[0]
#         b7 = Note(tonic.midi_note_number + 10)
#         M6 = Note(tonic.midi_note_number +9)
#         return [M6, b7]
#
#     def two_eighths_on_the_one(self, chord_and_dur_block):
#         notes = [chord_and_dur_block[0].get_bass_note(), chord_and_dur_block[0].get_bass_note()]
#         durations = [0.5, 0.5]
#         return notes, durations
#
#     def heavy_on_the_one(self, chord_and_dur_block):
#         return [chord_and_dur_block[0].get_bass_note()], [self.harmonic_rhythm.meter.subdivisions[0]]
#
#     def on_the_one(self, chord_and_dur_block):
#         return random.choices(
#             population=[
#                 self.heavy_on_the_one,
#                 self.two_eighths_on_the_one
#             ],
#             weights=[50, 50],
#             k=100
#         )[0](chord_and_dur_block)
#
#     def next_duration_is_syncopation(self, durations):
#         if sum(durations) % 1 == 0:
#             return True
#         else:
#             return False


if __name__ == "__main__":
    from pythonosc import udp_client

    sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
    meter = ComplexMeter(7, [3, 1, 2, 1, 1, 2, 1], [2, 3, 2])
    duple = SimpleDuple(4)
    scale = Scale(Note(0), Note(2), Note(4), Note(5), Note(7), Note(9), Note(11))
    blues_scale = Scale(Note(0), Note(2), Note(3), Note(4), Note(5), Note(7), Note(9), Note(10), Note(11))
    whole_tone_scale = Scale(Note(0), Note(2), Note(4), Note(6), Note(8), Note(10))
    c_major = Chord(Note(0), Note(4), Note(7))
    CM7 = Chord(Note(0), Note(4), Note(7), Note(11))
    Cmm7 = Chord(Note(0), Note(3), Note(7), Note(10))
    a = Chord(Note(9), Note(0), Note(4))
    G7 = Chord(Note(7), Note(11), Note(14), Note(17))
    e = Chord(Note(4), Note(7), Note(11))
    b = Chord(Note(11), Note(2), Note(5))
    chords = [c_major, CM7, Cmm7, a, G7, e, b]
    meter1 = ComplexMeter(7, [3, 1, 2, 1, 1, 2, 1], [2, 3, 2])
    meter2 = CompoundMeter(9, [3, 1, 1, 2, 1, 1, 2, 1, 1], [3, 3, 3])
    meter3 = SimpleDuple(4)
    meter4 = SimpleDuple(2)
    meter5 = SimpleTriple()

    random.shuffle(chords)
    prog = ChordProgression(chords)
    hr = HarmonicRhythm(meter5, prog)
    sb = WalkingBass(hr, blues_scale)
    ab = AlbertiBass(hr, scale)
    print(ab.notes_and_durations)
    print(ab.harmonic_rhythm.get_zipped_hr_chords_and_durations())
    # send_bass_or_melody_notes_to_sc(sb, sc_client, "/bass_notes")
    # send_bass_or_melody_durations_to_sc(sb, sc_client, '/bass_durations')
    # send_bass_or_melody_initialization_to_sc(0, sc_client, '/bass_init')
    #
    # for i in range(100):
    #     random.shuffle(chords)
    #     prog = random.choice([ChordProgression(chords), cybernetic_republic_progressions['changes']])
    #     hr = HarmonicRhythm(random.choice([meter1, meter2, meter3, meter4, meter5]), prog)
    #     ab = AlbertiBass(hr, scale)
    #     # rb = RandomBass(hr, scale)
    #     # pr = PolyrhythmicBass(hr, scale)
    #     # obb = OnBeatBass(hr, scale)
    #     wb = WalkingBass(hr, scale)
    #     for i in [ab]:
    #         print("name: {}, sum durations: {}, total beats: {}, meter beats: {}, notes and durations: {}".format(i.__class__.__name__,
    #                                                                     i.sum_with_rests(i.notes_and_durations[1]),
    #                                                                     i.harmonic_rhythm.meter.num_beats * i.harmonic_rhythm.num_bars,
    #                                                                                      i.harmonic_rhythm.meter.num_beats,
    #                                                                                                               i.notes_and_durations)
    #              )

