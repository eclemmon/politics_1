# Politics I

![Politics 1](/blob/logo_square.jpg)

### Politics I is a participatory work of music created by Eric Lemmon. For performances of this work, please get in touch at ec.lemmon@gmail.com
***
# Table of Contents

1. [Installation](#installation)
2. Registering for requisite services and getting access to web APIs
3. Setting up Politics I Environment
4. Running

***
# Installation

Politics I requires many different dependencies. This README file will walk you through downloading and installing the
software required for Politics I and its installation.

NB: Politics I has only been tested and run on MacOS. All installation instructions are based on the assumption that you are running MacOS Monterey.

## Installing Dependencies from Source

### Step 1:

Download and install [Python 3.9.2](https://www.python.org/downloads/release/python-392/)

### Step 2:

Download and install [SuperCollider](https://supercollider.github.io/downloads)

### Step 3:

Download and install [Ableton Live 11](https://www.ableton.com/en/)

### Step 4:

Download and install [Twilio CLI interface](https://www.twilio.com/docs/twilio-cli/getting-started/install#pkg-file)

### Step 5:

Download and install [ngrok CLI interface](https://ngrok.com/download)

### Step 6:

Download and install [Postgresql](https://www.postgresql.org/download/macosx/)

### Step 7:

Download and install [Redis from source](https://redis.io/docs/getting-started/installation/install-redis-from-source/)

### Step 8:

Download and extract [Politics I](https://github.com/eclemmon/politics_1/archive/refs/heads/trunk.zip) from github into a directory of your choosing

## Installing Dependencies with Brew

### Step 1:

Download and install [Python 3.9.2](https://www.python.org/downloads/release/python-392/)

### Step 2:

Download and install [Ableton Live 11](https://www.ableton.com/en/)

### Step 3:

Install brew from terminal

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

### Step 4:

Install all other requisite packages

`brew install \
--cask supercollider \
ngrok/ngrok/ngrok \
git \
postgresql \
redis &&
brew tap twilio/brew && brew install twilio`

### Step 5:

Clone Politics I from GitHub

`git clone https://github.com/eclemmon/politics_1.git`

