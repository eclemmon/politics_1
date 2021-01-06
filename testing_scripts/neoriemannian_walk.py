from pythonosc import udp_client
from pythonosc import osc_message_builder
import time
import neo_riemannian_web
from chord import Chord
from note import Note

def generate_pitch_materials(web, octave):
    chords = []
    chords.append(web.current_chord)
    for chord in web.web[web.current_chord]:
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
    client.send(msg)
    time.sleep(0.1)




if __name__ == "__main__":
    client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
    starting_chord = Chord(Note(60), Note(64), Note(67))
    web = neo_riemannian_web.NeoriemannianWeb(starting_chord)
    web.build_web()
    print(generate_pitch_materials(web, 4))
    send_pitch_materials(generate_pitch_materials(web, 4))
