from pythonosc import udp_client
from pythonosc import osc_message_builder


def send_middle_voice_chords_to_sc(middle_voices, sc_client, address='/middle_voice_chords'):
    for chord in middle_voices.chords_and_durations[0]:
        msg = osc_message_builder.OscMessageBuilder(address=address)
        for note in chord.notes:
            msg.add_arg(note.midi_note_number, 'i')
        msg = msg.build()
        sc_client.send(msg)


def send_middle_voice_durations_to_sc(middle_voices, sc_client, address='/middle_voice_durations'):
    msg = osc_message_builder.OscMessageBuilder(address=address)
    for duration in middle_voices.chords_and_durations[1]:
        msg.add_arg(duration, 'f')
    msg = msg.build()
    sc_client.send(msg)


def send_middle_voice_initialization_to_sc(channel, sc_client, address='/middle_voice_init'):
    msg = osc_message_builder.OscMessageBuilder(address=address)
    msg.add_arg(channel, arg_type='i')
    msg = msg.build()
    sc_client.send(msg)


def send_rhythm_to_sc(rhythm_section, sc_client, address="/break_beat_1"):
    for i in range(len(rhythm_section.midi_notes)):
        msg = osc_message_builder.OscMessageBuilder(address=address)
        msg.add_arg(rhythm_section.midi_notes[i], 'i')
        for note_event in rhythm_section.midi_note_duration_arrays[i]:
            msg.add_arg(note_event)
        msg = msg.build()
        sc_client.send(msg)

    msg = osc_message_builder.OscMessageBuilder(address="/init")
    msg.add_arg("break_beat_1")
    msg.add_arg("rhythm_pattern")
    msg = msg.build()
    sc_client.send(msg)