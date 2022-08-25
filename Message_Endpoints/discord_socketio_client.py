"""
discord_socketio_client.py
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2022, Eric Lemmon"
__credits__ = ["Eric Lemmon"]
__version__ = ""
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Production"


import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
WEBHOOK = os.getenv('DISCORD_WEBHOOK')
intents = discord.Intents.all()

client = discord.Client(intents=intents)
post_address = 'http://127.0.0.1:8000/discord'


@client.event
async def on_ready():
    print("Discord connection is ready.")


@client.event
async def on_message(message: discord.Message):
    if not message.author.bot:
        payload = {
            'id': message.id,
            'channel_id': message.channel.id,
            'author_id': message.author.id,
            'username': message.author.name,
            'guild_id': message.guild.id,
            'guild_name': message.guild.name,
            'text': message.content
        }
        requests.post(post_address, data=payload)
    else:
        pass


client.run(TOKEN)


