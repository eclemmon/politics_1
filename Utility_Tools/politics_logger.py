import datetime
import logging
import os
import time
from pathlib import Path

path = Path(__file__).parent.parent
FILE_PATH = os.path.join(path, 'Log_Files/')
# FILE_PATH = "/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/Log_Files/"


def construct_filename(path):
    """
    Constructs a file name  so that the .log file constructor can create
    a logging file dileneated by date and time.
    :param path: str The target file path to save logged files.
    :return: str Returns the new path, along with constructed file name.
    """
    tail = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    new_path = path + 'Politics-Log-' + tail + '.log'
    print(new_path)
    return new_path


def create_logger_file(path):
    """
    Builds a .log file that can be written to.
    :param path: str The target file path to create logged files.
    """
    file_name = construct_filename(path)
    current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    if os.path.exists(file_name):
        print("This date-time already exists, did you change timezones recently?")
        time.sleep(1)
        create_logger_file(path)
    else:
        try:
            new_file = open(file_name, 'w')
            logger_header = '#' * 10 + ' STARTING NEW SESSION: ' + current_time + ' ' + '#' * 10 + '\n\n'
            new_file.write(logger_header)
        except:
            raise Exception("Something went wrong!")
        finally:
            print("File created, cleaning up.")
            new_file.close()
            return file_name


def setuplogger(path):
    """
    This function sets up the logger after building the file required through
    function: create_logger_file(path)
    :param path: str This is the path where you want to store your log of data
    :return: FileHandler Returns a file handler that will continuously write to the file
    specified in path for the duration of the session running.
    """
    print("Creating new logger file...")
    filename = create_logger_file(path)

    print("Initializing logger...")
    file_handler = logging.FileHandler(filename, mode='a')
    return file_handler


def logger_launcher():
    """
    This function launches the logger so any/all data is printed to the log file during the course of a concert.
    :return: Logger
    """
    print("Launching Logger")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    filehandler = setuplogger(FILE_PATH)
    formatter = logging.Formatter('OUTPUT %(asctime)s: %(message)s')
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    return logger


if __name__ == '__main__':
    setuplogger(FILE_PATH)
