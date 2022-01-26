import itertools

from pythonosc import osc_message_builder
from Utility_Tools.logistic_function import linear_to_logistic as l2l

import Harmonic_Graph_Constructors.harmonic_web


def generate_pitch_materials(web: Harmonic_Graph_Constructors.harmonic_web.HarmonicWeb, octave, current_chord):
    """
    This helper function simply returns an array of midi note numbers according to
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


def send_chord_materials(notes, client, time_interval, harmonic_rhythm):
    """
    Builds pitch materials into an OSC message, send to SuperCollider.
    :param harmonic_rhythm: The length of the formal structure in time over which the harmonies change.
    :param time_interval: The time interval by which chords advance
    :param notes: Notes array of arrays generated by generate_pitch_materials helper function.
    :param client: OSC client
    :return:
    """
    msg = osc_message_builder.OscMessageBuilder(address='/harmonic_materials')
    pitches = list(itertools.chain(*[note for chord in notes for note in chord]))
    msg.add_arg(harmonic_rhythm, arg_type='f')
    msg.add_arg(time_interval, arg_type='f')
    for pitch in pitches:
        msg.add_arg(pitch, arg_type='i')
    msg = msg.build()
    # print(msg.params)
    client.send(msg)


def random_walk_only_new(num_chords_walked, harmonic_web, client, octave=None, time_interval=None,
                         harmonic_rhythm=None):
    """
    Function that walks randomly through a harmonic web object, selects
    Chord objects that have not been visited yet and sends their pitch materials to SC.
    :param client:
    :param harmonic_rhythm:
    :param num_chords_walked: Number of chords to be passed to SC.
    :param harmonic_web: Harmonic Web object.
    :param octave: The octave to transpose midi note values to.
    :param time_interval: The frequency that send_pitch_materials is called.
    """
    if octave is None:
        octave = 5

    if time_interval is None:
        time_interval = 5

    if harmonic_rhythm is None:
        harmonic_rhythm = 5

    chords = harmonic_web.random_walk_only_new(num_chords_walked)
    schedule_chords(chords, time_interval, harmonic_rhythm, harmonic_web, octave, client)


def schedule_chords(chords, time_interval, harmonic_rhythm, chord_graph, octave, client):
    pitch_materials = []
    for chord in chords:
        pitch_materials.append(generate_pitch_materials(chord_graph, octave, chord))
    send_chord_materials(pitch_materials, client, time_interval, harmonic_rhythm)


def num_chords_walked(lev_mean, lev_standard_of_deviation):
    return int(l2l(abs(lev_mean), 0, 100, 0, 10, lev_standard_of_deviation))