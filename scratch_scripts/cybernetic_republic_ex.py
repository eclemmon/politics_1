"""
cybernetic_republic_ex.py
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2022, Eric Lemmon"
__credits__ = ["Eric Lemmon"]
__version__ = ""
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Production"

from Classes.chord import Chord
from Classes.scale import Scale
from Classes.meter import ComplexMeter
from Classes.note import Note
from Classes.meter import CompoundMeter
from Classes.harmonic_rhythm import HarmonicRhythm
from Data_Dumps.rhythm_section_data import TakeFive
from Data_Dumps.progession_data import cybernetic_republic_progressions
from Data_Dumps.melody_data import cybernetic_republic_melodies
from a2_Cybernetic_Republic.python_files.build_music_generator_objects import *
from a2_Cybernetic_Republic.python_files.send_to_sc_functions import *
from pythonosc import udp_client
import time

complex = ComplexMeter(5, [3, 1, 1, 2, 1], [3, 2])
# compound = CompoundMeter(9, [3, 1, 1, 2, 1, 1, 2, 1, 1], [3, 3, 3])
progression = cybernetic_republic_progressions['lament']
hr = HarmonicRhythm(complex, progression)
scale_hm = Scale(Note(0), Note(2), Note(3), Note(5), Note(7), Note(8), Note(11))
scale_m = Scale(Note(0), Note(2), Note(4), Note(5), Note(7), Note(9), Note(11))

melody = build_melody('max-ornament', hr, scale_hm)

sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

send_bass_or_melody_notes_to_sc(melody, sc_client, '/melody_notes')
send_bass_or_melody_durations_to_sc(melody, sc_client, '/melody_durations')
send_bass_or_melody_initialization_to_sc(5, sc_client, '/melody_init')

# send_rhythm_to_sc(tf5, sc_client)
# send_rhythm_initialization_to_sc(sc_client)
# time.sleep(10)
# send_rhythm_to_sc(tf9, sc_client)
# send_rhythm_initialization_to_sc(sc_client)

