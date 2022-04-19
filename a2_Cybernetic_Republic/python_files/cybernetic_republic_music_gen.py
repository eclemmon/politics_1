import json
import logging
import random
import threading
import time

import tweepy
from dotenv import dotenv_values

import Classes.countdown
import Classes.vote_processor
from Classes.worker_thread import WorkerThread
from Data_Dumps.scale_data import cybernetic_republic_scales
from Data_Dumps.vote_options import vote_options
from Utility_Tools.message_response import PoliticsMessageResponder
from Utility_Tools.message_response import generate_cybernetic_republic_message_response
from Utility_Tools.politics_logger import logger_launcher
from a2_Cybernetic_Republic.python_files.build_music_generator_objects import *
from a2_Cybernetic_Republic.python_files.send_to_sc_functions import *


class CyberneticRepublicMusicGen:
    def __init__(self, logger_object: logging.Logger, vote_processor_dat: dict,
                 num_cycles: int = 2, voting_period: int = 20, resting_period: int = 10) -> object:
        """
        Initializes Cybernetic Republic's music generator.
        :param logger_object: Logger to log as needed.
        :param vote_processor_dat: Dictionary of {String (Section): List (Keys to Music Generators)}
        :param num_cycles: Integer of number of sections to run through. (not an entire cycle through the sections).
        Currently, there are six sections, so num_cycles would need to be set to 6 to go through each different
        musical layer once.
        :param voting_period: Integer in seconds. The amount of time votes can be cast.
        :param resting_period: Integer in seconds. The amount of time that voting is closed and audience members
        can see the next vote options and listen.
        """
        # Data initialization
        self.logger = logger_object
        self.countdown = Classes.countdown.Countdown(voting_period, resting_period)
        self.section = 0
        self.introduction = True
        self.vote_option_keys = list(vote_processor_dat.keys())
        self.vote_processor_dat = vote_processor_dat
        self.vote_processor = self.build_vote_processor_options(0, self.vote_processor_dat)
        self.voters = {}

        # For thread safe handling of data
        self.worker_thread = None
        self.lock = threading.Lock()
        self.is_voting_period = False
        self.total_time = (voting_period + resting_period) * num_cycles

        # OSC UDP Clients
        self.sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
        self.gui_client = udp_client.SimpleUDPClient("127.0.0.1", 12000)

        # OSC Addresses
        self.vote_tally_address = "/vote_tally"
        self.update_vote_tally_address = "/update_vote_tally"
        self.count_address = "/count"
        self.selected_vote_address = "/selected_vote"
        self.end_section = "/end_section"
        self.end_address = "/end"

        # Musical Data
        self.arpeggiator = False

        self.variable_keys = {
            'bass': None,
            'progression': None,
            'middle-voices': None,
            'melody': None,
            'rhythm': None,
            'meter': None
        }

        # Message Responder
        config = dotenv_values()

        twitter_path = '/Users/ericlemmon/Documents/PhD/PhD_Project_v2/twitter_credentials.json'
        with open(twitter_path, "r") as file:
            credentials = json.load(file)

        self.twitter_auth = tweepy.OAuth1UserHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'],
                                                     credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
        self.responder = PoliticsMessageResponder(config['TWILIO_ACCOUNT_SID'], config['TWILIO_AUTH_TOKEN'],
                                                  config['TWILIO_PHONE_NUMBER'], self.twitter_auth)

        # run the countdown
        self.run_music()

    def on_data(self, data: dict):
        """
        Checks if a user has already submitted a vote. If not, via the vote processor, checks to see if an option has
        been voted for. If something has been voted for, it modifies the vote percentage tally and sends the returned
        vote string off to the GUI.
        :param data: Dictionary of data e.g. {'username': "voter", 'text': "I want a)"}
        :return: None
        """
        kwargs = {
            'vote': None,
            'already-voted': False,
            'no-option-selected': False,
            'voting-period': self.is_voting_period,
            'introduction': self.introduction,
            'first-option': self.vote_processor.candidates[0],
            'vote-text': data['text']
        }
        print(data)
        if self.is_voting_period:
            # If voting is open
            if self.voters.get(data['username']):
                # skip voter if they have already voted
                # Respond
                kwargs['already-voted'] = True
            else:
                # Update vote processor and get updated GUI string
                vote = self.vote_processor.on_message(data['text'])
                print(vote)
                if vote is None:
                    # If the voter submitted a message without a vote option.
                    # if the vote processor returns None, set voter to not having voted
                    self.voters[data['username']] = False
                    kwargs['no-option-selected'] = True
                else:
                    # If the voter submitted a message with a vote option
                    # the voter successfully voted
                    # Add voter to voters
                    self.voters[data['username']] = True
                    self.send_vote_message_to_gui(vote.splitlines(), update=True)
                    # Respond with sucessful vote
                    kwargs['vote'] = vote

        else:
            # If voting is not open
            # Respond and do nothing
            kwargs['voting-period'] = self.is_voting_period

        # Generate a response based on conditional logic
        generate_cybernetic_republic_message_response(self.responder, data=data, kwargs=kwargs)

    def run(self):
        """
        Runs the main program which spins off a subtask via self.worker_thread to count through the sections and update
        any values in a thread-safe manner.
        :return: None
        """
        # Start the GUI
        self.send_logic_to_gui("/start")
        # send initial section title to GUI
        self.send_section_title_to_gui(list(self.vote_processor_dat.keys())[self.section].upper())
        # Set initial GUI Vote options
        vote = self.vote_processor.display_current_results()
        self.send_vote_message_to_gui(vote.splitlines())
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

    def run_counter(self, total_time: int):
        """
        This function runs the main logic of the cybernetic republic music generator. The counter handles the timing
        of section changeovers in a thread-safe manner.
        :param total_time: Integer of total time to run the movement.
        :return: None
        """
        total_count = 0
        while total_count <= total_time:
            if self.introduction and total_count == self.countdown.init_rest_period:
                self.start_introduction()
            # Set is voting period to match countdown
            self.is_voting_period = self.countdown.is_voting_period
            # Get message of count down as string
            count_msg = self.countdown.count()
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
                    # Send the music data to SC
                    section = self.vote_option_keys[self.section]
                    winning_key = self.vote_processor.get_winning_key()
                    self.variable_keys[section] = winning_key
                    # Turn on or off arpeggiator
                    if self.variable_keys['middle-voices'] == 'arpeggiated':
                        self.turn_arpeggiator_on_off(True)
                    else:
                        self.turn_arpeggiator_on_off(False)
                    # Send all data to SC
                    self.run_music()
                    # Send the winning key to the GUI
                    self.send_selected_vote_to_gui(self.vote_processor.get_winning_key_index())
                    # Update section
                    self.send_logic_to_gui(self.end_section)
                    self.section = (self.section + 1) % len(self.vote_option_keys)
                    self.vote_processor = self.build_vote_processor_options(self.section, self.vote_processor_dat)
                    vote = self.vote_processor.display_current_results()
                    if self.introduction:
                        self.introduction = False
                        self.end_introduction()
                    # Send New Section Title
                    self.send_section_title_to_gui(list(self.vote_processor_dat.keys())[self.section].upper())
                    # Send new vote options
                    self.send_vote_message_to_gui(vote.splitlines())
                    # reset voters
                    self.voters = {}
                finally:
                    self.lock.release()
        self.end()

    def build_vote_processor_options(self, section: str, dat: dict):
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

    def send_vote_message_to_gui(self, text_list: list, update: bool = False):
        """
        Helper function that updates the vote string on the GUI side.
        :param update: bool
        :param text_list: List of Strings from VoteProcessor object returned by a vote.
        :return: None
        """
        if update:
            msg = osc_message_builder.OscMessageBuilder(address=self.update_vote_tally_address)
        else:
            msg = osc_message_builder.OscMessageBuilder(address=self.vote_tally_address)
        for text in text_list:
            msg.add_arg(text, arg_type='s')
        msg = msg.build()
        self.gui_client.send(msg)

    def send_selected_vote_to_gui(self, selected_vote_index: int):
        """
        Sends the selected vote to the GUI.
        :param selected_vote_index: Integer of selected vote.
        :return: None
        """
        msg = osc_message_builder.OscMessageBuilder(address=self.selected_vote_address)
        msg.add_arg(selected_vote_index, arg_type='i')
        msg = msg.build()
        self.gui_client.send(msg)

    def send_logic_to_gui(self, address: str):
        """
        Sends logic to the GUI that requires no data (kind of like a bang, trigger, or gate) that simply flips a
        'switch' on receipt.
        :param address: String as OSC address.
        :return: None
        """
        msg = osc_message_builder.OscMessageBuilder(address=address)
        msg = msg.build()
        self.gui_client.send(msg)

    def send_section_title_to_gui(self, section_title, address='/section_title'):
        msg = osc_message_builder.OscMessageBuilder(address=address)
        msg.add_arg(section_title, arg_type='s')
        msg = msg.build()
        self.gui_client.send(msg)

    def start_introduction(self):
        self.send_logic_to_gui('/start_introduction')

    def end_introduction(self):
        self.send_logic_to_gui('/end_introduction')
        self.introduction = False

    @staticmethod
    def build_music_generators(meter_key=None, melody_key=None, bass_key=None,
                               middle_voices_key=None, rhythm_key=None, progression_key=None):
        """
        Builds various music generator objects by key. Some additional logic is added so that music starts from the
        beginning with some default options running.
        :param meter_key: String || None
        :param melody_key: String || None
        :param bass_key: String || None
        :param middle_voices_key: String || None
        :param rhythm_key: String || None
        :param progression_key: String || None
        :return: Dictionary of {String: Musical Generator Object}
        """
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

    def send_musical_data_to_sc(self, data: dict):
        """
        Sends musical data to SuperCollider via OSC.
        :param data: Dictionary of {String: Musical Generator Object}
        :return:
        """
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

    def initialize_musical_data(self, data: dict, max_inst: int = 8, arppeggiator: bool = False):
        """
        Sends initialization command to SuperCollider via OSC.
        :param data: Dictionary of {String: Musical Generator Object}
        :param arppeggiator: Boolean of whether the arpeggiator is to be turned on or off
        :return: None
        """
        # Initialize everything
        send_rhythm_initialization_to_sc(self.sc_client)
        send_bass_or_melody_initialization_to_sc(random.randint(0, max_inst), self.sc_client, '/bass_init')
        if data['melody'] is not None:
            send_bass_or_melody_initialization_to_sc(random.randint(0, max_inst), self.sc_client, '/melody_init')
        if data['middle_voices'] is not None:
            send_middle_voice_initialization_to_sc(random.randint(0, max_inst), self.sc_client)
        # turn on or off arpeggiator
        if arppeggiator:
            send_arpeggiator_on_off_to_sc(self.sc_client, address='/arpeggiator')
        # Set Quantization after initialization
        send_quantization_update_to_sc(data['rhythm'].meter.num_beats, self.sc_client, address='/quantization')

    def run_music(self):
        """
        Runs the music generators based on the keys called.
        :return: None.
        """
        data = self.build_music_generators(self.variable_keys['meter'], self.variable_keys['melody'],
                                           self.variable_keys['bass'], self.variable_keys['middle-voices'],
                                           self.variable_keys['rhythm'], self.variable_keys['progression'])
        self.send_musical_data_to_sc(data)
        self.initialize_musical_data(data, self.arpeggiator)

    def turn_arpeggiator_on_off(self, arpeggiator_on_off: bool):
        """
        Helper function that sets class variable self.arpeggiator.
        :param arpeggiator_on_off: Boolean. True = On, False = Off
        :return: None
        """
        self.arpeggiator = arpeggiator_on_off

if __name__ == "__main__":
    a = {'username': 'boop', 'text': '808'}
    b = {'username': 'lop', 'text': 'random'}
    logger = logger_launcher()
    music_gen = CyberneticRepublicMusicGen(logger, vote_options, num_cycles=20)
    music_gen.run()
    for i in range(9):
        music_gen.on_data(b)
        time.sleep(random.random() * 5)
    for i in range(5):
        music_gen.on_data(b)
        time.sleep(random.random() * 5)
    for i in range(40):
        music_gen.on_data(b)
        time.sleep(random.random() * 5)
