from Classes.harmonic_rhythm import HarmonicRhythm
from Classes.chord_progression import ChordProgression
from Classes.scale import Scale
from Classes.meter import *
from Classes.note import Note
from Rhythm_Generators.subdivision_generator import subdivide_meter_into_polyrhythm
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
                if duration_left <= 0.05:
                    duration = duration_left
                else:
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
            polyrhythm = subdivide_meter_into_polyrhythm(chord_and_dur_block[1], random.randint(3, 7))
            durations += polyrhythm
            notes += [chord_and_dur_block[0].get_bass_note() for _ in range(len(polyrhythm))]

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
            return {'ascending': True, 'steps': abs(bn2.midi_note_number - bn1.midi_note_number)}
        else:
            return {'ascending': False, 'steps': -(bn1.midi_note_number + 12 - bn2.midi_note_number)}

    def get_shortest_distance_data_scalar(self, bn1: Note, bn2: Note):
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

    def step_between_notes_scalar(self, bn1, distance_data):
        current_index = self.scale.notes.index(bn1)
        if distance_data['ascending']:
            return [self.scale.notes[(current_index + i) % len(self.scale.notes)] for i in
                    range(0, distance_data['steps'])]
        else:
            return [self.scale.notes[(current_index + i) % len(self.scale.notes)] for i in
                    range(0, distance_data['steps'], -1)]

    def step_between_notes_chromatic(self, bn1, distance_data):
        if distance_data['ascending']:
            return [Note(bn1.midi_note_number + i) for i in range(0, distance_data['steps'])]
        else:
            return [Note(bn1.midi_note_number + i) for i in range(0, distance_data['steps'], -1)]

    def build_notes_and_durations(self):
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

    def choose_between_chromatic_and_scalar(self, chromatic_step, scalar_step, bn1, hr_length, probability=0.1):
        if abs(scalar_step['steps']) < hr_length:
            if random.random() < probability:
                return self.step_between_notes_scalar(bn1, scalar_step), 'scalar'
            else:
                return self.step_between_notes_chromatic(bn1, chromatic_step), 'chromatic'
        else:
            if random.random() < probability:
                return self.step_between_notes_chromatic(bn1, chromatic_step), 'chromatic'
            else:
                return self.step_between_notes_scalar(bn1, scalar_step), 'scalar'

    def next_beat_fourth_down_tonicization(self, duration, next_note):
        return next_note - 5, duration

    def next_beat_leading_tone_tonicization(self, duration, next_note):
        return next_note - 1, duration

    def next_beat_chromatic_upper_neighbor_tonicization(self, duration, next_note):
        return next_note + 1, duration

    def next_beat_pass(self, duration, next_note):
        return None

    def build_notes_for_current_subdivision(self, current_chord_and_dur_block, next_chord_and_dur_block):
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
            durations = self.split_note_durations_by_duple_subdivisions(notes, harmonic_rhythm_length)
            # get last step in subdivision
            last_step = notes[-1]
            last_step_anacruxis = self.get_tonicization_function(last_step, bn2)(0.25, bn2)
            if last_step_anacruxis is not None:
                durations[-1] = durations[-1] - last_step_anacruxis[1]
                notes.append(last_step_anacruxis[0])
                durations.append(last_step_anacruxis[1])
            return notes, durations

    def split_note_durations_by_duple_subdivisions(self, steps, harmonic_rhythm_length):
        basic_subdivision = [1 for _ in range(len(steps))]
        if sum(basic_subdivision) == harmonic_rhythm_length:
            return basic_subdivision
        elif sum(basic_subdivision) < harmonic_rhythm_length:
            i = 0
            while sum(basic_subdivision) < harmonic_rhythm_length:
                basic_subdivision[i] = basic_subdivision[i] + 1
                i = (i + 1) % len(basic_subdivision)
            return basic_subdivision
        else:
            i = 0
            while sum(basic_subdivision) > harmonic_rhythm_length:
                basic_subdivision[i] = basic_subdivision[i] / 2
                i = (i + 1) % len(basic_subdivision)
            return basic_subdivision

    def same_chords(self, bass_note, harmonic_rhythm_length):
        return [bass_note for _ in range(harmonic_rhythm_length)], [1 for _ in range(harmonic_rhythm_length)]

    def get_tonicization_function(self, last_step, next_step):
        if last_step > next_step:
            return random.choices(
                population=[
                    self.next_beat_fourth_down_tonicization,
                    self.next_beat_leading_tone_tonicization,
                    self.next_beat_chromatic_upper_neighbor_tonicization,
                    self.next_beat_pass
                ],
                weights=[10, 10, 5, 75],
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
    from a2_Cybernetic_Republic.python_files.send_to_sc_functions import *
    from pythonosc import udp_client

    sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

    # def sum_with_rests(durations):
    #     res = []
    #     for dur in durations:
    #         if type(dur) == str:
    #             res.append(float(dur[2:]))
    #         else:
    #             res.append(dur)
    #     return sum(res)
    meter = ComplexMeter(7, [3, 1, 2, 1, 1, 2, 1], [2, 3, 2])
    duple = SimpleDuple(4)
    scale = Scale(Note(0), Note(2), Note(4), Note(5), Note(7), Note(9), Note(11))
    blues_scale = Scale(Note(0), Note(2), Note(3), Note(4), Note(5), Note(7), Note(9), Note(10), Note(11))
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

    random.shuffle(chords)
    prog = ChordProgression(chords)
    hr = HarmonicRhythm(random.choice([meter1, meter2, meter3]), prog)
    sb = SustainedBass(hr, scale)
    send_bass_or_melody_notes_to_sc(sb, sc_client, "/bass_notes")
    send_bass_or_melody_durations_to_sc(sb, sc_client, '/bass_durations')

    # for i in range(100):
    #     random.shuffle(chords)
    #     prog = ChordProgression(chords)
    #     hr = HarmonicRhythm(random.choice([meter1, meter2, meter3]), prog)
    #     ab = SustainedBass(hr, scale)
    #     rb = RandomBass(hr, scale)
    #     pr = PolyrhythmicBass(hr, scale)
    #     obb = OnBeatBass(hr, scale)
    #     wb = WalkingBass(hr, scale)
    #     for i in [ab, rb, pr, obb, wb]:
    #         print("name: {}, sum durations: {}, total beats: {}, meter beats: {}".format(i.__class__.__name__,
    #                                                                     sum_with_rests(i.notes_and_durations[1]),
    #                                                                     i.harmonic_rhythm.meter.num_beats * i.harmonic_rhythm.num_bars,
    #                                                                                      i.harmonic_rhythm.meter.num_beats)
    #              )

