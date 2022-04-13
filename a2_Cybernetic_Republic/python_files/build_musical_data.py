from Data_Dumps.progession_data import cybernetic_republic_progressions
from Data_Dumps.meter_data import cybernetic_republic_meter_data
from Data_Dumps.melody_data import cybernetic_republic_melodies
from Data_Dumps.bass_data import cybernetic_republic_basses
from Data_Dumps.middle_voices_data import cybernetic_republic_middle_voices
from Data_Dumps.rhythm_section_data import cybernetic_republic_rhythm_section
from Classes.harmonic_rhythm import HarmonicRhythm
from Classes.melody import *


def build_cybernetic_harmonic_rhythm(meter_key, progression_key):
    return HarmonicRhythm(cybernetic_republic_meter_data[meter_key], cybernetic_republic_progressions[progression_key])


def build_melody(melody_key, harmonic_rhythm, scale):
    return cybernetic_republic_melodies[melody_key](harmonic_rhythm, scale)


def build_bass(bass_key, harmonic_rhythm, scale):
    return cybernetic_republic_basses[bass_key](harmonic_rhythm, scale)


def build_middle_voices(middle_voices_key, harmonic_rhythm):
    return cybernetic_republic_middle_voices[middle_voices_key](harmonic_rhythm)


def build_rhythm_section(rhythm_section_key, meter):
    return cybernetic_republic_rhythm_section[rhythm_section_key](meter)
