from Classes.scale import Scale
from Data_Dumps.progession_data import cybernetic_republic_progressions
from Data_Dumps.progession_data import cybernetic_republic_intro_progression
from Data_Dumps.melody_data import cybernetic_republic_melodies
from Data_Dumps.bass_data import cybernetic_republic_basses
from Data_Dumps.bass_data import cybernetic_republic_intro_bass
from Data_Dumps.middle_voices_data import cybernetic_republic_middle_voices
from Data_Dumps.rhythm_section_data import cybernetic_republic_rhythm_section
from Data_Dumps.rhythm_section_data import cybernetic_republic_intro_rhythm_section
from Data_Dumps.meter_data import cybernetic_republic_meter_data
from Classes.harmonic_rhythm import HarmonicRhythm


def build_harmonic_rhythm(meter_key: str, progression_key: str):
    """
    Builds a HarmonicRhythm object based on a given meter_key and progression_key. Objects associated with
    keys come from Data_Dumps.meter_data and Data_Dumps.progression_data
    :param meter_key: str
    :param progression_key: str
    :return: HarmonicRhythm
    """
    if progression_key == 'introduction':
        return HarmonicRhythm(cybernetic_republic_meter_data[meter_key],
                              cybernetic_republic_intro_progression[progression_key])
    else:
        return HarmonicRhythm(cybernetic_republic_meter_data[meter_key], cybernetic_republic_progressions[progression_key])


def build_melody(melody_key: str, harmonic_rhythm: HarmonicRhythm, scale: Scale):
    """
    Builds a Melody object based on a given melody_key and passed in HarmonicRhythm and Scale. Objects associated with
    keys come from Data_Dumps.melody_data
    :param melody_key: str
    :param harmonic_rhythm: HarmonicRhythm
    :param scale: Scale
    :return: Melody
    """
    return cybernetic_republic_melodies[melody_key](harmonic_rhythm, scale)


def build_bass(bass_key: str, harmonic_rhythm: HarmonicRhythm, scale: Scale):
    """
    Builds a Bass object based on a given bass_key and passed in HarmonicRhythm and Scale. Objects associated with
    keys come from Data_Dumps.bass_data
    :param bass_key: str
    :param harmonic_rhythm: HarmonicRhythm
    :param scale: Scale
    :return: Bass
    """
    if bass_key == 'introduction':
        return cybernetic_republic_intro_bass[bass_key](harmonic_rhythm, scale)
    else:
        return cybernetic_republic_basses[bass_key](harmonic_rhythm, scale)


def build_middle_voices(middle_voices_key: str, harmonic_rhythm: HarmonicRhythm):
    """
    Builds a MiddleVoices object based on a given middle_voices_key and HarmonicRhythm object. Objects associated with
    keys come from Data_Dumps.middle_voices_data
    :param middle_voices_key: str
    :param harmonic_rhythm: HarmonicRhythm
    :return: MiddleVoices
    """
    return cybernetic_republic_middle_voices[middle_voices_key](harmonic_rhythm)


def build_rhythm_section(rhythm_section_key: str, meter_key: str):
    """
    Builds a RhythmSection object based on a given rhythm_section_key and meter_key. Objects associated with
    keys come from Data_Dumps.meter_data and Data_Dumps.rhythm_section_data
    :param rhythm_section_key: str
    :param meter_key: str
    :return: RhythmSection
    """
    if rhythm_section_key == 'introduction':
        return cybernetic_republic_intro_rhythm_section[rhythm_section_key](cybernetic_republic_meter_data[meter_key])
    else:
        return cybernetic_republic_rhythm_section[rhythm_section_key](cybernetic_republic_meter_data[meter_key])


def build_meter(meter_key: str):
    """
    Builds a Meter object based on a given meter_key. Objects associated with key comes from Data_Dumps.meter_data
    :param meter_key: str
    :return: Meter
    """
    return cybernetic_republic_meter_data[meter_key]


def build_progression(progression_key: str):
    """
    Builds a Progression object based on a given progression_key. Objects associated with key comes from
    Data_Dumps.progression_data
    :param progression_key: str
    :return: Progression
    """
    return cybernetic_republic_progressions[progression_key]