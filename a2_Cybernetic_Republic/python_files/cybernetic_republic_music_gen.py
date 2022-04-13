import logging
import random
import time
import threading
import random

import Classes.countdown
import Classes.vote_processor

from Classes.worker_thread import WorkerThread
from pythonosc import udp_client
from pythonosc import osc_message_builder
from Utility_Tools.politics_logger import logger_launcher
from Data_Dumps.vote_options import vote_options




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
