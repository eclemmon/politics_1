"""
discord_connector.py
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2022, Eric Lemmon"
__credits__ = ["Eric Lemmon"]
__version__ = ""
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Production"

import asyncio
import os
import discord
import threading
from dotenv import load_dotenv
from Utility_Tools.message_response import generate_discord_discourse_message
from Classes.node import Node

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
WEBHOOK = os.getenv('DISCORD_WEBHOOK')
intents = discord.Intents.all()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Discord connection is ready.")


@client.event
async def on_message(message):
    if message.author.bot == False:
        await message.reply("You said: " + message.content)
    else:
        pass

async def start():
    await client.start(TOKEN)

def run_it_forever(loop):
    loop.run_forever()

def init():
    asyncio.get_child_watcher()
    loop = asyncio.get_event_loop()
    loop.create_task(start())

    thread = threading.Thread(target=run_it_forever, args=(loop,))
    thread.start()

init()




username = "Eric"
url = "https://discord.com/channels/995399237061857381/995399237623885906/995404775292141609"
# embed = discord.Embed(title="Hi {}!".format(username),
#                       url=url,
#                       color=discord.Color.green())
# embed.add_field(name="YOU SAID: ", value="boops\n", inline=False)
# embed.add_field(name="THE RESULT: ", value="DATA\nDATA\nDATA", inline=False)
parent = Node('uh')
data = {'username': username, 'url': url, 'text': 'ho hum doldrum'}
kwargs = {'od': 7.43, 'time_interval': 4, 'rhythm': [0, 1, 0, 1], 'delay_t_a_d': (3, 3), 'spat': (-0.99, 0.0, 1.0), 'pmod': '8.4', 'inst_node': Node("abc", parent=parent)}


# embed = generate_discord_discourse_message(data, kwargs)
# webhook = discord.Webhook.from_url(WEBHOOK, adapter=discord.RequestsWebhookAdapter())
# webhook.send(username="Politics I Bot", embed=embed)

