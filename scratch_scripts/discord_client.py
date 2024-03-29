"""
discord_client.py
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2022, Eric Lemmon"
__credits__ = ["Eric Lemmon"]
__version__ = ""
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Production"

import discord
from flask_socketio import SocketIO
from Utility_Tools.store_user_message import store_message


class DiscordClient(discord.Client):
    def __init__(self, app, config, db, intents):
        super().__init__(intents=intents)
        self.client_sio = SocketIO(message_queue='redis://')
        self.send_data = False
        self.app = app
        self.config = config
        self.db = db

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        else:
            print(message)
            message_data = {'discord': True}
            store_message(message_data, self.app, self.config, self.db)
            self.client_sio.emit('handle_message', message_data)

    def send_data_off(self):
        self.send_data = False
        print(self.send_data_report())

    def send_data_on(self):
        self.send_data = True
        print(self.send_data_report())

    def send_data_report(self):
        return 'Sending data set to: {}'.format(self.send_data)

