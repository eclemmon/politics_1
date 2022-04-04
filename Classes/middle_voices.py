import random

from Classes import harmonic_rhythm
from Classes import meter
from Classes import chord_progression
from Data_Dumps.harmonic_progession_data import cybernetic_republic_harmonic_progressions


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

    def get_random_instrument_channel(self):
        return random.choice(self.instrument_channels)


if __name__ == "__main__":
    from a2_Cybernetic_Republic.python_files.send_to_sc_functions import *
    from pythonosc import udp_client

    sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

    meter = meter.ComplexMeter(5, [3,1,2,1,1], [2, 3])
    hr = harmonic_rhythm.HarmonicRhythm(meter, cybernetic_republic_harmonic_progressions['giant-steps'])
    pads = Pads(hr)
    print(pads.chords_and_durations)

    send_middle_voice_chords_to_sc(pads, sc_client)
    send_middle_voice_durations_to_sc(pads, sc_client)
    send_middle_voice_initialization_to_sc(pads.get_random_instrument_channel(), sc_client)





