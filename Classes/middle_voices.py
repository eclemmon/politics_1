import random

from Classes import harmonic_rhythm
from Classes import meter
from Classes import chord_progression
from Data_Dumps.harmonic_progession_data import cybernetic_republic_progressions


class MiddleVoices:
    def __init__(self, harmonic_rhythm_object: harmonic_rhythm.HarmonicRhythm, octave=4):
        self.harmonic_rhythm = harmonic_rhythm_object
        self.instrument_channels = [channel for channel in range(16)]
        self.harmonic_rhythm.progression.transpose(octave)
        # print(self.harmonic_rhythm.progression.chords)
        self.chords_and_durations = self.build_chords_and_durations()

    def build_chords_and_durations(self):
        pass

    def build_next_temporal_unit(self):
        pass

    def get_random_instrument_channel(self):
        return random.choice(self.instrument_channels)

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


class Pads(MiddleVoices):
    def __init__(self, harmonic_rhythm_object, octave=5):
        super().__init__(harmonic_rhythm_object, octave)

    def build_chords_and_durations(self):
        return self.harmonic_rhythm.get_chords_and_durations()


class RandomMiddleVoices(MiddleVoices):
    def __init__(self, harmonic_rhythm_object, octave=4):
        super().__init__(harmonic_rhythm_object, octave)

    def build_chords_and_durations(self):
        chords = []
        durations = []
        for chord_and_dur_block in self.harmonic_rhythm.get_zipped_hr_chords_and_durations():
            duration_left = chord_and_dur_block[1]
            while duration_left > 0:
                duration = random.uniform(0.05, duration_left)
                durations.append(self.make_note_or_rest(duration, 0.25))
                duration_left -= duration
                chords.append(chord_and_dur_block[0])
        return [chords, durations]


class OffBeatMiddleVoices(MiddleVoices):
    def __init__(self, harmonic_rhythm_object, octave=4):
        super().__init__(harmonic_rhythm_object, octave)

    def build_chords_and_durations(self):
        chords = []
        durations = []
        beat_in_meter = 0

        for chord_and_dur_block in self.harmonic_rhythm.get_zipped_hr_chords_and_durations():
            total_beats = chord_and_dur_block[1]
            beat = 0
            while beat < total_beats:
                accent_index = beat_in_meter % len(self.harmonic_rhythm.meter.accent_weights)
                chords.append(chord_and_dur_block[0])
                if self.harmonic_rhythm.meter.accent_weights[accent_index] > 1:
                    durations.append(self.build_rest())
                else:
                    durations.append(1)
                beat += 1
                beat_in_meter += 1
        return [chords, durations]


class ArpeggiatedMiddleVoices(Pads):
    def __init__(self, harmonic_rhythm_object, octave=5):
        super().__init__(harmonic_rhythm_object, octave)


class ChoppyMiddleVoices(Pads):
    def __init__(self, harmonic_rhythm_object, octave=5):
        super().__init__(harmonic_rhythm_object, octave)

    def build_chords_and_durations(self):
        note_values = [0.25, 0.5, 0.75, 1]
        chords = []
        durations = []

        for chord_and_dur_block in self.harmonic_rhythm.get_zipped_hr_chords_and_durations():
            duration_left = chord_and_dur_block[1]
            while duration_left > 0:
                duration = random.choice(note_values)
                durations.append(self.make_note_or_rest(duration, 0.33))
                duration_left -= duration
                chords.append(chord_and_dur_block[0])
        return [chords, durations]


if __name__ == "__main__":
    from a2_Cybernetic_Republic.python_files.send_to_sc_functions import *
    from pythonosc import udp_client

    sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

    meter = meter.ComplexMeter(5, [3,1,2,1,1], [2, 3])
    hr = harmonic_rhythm.HarmonicRhythm(meter, cybernetic_republic_progressions['giant-steps'])
    # pads = Pads(hr)

    # rand = RandomMiddleVoices(hr)
    # offbeat = OffBeatMiddleVoices(hr)
    # arp = ArpeggiatedMiddleVoices(hr)
    chop = ChoppyMiddleVoices(hr)
    print(chop.chords_and_durations)

    send_middle_voice_chords_to_sc(chop, sc_client)
    send_middle_voice_durations_to_sc(chop, sc_client)
    send_middle_voice_initialization_to_sc(chop.get_random_instrument_channel(), sc_client)
    # send_arpeggiator_on_off_to_sc(sc_client)




