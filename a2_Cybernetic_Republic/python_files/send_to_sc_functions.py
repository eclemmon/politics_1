from pythonosc import udp_client
from pythonosc import osc_message_builder
from typing import Union

from Classes.bass import Bass
from Classes.melody import Melody
from Classes.middle_voices import MiddleVoices
from Classes.rhythm_section import RhythmSection


def send_middle_voice_chords_to_sc(middle_voices: MiddleVoices, sc_client: udp_client.SimpleUDPClient,
                                   address: str = '/middle_voice_chords'):
    """
    Function to send chords from MiddleVoices object over to SuperCollider for sequencing.
    :param middle_voices: MiddleVoices
    :param sc_client: SimpleUDPClient
    :param address: str
    :return: None
    """
    for chord in middle_voices.chords_and_durations[0]:
        msg = osc_message_builder.OscMessageBuilder(address=address)
        for note in chord.notes:
            msg.add_arg(note.midi_note_number, 'i')
        msg = msg.build()
        sc_client.send(msg)


def send_middle_voice_durations_to_sc(middle_voices: MiddleVoices, sc_client: udp_client.SimpleUDPClient,
                                      address: str = '/middle_voice_durations'):
    """
    Function to send durations from MiddleVoices object over to SuperCollider for sequencing.
    :param middle_voices: MiddleVoices
    :param sc_client: SimpleUDPClient
    :param address: str
    :return: None
    """
    msg = osc_message_builder.OscMessageBuilder(address=address)
    for duration in middle_voices.chords_and_durations[1]:
        msg.add_arg(duration)
    msg = msg.build()
    sc_client.send(msg)


def send_middle_voice_initialization_to_sc(channel: int, sc_client: udp_client.SimpleUDPClient,
                                           address: str = '/middle_voice_init'):
    """
    Function to initialize middle voices pattern in SuperCollider.
    :param channel: int
    :param sc_client: SimpleUDPClient
    :param address: str
    :return: None
    """
    msg = osc_message_builder.OscMessageBuilder(address=address)
    msg.add_arg(channel, arg_type='i')
    msg = msg.build()
    sc_client.send(msg)


def send_bass_or_melody_notes_to_sc(b_or_m: Union[Bass, Melody], sc_client: udp_client.SimpleUDPClient, address: str):
    """
    Sends notes from a Bass or Melody object over to SuperCollider.
    :param b_or_m: Bass or Melody object
    :param sc_client: SimpleUDPClient
    :param address: str
    :return: None
    """
    for note in b_or_m.notes_and_durations[0]:
        msg = osc_message_builder.OscMessageBuilder(address=address)
        msg.add_arg(note.midi_note_number, 'i')
        msg = msg.build()
        sc_client.send(msg)


def send_bass_or_melody_durations_to_sc(b_or_m: Union[Bass, Melody], sc_client: udp_client.SimpleUDPClient,
                                        address: str):
    """
    Function to send durations from Bass or Melody object over to SuperCollider for sequencing.
    :param b_or_m: Bass or Melody Object
    :param sc_client: SimpleUDPClient
    :param address: str
    :return: None
    """
    msg = osc_message_builder.OscMessageBuilder(address=address)
    for duration in b_or_m.notes_and_durations[1]:
        msg.add_arg(duration)
    msg = msg.build()
    sc_client.send(msg)


def send_bass_or_melody_initialization_to_sc(channel: int, sc_client: udp_client.SimpleUDPClient, address: str):
    """
    Function to initialize bass or melody pattern in SuperCollider.
    :param channel: int
    :param sc_client: SimpleUDPClient
    :param address: str
    :return: None
    """
    msg = osc_message_builder.OscMessageBuilder(address=address)
    msg.add_arg(channel, arg_type='i')
    msg = msg.build()
    sc_client.send(msg)


def send_arpeggiator_on_off_to_sc(sc_client: udp_client.SimpleUDPClient, address: str = '/arpeggiator'):
    """
    Function to turn arpeggiator on or off.
    :param sc_client: SimpleUDPClient
    :param address: str
    :return: None
    """
    msg = osc_message_builder.OscMessageBuilder(address=address)
    msg = msg.build()
    sc_client.send(msg)


def send_rhythm_to_sc(rhythm_section: RhythmSection, sc_client: udp_client.SimpleUDPClient,
                      address: str = "/rhythm_section"):
    """
    Sends notes and durations from a RhythmSection object over to SuperCollider.
    :param rhythm_section: RhythmSection
    :param sc_client: SimpleUDPClient
    :param address: str
    :return: None
    """
    for i in range(len(rhythm_section.midi_notes)):
        msg = osc_message_builder.OscMessageBuilder(address=address)
        msg.add_arg(rhythm_section.midi_notes[i], 'i')
        for note_event in rhythm_section.midi_note_duration_arrays[i]:
            msg.add_arg(note_event)
        msg = msg.build()
        sc_client.send(msg)


def send_rhythm_initialization_to_sc(sc_client: udp_client.SimpleUDPClient, address: str = "/rhythm_init"):
    """
    Function to initialize RhythmSection pattern in SuperCollider.
    :param sc_client: SimpleUDPClient
    :param address: str
    :return: None
    """
    msg = osc_message_builder.OscMessageBuilder(address=address)
    msg = msg.build()
    sc_client.send(msg)


# TODO: Bug fix on quantization. Why is it not updating?
def send_quantization_update_to_sc(value: int, sc_client: udp_client.SimpleUDPClient,
                                   address: str = '/quantization'):
    """
    Updates the quantization value for patterns in SuperCollider.
    :param value: int
    :param sc_client: SimpleUDPClient
    :param address: str
    :return: None
    """
    msg = osc_message_builder.OscMessageBuilder(address=address)
    msg.add_arg(value)
    msg = msg.build()
    sc_client.send(msg)
