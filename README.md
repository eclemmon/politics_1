# Politics I

![Politics 1](/blob/readme/logo_square.jpg)

### Politics I is a participatory work of music created by Eric Lemmon. For performances of this work, please get in touch at ec.lemmon@gmail.com. 
For more about this work, please visit [my website](https://ericlemmon.net/politics-i/).

***

# Table of Contents

1. [Technical Requirements](#technical-requirements)
2. [Installation](#installation)
3. [Registering for requisite services and getting access to web APIs](#Registering-for-Services-and-Getting-Access-to-APIs)
4. [Setting up Politics I Environment](#setting-up-politics-i-environment)
5. [Running](#Running-Politics-I)
6. [Bibliography](#bibliography)

***

# Technical Requirements

- Minimum: Stereo PA System & Sub
- Projector Screen
- Projector
- Stable Internet Connection

***

# Installation

Politics I requires many different dependencies. This README file will walk you through downloading and installing the
software required for Politics I and its installation.

NB: Politics I has only been tested and run on MacOS. All installation instructions are based on the assumption that you are running MacOS Monterey.

***

## Installing Dependencies from Source

### Step 1:

> Download and install [Python 3.9.2](https://www.python.org/downloads/release/python-392/)

### Step 2:

> Download and install [SuperCollider](https://supercollider.github.io/downloads)

### Step 3:

> Download and install [Ableton Live 11](https://www.ableton.com/en/)

### Step 4:

> Download and install [Twilio CLI interface](https://www.twilio.com/docs/twilio-cli/getting-started/install#pkg-file)

### Step 5:

> Download and install [ngrok CLI interface](https://ngrok.com/download)

### Step 6:

> Download and install [Postgresql](https://www.postgresql.org/download/macosx/)

### Step 7:

> Download and install [Redis from source](https://redis.io/docs/getting-started/installation/install-redis-from-source/)

### Step 8:

> Download and install [Processing](https://processing.org/download)

### Step 9:

> Download and extract [Politics I](https://github.com/eclemmon/politics_1/archive/refs/heads/trunk.zip) from github into a directory of your choosing

***

## Installing Dependencies with Brew

### Step 1:

> Download and install [Python 3.9.2](https://www.python.org/downloads/release/python-392/)

### Step 2:

> Download and install [Ableton Live 11](https://www.ableton.com/en/)

### Step 3:

> Download and install [Processing](https://processing.org/download)

### Step 4:

Install brew from terminal

`$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

### Step 5:

Install all other requisite packages

`$ brew install \
--cask supercollider \
ngrok/ngrok/ngrok \
git \
postgresql \
redis &&
brew tap twilio/brew && brew install twilio`

### Step 6:

Clone Politics I from GitHub

`$ git clone https://github.com/eclemmon/politics_1.git`

***

# Registering for Services and Getting Access to APIs

## Sign up for Twilio

**Twilio is a low-cost, enterprise messaging service provider. This service is how Politics I sends and receives
sms messages from and too the audience.**

### Step 1:

> [Register for Twilio](https://www.twilio.com/try-twilio)

### Step 2:

> [Buy a phone number](https://support.twilio.com/hc/en-us/articles/223135247-How-to-Search-for-and-Buy-a-Twilio-Phone-Number-from-Console) on Twilio.

### Step 3:

> [Fill Twilio account](https://support.twilio.com/hc/en-us/articles/223135487-How-Twilio-billing-works) as needed.
Running a performance of Politics I takes <$20 to buy the number and fill the account for a concert, depending
on the number of people in the audience.

## Sign up for Twitter

### Step 1:

> [Register for Twitter](https://twitter.com/i/flow/signup)

### Step 2:

> [Create a Developer account](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)
and go through the process of applying for a standalone app.

NB: so that the tweepy message responder can reply to tweets automatically in Politics I, OAuth 1.0a must be turned on:

![OAuth](/blob/readme/twitter_oauth.png)

## Register for Discord

### Step 1:

> [Register for Discord and log in via web browser](https://discord.com/)

### Step 2:

> Create a new server

![discord_server](/blob/readme/discord_create_server.png)

### Step 3:

> [Navigate to Discord's application developer portal.](https://discord.com/developers/applications)

### Step 4:

> Create a new application

![Create a new application](/blob/readme/discord_bot_1.png)

![Create a new application](/blob/readme/discord_bot_2.png)

### Step 5:

> Add the bot

![Add the bot](/blob/readme/discord_bot_3.png)

### Step 6:

> Make the bot private and get the token

![Get the token](/blob/readme/discord_bot_4.png)

### Step 7:

> Go to the Oauth2 --> URL Generator tab and check the bot option in scopes

![check the bot scopes in OAuth2](/blob/readme/discord_bot_5.png)

### Step 8:

> Set the bot permissions and copy the generated URL

![set permission and copy url](/blob/readme/discord_bot_6.png)

### Step 9:

> Add the bot to your server

![Add bot to server](/blob/readme/discord_bot_7.png)

### Step 10:

> In your discord server, go to server settings by hitting the carrot at the top left near the server name.

![Go to server settings step 1](/blob/readme/discord_server_settings_1.png)

![Go to server settings step 2](/blob/readme/discord_server_settings_2.png)

### Step 11:

> Click on the integrations tab

![Go to integrations tab](/blob/readme/discord_server_settings_3.png)

### Step 12:

> Select the webhooks option and create a new webhook.

![Select webhooks option](/blob/readme/discord_webhook_settings_4.png)
![Create a new webhook](/blob/readme/discord_webhook_settings_5.png)

### Step 13:

> Set the webhook name, set the target channel where participants can chat, save changes, and copy the webhook URL into the .env file

![Set webhook, channel, save, and copy webhook to .env](/blob/readme/discord_webhook_settings_6.png)

PHEW! All done with setting up discord!
***

# Setting up Politics I Environment

## Set up Postgresql

>[Follow these instructions](https://kb.objectrocket.com/postgresql/how-to-create-a-database-in-postgresql-1350). When you are choosing what to name the database, you can name it whatever you want, but it is recommended that
the name is something recognizably associated with the piece, like `politics_1_prod`.

## Set up Python

### Step 1:

Navigate to your Politics I directory in terminal:

`$ cd /path/to/politics_1`

### Step 2:

Initialize a virtual environment with python:

`$ python3 -m venv /path/to/new/virtual/environment`

### Step 3:

Activate your python virtual environment:

`$ source myvenv/bin/activate`

### Step 4:

Install required python packages:

`$ (venv) python3 -m pip install -r requirements.txt`

### Step 5:

Install processing-java for CLI control of processing sketches.

* Open Processing IDE in `~/path/to/Processing`
* In the menubar select `tools` > `install processing-java`:
![Politics 1](/blob/readme/install-processing-java.png)


## Set Environment Variables

### Step 1:

Still in your politics I directory, create a .env file through Terminal, which will store global environment variables.
NB: You may need to execute `⌘` + `⇧ Shift` + `.` to see this file after its creation.

`$ touch .env`

### Step 2:

Open the .env file and fill out the empty fields following the `=` symbol.
For example, after TWILIO_ACCOUNT_SID=, you will place your unique String Identifier code, which will look something like this:
`SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` (see instructions below to find all authentication tokens for both Twilio, Discord, and Twitter).

```
# GET THESE TWILIO VALUES FROM TWILIO DASH
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# GET THESE TWITTER VALUES FROM TWITTER DEV DASH
TWITTER_CONSUMER_KEY=
TWITTER_CONSUMER_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=

# YOUR TWITTER HANDLE GOES HERE, AUDIENCE MEMBERS SHOULD BE INSTRUCTED TO TWEET AT YOUR ACCOUNT
SEARCH_TERM=

# YOUR DISCORD TOKEN, GUILD, AND WEBHOOKS GO HERE
DISCORD_TOKEN=
DISCORD_GUILD=
DISCORD_WEBHOOK=

# SOME LOGIC VALUES FOR RUNNING THE PROGRAM
MOVEMENT=1
SCORED=false
DAW=true
DEBUG=true,
SECRET_KEY=abc123

# SHOULD BE THE NAME OF THE POSTGRES DB YOU CREATED
SQLALCHEMY_DATABASE_URI=postgresql:///politics_1_prod

# DEFAULT DIRECTORY FOR SUPERCOLLIDER ALLOWING FOR AUTO-BOOT VIA SHELL SCRIPT
SC_DIR="/Applications/SuperCollider.app/Contents/MacOS"
```

> Twilio SID and Auth Token [instructions](https://support.twilio.com/hc/en-us/articles/223136027-Auth-Tokens-and-How-to-Change-Them).

> [Instructions](https://developer.twitter.com/en/docs/authentication/oauth-1-0a/api-key-and-secret) for finding and getting twitter authentication keys and secrets.

> Get Discord [bot token](https://docs.discordbotstudio.org/setting-up-dbs/finding-your-bot-token).

> Get Discord [webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

Once all these variables are set, you should be almost ready to go!

***

# Running Politics I

First, boot the messaging servicer(s):

`$ sh run.sh`

Then, open Live and SuperCollider (whether you open live will depend on the movement you are performing) and execute 
any necessary supercollider code in the movement_name_main.scd file. Then navigate back to the directory of the movement 
you are performing and execute:

`$ sh run_movement_name.sh`

NB: In the future, you will not need to run SuperCollider code manually, as sclang and scsynth
will be run from the shell scripts automatically.

***

If you have any questions, or any steps seem to be missing in this installation walk-through,
let me know! Contact me at `ec.lemmon@gmail.com`

***

#### [Bibliography](/blob/politics_I.bib)

