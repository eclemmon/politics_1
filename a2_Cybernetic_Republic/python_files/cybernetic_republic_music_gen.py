import logging
import random
import time
import threading
import random

import Classes.countdown
import Classes.vote_processor

from Classes.worker_thread import WorkerThread
from Classes.chord_progression import ChordProgression
from build_musical_data import *
from send_to_sc_functions import *
from pythonosc import udp_client
from pythonosc import osc_message_builder
from Utility_Tools.politics_logger import logger_launcher
from Data_Dumps.vote_options import vote_options
from Data_Dumps.scale_data import cybernetic_republic_scales
from Data_Dumps.progession_data import cybernetic_republic_intro_progression


class CyberneticRepublicMusicGen:
    def __init__(self, logger_object: logging.Logger, vote_processor_dat,
                 num_cycles=2, voting_period=30, resting_period=15):
        self.logger = logger_object
        self.countdown = Classes.countdown.Countdown(voting_period, resting_period)
        self.section = 0
        self.vote_option_keys = list(vote_processor_dat.keys())
        self.vote_processor_dat = vote_processor_dat
        self.vote_processor = self.build_vote_processor_options(0, self.vote_processor_dat)
        self.voters = {}

        self.sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
        self.gui_client = udp_client.SimpleUDPClient("127.0.0.1", 12000)

        self.worker_thread = None
        self.lock = threading.Lock()
        self.is_voting_period = False
        self.layer = 0
        self.total_time = (voting_period + resting_period) * num_cycles

        self.msg_address = "/message"
        self.count_address = "/count"
        self.flash_address = "/flash"
        self.end_address = "/end"

        self.meter_key = None
        self.progression_key = None
        self.bass_key = None
        self.rhythm_key = None
        self.middle_voices_key = None
        self.melody_key = None
        self.arpeggiator = False

    def on_data(self, data):
        """
        Checks if a user has already submitted a vote. If not, via the vote processor, checks to see if an option has
        been voted for. If something has been voted for, it modifies the vote percentage tally and sends the returned
        vote string off to the GUI.
        :param data: Dictionary of data e.g. {'username': "voter", 'text': "I want a)"}
        :return: None
        """
        if self.is_voting_period:
            # skip voter if they have already voted
            if self.voters.get(data['username']):
                pass
            else:
                # Add voter to voters
                self.voters[data['username']] = True
                # Update vote processor and get updated GUI string
                vote = self.vote_processor.on_message(data['text'])
                self.send_vote_message_to_gui(vote)
        else:
            pass

    def run(self):
        """
        Runs the main program which spins off a subtask via self.worker_thread to count through the sections and update
        any values in a thread-safe manner.
        :return: None
        """
        # Set initial GUI string
        vote = self.vote_processor.display_current_results()
        self.send_vote_message_to_gui(vote)
        # Start worker thread that counts through the sections
        if self.worker_thread is None:
            self.worker_thread = WorkerThread(target=self.run_counter, args=[self.total_time])
            self.worker_thread.start()

    def end(self):
        """
        Sends graceful shutdown messages and then runs shutdown on the python side.
        :return: None
        """
        msg = osc_message_builder.OscMessageBuilder(address=self.end_address)
        msg.add_arg(1, arg_type='i')
        msg = msg.build()
        self.sc_client.send(msg)
        self.gui_client.send(msg)
        self.shutdown()

    def shutdown(self):
        """
        Prints shutting down and ends the program.
        :return: None
        """
        print("shutting down")

    # TODO: Send section title over to GUI
    def run_counter(self, total_time):
        """
        This function runs the main logic of the cybernetic republic music generator. The counter handles the timing
        of section changeovers in a thread-safe manner.
        :param total_time: Integer of total time to run the movement.
        :return: None
        """
        total_count = 0
        while total_count <= total_time:
            # print(total_count)
            # reset vote processor after
            # Set is voting period to match countdown
            self.is_voting_period = self.countdown.is_voting_period
            # Get message of count down as string
            count_msg = self.countdown.count()
            # print(count_msg)
            # Create osc message object
            msg = osc_message_builder.OscMessageBuilder(address=self.count_address)
            # Add count string to osc message
            msg.add_arg(count_msg, arg_type='s')
            # Build osc message
            msg = msg.build()
            self.gui_client.send(msg)
            # Increment aggregate count of time passed and sleep one second
            total_count += 1
            time.sleep(1)
            # On section change, generate new vote processor options/reset, flash
            if total_count % (self.countdown.init_rest_period + self.countdown.init_vote_period) == 0:
                self.lock.acquire()
                try:
                    flash_msg = osc_message_builder.OscMessageBuilder(address=self.flash_address)
                    flash_msg = flash_msg.build()
                    self.gui_client.send(flash_msg)
                    self.section += 1
                    self.vote_processor = self.build_vote_processor_options(self.section, self.vote_processor_dat)
                    vote = self.vote_processor.display_current_results()
                    self.send_vote_message_to_gui(vote)
                finally:
                    self.lock.release()
        self.end()

    def build_vote_processor_options(self, section, dat):
        """
        Gets a random selection of values (that then become keys for the sound synthesis side of the program) to present
        as votes.
        :param section: String of the passed section.
        :param dat: Dictionary constructed as {String: List}
        :return: VoteProcessor with the section values as the selectable options
        """
        section_vals = dat[self.vote_option_keys[section]]
        section_vals = random.sample(section_vals, 4)
        return Classes.vote_processor.VoteProcessor(*section_vals)

    def send_vote_message_to_gui(self, text):
        """
        Helper function that updates the vote string on the GUI side.
        :param text: String from VoteProcessor object returned by a vote.
        :return: None
        """
        msg = osc_message_builder.OscMessageBuilder(address=self.msg_address)
        msg.add_arg(text, arg_type='s')
        msg = msg.build()
        self.gui_client.send(msg)

    @staticmethod
    def build_music_generators(meter_key=None, melody_key=None, bass_key=None,
                               middle_voices_key=None, rhythm_key=None, progression_key=None):
        if meter_key is None:
            meter_key = 'four'
        else:
            meter_key = meter_key

        if progression_key is None:
            progression_key = 'introduction'
        else:
            progression_key = progression_key

        hr = build_harmonic_rhythm(meter_key, progression_key)

        if bass_key is None:
            bass_key = 'introduction'
        else:
            bass_key = bass_key

        bass = build_bass(bass_key, hr, cybernetic_republic_scales['major'])

        if melody_key is None:
            melody = None
        else:
            melody = build_melody(melody_key, hr, cybernetic_republic_scales['major'])

        if middle_voices_key is None:
            middle_voices = None
        else:
            middle_voices = build_middle_voices(middle_voices_key, hr)

        if rhythm_key is None:
            rhythm_key = 'introduction'
        else:
            rhythm_key = rhythm_key

        rhythm = build_rhythm_section(rhythm_key, meter_key)

        return {'bass': bass, 'melody': melody, 'middle_voices': middle_voices, 'rhythm': rhythm}

    def send_musical_data_to_sc(self, data):
        # send rhythm data
        send_rhythm_to_sc(data['rhythm'], self.sc_client)
        # send middle voices data
        if data['middle_voices'] is not None:
            send_middle_voice_chords_to_sc(data['middle_voices'], self.sc_client)
            send_middle_voice_durations_to_sc(data['middle_voices'], self.sc_client)
        # send melody data
        if data['melody'] is not None:
            send_bass_or_melody_notes_to_sc(data['melody'], self.sc_client, '/melody_notes')
            send_bass_or_melody_durations_to_sc(data['melody'], self.sc_client, '/melody_durations')
        # send bass data
        send_bass_or_melody_notes_to_sc(data['bass'], self.sc_client, '/bass_notes')
        send_bass_or_melody_durations_to_sc(data['bass'], self.sc_client, '/bass_durations')

    def initialize_musical_data(self, arppeggiator=False):
        # Initialize everythin
        send_rhythm_initialization_to_sc(self.sc_client)
        send_bass_or_melody_initialization_to_sc(0, self.sc_client, '/bass_init')
        send_bass_or_melody_initialization_to_sc(0, self.sc_client, '/melody_init')
        send_middle_voice_initialization_to_sc(0, self.sc_client)
        # turn on or off arpeggiator
        if arppeggiator:
            send_arpeggiator_on_off_to_sc(self.sc_client, address='/arpeggiator')

    def run_music(self):
        data = self.build_music_generators(self.meter_key, self.melody_key, self.bass_key, self.middle_voices_key,
                                           self.rhythm_key, self.progression_key)
        self.send_musical_data_to_sc(data)
        self.initialize_musical_data(self.arpeggiator)


if __name__ == "__main__":
    a = {'username': 'boop', 'text': '808'}
    b = {'username': 'lop', 'text': 'I want funk!'}
    logger = logger_launcher()
    music_gen = CyberneticRepublicMusicGen(logger, vote_options)
    music_gen.run()
    for i in range(9):
        music_gen.on_data(a)
        time.sleep(random.random() * 5)
    for i in range(5):
        music_gen.on_data(b)
        time.sleep(random.random() * 5)
