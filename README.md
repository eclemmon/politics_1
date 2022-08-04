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
`SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` (see instructions below to find all authentication tokens for both Twilio and Twitter).

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

# SOME LOGIC VALUES FOR RUNNING THE PROGRAM
MOVEMENT=1
SCORED=false
DAW=true
DEBUG=true,
SECRET_KEY=abc123

# SHOULD BE THE NAME OF THE POSTGRES DB YOU CREATED
SQLALCHEMY_DATABASE_URI=postgresql:///politics_1_prod
```

> Twilio SID and Auth Token [instructions](https://support.twilio.com/hc/en-us/articles/223136027-Auth-Tokens-and-How-to-Change-Them).

> [Instructions](https://support.twilio.com/hc/en-us/articles/223136027-Auth-Tokens-and-How-to-Change-Them) for finding and getting twitter authentication keys and secrets.

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

