"""
store_user_message.py
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2022, Eric Lemmon"
__credits__ = ["Eric Lemmon"]
__version__ = ""
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Production"

import datetime
from Models.message import Message
from Models.user import User


def store_message(message_data, app, config, db):
    """
    Function to store data to the PostgresDB. Returns True of False depending on whether the operation was successful.
    :param db:
    :param config:
    :param app:
    :param message_data: dict
    :return: bool
    """
    with app.app_context():
        try:
            user = get_or_make_user(message_data, app, db)
            msg = Message(text=message_data['text'],
                          date=datetime.datetime.now().isoformat(),
                          user_id=user.id,
                          movement=config["MOVEMENT"],
                          scored=scored(config))
            db.session.add(msg)
            db.session.commit()
            res = True
        except Exception as e:
            print("There was an exception!")
            print(e)
            db.session.rollback()
            res = False
        finally:
            db.session.close()
            return res


def get_or_make_user(message_data, app, db):
    """
    Function to create a user on the database
    :param db:
    :param app:
    :param message_data: dict
    :return: User on success || None on failure
    """
    with app.app_context():
        if db.session.query(User.id).filter_by(username=message_data['username']).first() is not None:
            return db.session.query(User).filter(User.username == message_data['username']).first()
        else:
            user = User(username=message_data['username'])
            try:
                db.session.add(user)
                db.session.commit()
                return user
            except:
                print("There was an exception in the making of the user!")
                db.session.rollback()
            finally:
                db.session.close()


def scored(config):
    """
    A helper function to get settings from the config file, since settings come in as strings
    :param config: dict
    :return: bool
    """
    if config["SCORED"] == "true":
        return True
    else:
        return False
