from pythonosc import udp_client
from pythonosc import osc_message_builder
import time
from harmonic_graph_constructors import neo_riemannian_web
from chord import Chord
from note import Note


# noinspection PyShadowingNames
def generate_pitch_materials(web: neo_riemannian_web.NeoriemannianWeb, octave, current_chord):
    """
    This helper functionfunction simply returns an array of midi note numbers according to
    the input chord.
    :param web: neo-Riemannian web object.
    :param octave: Which octave the desired midi note numbers should be transposed to.
    :param current_chord: a major or minor triad as a Chord object.
    :return: Returns an array of midi note numbers.
    """
    chords = [current_chord]
    for chord in web.web[current_chord]:
        chords.append(chord)
    return [[note.midi_note_number + 12 * octave for note in chord.notes] for chord in chords]


def send_pitch_materials(notes):
    """
    Builds pitch materials into an OSC message, send to SuperCollider.
    :param notes: Notes array of arrays generated by generate_pitch_materials helper function.
    """
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
    """
    Function that walks randomly through neo_rweb (neo-Riemannian web object), selects
    Chord objects that have not been visited yet and sends their pitch materials to SC.
    :param num_chords_walked: Number of chords to be passed to SC.
    :param neo_rweb: neoRiemannianWeb object.
    :param octave: The octave to transpose midi note values to.
    :param time_interval: The frequency that send_pitch_materials is called.
    """
    if octave is None:
        octave = 5

    if time_interval is None:
        time_interval = 5

    chords = [neo_rweb.current_chord] + neo_rweb.random_walk_only_new(num_chords_walked)
    for chord in chords:
        print("The original form of the chord is: ")
        print(chord)
        print("The Transformations are: ")
        send_pitch_materials(generate_pitch_materials(neo_rweb, octave, chord))
        time.sleep(time_interval)


if __name__ == "__main__":
    print("Building UDP Client")
    time.sleep(2)
    client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
    print("Done")
    time.sleep(1)
    print("Initializing neo-RiemannianWeb from C-Major Chord")
    starting_chord = Chord(Note(61), Note(64), Note(67))
    web = neo_riemannian_web.NeoriemannianWeb(starting_chord)
    web.build_web()
    time.sleep(2)
    print("Done")
    time.sleep(1)
    # print(generate_pitch_materials(web, 4))
    # send_pitch_materials(generate_pitch_materials(web, 4))
    print("Walking through web and sending to SuperCollider")
    random_walk_only_new(10, web, time_interval=12)
    print("Web traversed, ending process")
