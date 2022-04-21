# Politics I

![Politics 1](/blob/logo_square.jpg)

This repository hosts the development codebase for the participatory computer music work Politics I.

The current functionality uploaded here is currently in the development phase.

# Installation

Politics I requires many different dependencies. This README file will walk you through downloading and installing the
software required for Politics I. In this 

First and foremost, much of the software is written in Python. Download and install python by going here:

https://www.python.org/downloads/release/python-392/ or 

`brew tap twilio/brew && brew install twilio`




2. Download and install <a href=https://supercollider.github.io/download>SuperCollider</a>


3. Next, in your terminal (the following steps all occur in terminal), make sure pip is up to date:

`python3 -m pip install --user --upgrade pip`
   
4. Install venv:

`python3 -m pip install --user virtualenv`
   
5. Navigate to the directory you want to clone the repository (e.g. `/Users/your_user_name_here/Desktop/` on OSX):

`git clone https://github.com/eclemmon/politics_1`

6. Navigate into the new politics_1 directory.

`cd politics_1`

7. Create a virtual environment.

`python3 -m venv env`

8. Activate virtual environment.

`source env/bin/activate`

9. Install required packages.

`python3 -m pip install -r requirements.txt`

You now have all the required software to run Politics I! 

#Running Politics I

Coming soon! Currently, you need to launch both SuperCollider, evaluate a particular movement's .scd code and then run the files titled ***movement_name***_main.py.
In the future this will be automated.