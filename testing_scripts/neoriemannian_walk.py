from pythonosc import udp_client
from pythonosc import osc_message_builder
import time
import neo_riemannian_web
from chord import Chord
from note import Note

def generate_pitch_materials(web, octave, current_chord):
    chords = []
    chords.append(current_chord)
    for chord in web.web[current_chord]:
        chords.append(chord)
    return [[note.midi_note_number + 12 * octave for note in chord.notes] for chord in chords]

def send_pitch_materials(notes):
    msg = osc_message_builder.OscMessageBuilder(address='/s_new')
    chord_names = ['Q', 'L', 'P', 'R']
    for index in range(len(chord_names)):
        msg.add_arg(chord_names[index], arg_type='s')
        for note in notes[index]:
            msg.add_arg(note)
    msg = msg.build()
    print(msg.params)
    client.send(msg)
    time.sleep(0.1)

def random_walk_only_new(num_chords_walked, neo_rweb, octave=None, time_interval=None):
    if octave is None:
        octave = 5

    if time_interval is None:
        time_interval = 5

    chords = [neo_rweb.current_chord] + neo_rweb.random_walk_only_new(num_chords_walked)
    for chord in chords:
        send_pitch_materials(generate_pitch_materials(neo_rweb, octave, chord))
        time.sleep(time_interval)





if __name__ == "__main__":
    client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
    starting_chord = Chord(Note(60), Note(64), Note(67))
    web = neo_riemannian_web.NeoriemannianWeb(starting_chord)
    web.build_web()
    # print(generate_pitch_materials(web, 4))
    # send_pitch_materials(generate_pitch_materials(web, 4))
    random_walk_only_new(4, web, time_interval=3)

