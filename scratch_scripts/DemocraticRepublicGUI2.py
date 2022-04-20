import tkinter as tk
import tkinter.font as tkFont
from Classes import countdown
import vote_processor
import threading
import queue
from scratch_scripts.Python2SC import StreamListener
from scratch_scripts import Python2SC
import tweepy
import random
import json
from scratch_scripts.Python2SC import message_handler
from pythonosc import udp_client

with open("../Deprecated/twitter_credentials.json", "r") as file:
    credentials = json.load(file)

auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])

class CountDownApp(countdown.Countdown):
    def __init__(self, voting_period, rest_period, vote_processor, queue):

        # initiate vote processor and counter periods
        self.vote_processor = vote_processor
        self.init_seconds = voting_period
        self.seconds = self.init_seconds
        self.init_rest_period = rest_period
        self.rest_period = self.init_rest_period

        # initiate tkinter and GUI
        self.root = tk.Tk()
        self.fontStyle = tkFont.Font(family="Lucida Grande", size=40)
        self.counter = tk.Label(text="", font=self.fontStyle)
        self.counter.pack()
        self.votetotals = tk.Label(text="", font=self.fontStyle)
        self.votetotals.pack()
        self.my_msg = tk.StringVar()
        self.my_msg.set("Type entries here")

        # initiate entry field for testing voting system. To be deprecated in favor of tweets
        self.entry_field = tk.Entry(self.root, textvariable=self.my_msg)
        self.entry_field.bind("<Return>", self.send)
        self.entry_field.pack()
        self.send_button = tk.Button(self.root, text="Send", command=self.send)
        self.send_button.pack()


        # Begin counting
        self.voting_period()

    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                print(msg)
            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass


    def send(self, event=None):  # event is passed by binders.
        """Handles sending of messages."""
        msg = self.my_msg.get()
        self.my_msg.set("")
        self.root.after(0, self.vote_processor.on_message(msg))
        self.votetotals.configure(text=vote_processor.display_current_results())

    def on_tweet(self):
        pass


    def voting_period(self):
        if self.seconds > 0:
            self.voting_countdown_print()
            count = self.voting_countdown_print() + '\n'
            self.seconds -= 1
            self.counter.configure(text=count)
            self.root.after(1000, self.voting_period)
        else:
            self.seconds = self.init_seconds
            self.resting_period()

    def resting_period(self):
        if self.rest_period > 0:
            count = self.resting_countdown_print() + '\n'
            self.rest_period -= 1
            self.counter.configure(text=count)
            self.root.after(1000, self.resting_period)
        else:
            self.rest_period = self.init_rest_period
            self.vote_processor.reset_vote_tallies()
            self.voting_period()

    def tweet_stream_launcher(self, logger_object):
        """
        This is the main loop.
        :param logger_object: needs the logger object passed to it so it knows what to use.
        """



class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui = CountDownApp(master, self.queue)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(200, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        try:
            message_handler('Testing logger...', self.logger_object)
            message_handler("Launching Twitter Listener", self.logger_object)
            self.api = tweepy.API(auth)
            message_handler("Launching Passer", self.logger_object)
            self.client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
            message_handler("testing passer",self.logger_object)
            self.client.send_message("/filter", ["Testing OSC Message"])
            message_handler("Information passed, check SuperCollider to see if arrived", self.logger_object)
            message_handler('Trying to listen', self.logger_object)
            self.stream_listener = DemocraticRepublicStreamListener(self.client)
            self.stream = tweepy.Stream(auth=self.api.auth, listener=self.stream_listener)
            self.stream.filter(follow=["1191395193615990785"])
            message_handler('Boot complete\n\n', logger_object)
        except Exception:
            logger_object.exception("There Was a Problem in the Main Loop\n")



        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following two lines with the real
            # thing.

            msg = random.random()
            self.queue.put(msg)




class VoteProcessor(vote_processor.Voteprocessor):
    def display_current_results(self):
        totals = self.tally_votes()
        formatted_text = ''
        for key, value in totals.items():
            text = key + ':  ' + '{0:.2f}%\n'.format(round(value*100, 2))
            formatted_text += text
        return formatted_text

class DemocraticRepublicStreamListener(StreamListener):
    def on_data(self, raw_data):
        """
        Takes in data in json format from Twitter, and checks for the data fields desired to be
        taken in for processing. Currently only logs and posts the data to console and log file.
        Will call NLP processes on the data in the future and pass the data to SuperCollider.
        :param raw_data: Data as json from Twitter
        """
        try:
            raw_data_as_dict = json.loads(raw_data)
            messageheader = '\n\n##### START OF TWEET DATA #####\n\n'
            message_body_list = []
            for item in self.user_keys_to_query:
                message_body_list.append('{:<25}: {:}\n'.format(item.upper(), raw_data_as_dict['user'][item]))
            for item in self.entities_keys_to_query:
                message_body_list.append('{:<25}: {:}\n'.format(item.upper(), raw_data_as_dict['entities'][item]))
            for key in self.keys_to_query:
                message_body_list.append('{:<25}: {:}\n'.format(key.upper(), raw_data_as_dict[key]))
            message_body = ''.join(message_body_list)
            message_footer = '\n##### END OF TWEET DATA #####\n'
            full_message = messageheader + message_body + message_footer
            message_handler(full_message, logger_object)
            return raw_data_as_dict['text']
        except Exception:
            logger_object.exception("Something went wrong while trying to collect data!\n")

    def on_connect(self):
        """
        Posts a message to message handler.
        """
        msg = "Successfully connected to streaming server."
        message_handler(msg, logger_object)




if __name__ == '__main__':
    vote_processor = VoteProcessor('a)', 'b)', 'c)', 'd)', 'e)')
    logger_object = Python2SC.logger_launcher()
    app = CountDownApp(30, 15, vote_processor, logger_object)
    app.root.mainloop()



