from a2_Cybernetic_Republic.python_files.build_musical_data import *
from a2_Cybernetic_Republic.python_files.send_to_sc_functions import *
from Data_Dumps.scale_data import cybernetic_republic_scales
from pythonosc import udp_client

sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

hr = build_harmonic_rhythm('five-2+3', 'giant-steps')
bass = build_bass('sustained', hr, cybernetic_republic_scales['major'])
melody = build_melody('leapy', hr, cybernetic_republic_scales['major'])
rhythm = build_rhythm_section('take-five', 'five-2+3')
middle_voices = build_middle_voices('pads', hr)

send_rhythm_to_sc(rhythm, sc_client)
send_rhythm_initialization_to_sc(sc_client)
send_bass_or_melody_notes_to_sc(bass, sc_client, '/bass_notes')
send_bass_or_melody_durations_to_sc(bass, sc_client, '/bass_durations')
send_bass_or_melody_initialization_to_sc(0, sc_client, '/bass_init')

send_bass_or_melody_notes_to_sc(melody, sc_client, '/melody_notes')
send_bass_or_melody_durations_to_sc(melody, sc_client, '/melody_durations')
send_bass_or_melody_initialization_to_sc(0, sc_client, '/melody_init')

send_middle_voice_chords_to_sc(middle_voices, sc_client)
send_middle_voice_durations_to_sc(middle_voices, sc_client)
send_middle_voice_initialization_to_sc(0, sc_client)