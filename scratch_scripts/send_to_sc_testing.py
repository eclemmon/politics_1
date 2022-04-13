from a2_Cybernetic_Republic.python_files.build_musical_data import *
from a2_Cybernetic_Republic.python_files.send_to_sc_functions import *
from Data_Dumps.bass_data import cybernetic_republic_basses
from Data_Dumps.melody_data import cybernetic_republic_melodies
from Data_Dumps.meter_data import cybernetic_republic_meter_data
from Data_Dumps.progession_data import cybernetic_republic_progressions
from Data_Dumps.rhythm_section_data import cybernetic_republic_rhythm_section

hr = build_harmonic_rhythm('four', 'chromatic-lament')
bass = build_bass('walking')
melody = build_melody('choppy', hr)
