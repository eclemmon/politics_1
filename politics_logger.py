import os, datetime, time, logging

FILE_PATH = "/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/Log_Files/"


def construct_filename(path):
    """
    Constructs a file name  so that the .log file constructor can create
    a logging file dileneated by date and time.
    :param str path: The target file path to save logged files.
    :return: Returns the new path, along with constructed file name.
    """
    tail = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    new_path = path + 'Politics-Log-' + tail + '.log'
    print(new_path)
    return new_path


def create_logger_file(path):
    """
    Builds a .log file that can be written to.
    :param str path: The target file path to create logged files.
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
    :param path: This is the path where you want to store your log of data
    :return: Returns a file handler that will continuously write to the file
    specified in path for the duration of the session running.
    """
    print("Creating new logger file...")
    filename = create_logger_file(path)

    print("Initializing logger...")
    file_handler = logging.FileHandler(filename, mode='a')
    return file_handler


# def mainlogger(path):
#     """
#     This function acts as the mainloop for the logger from the logger module.
#     The goal is for it
#     :param path: The target file path to create logged files.
#     """
#     filename = construct_filename(path)
#     current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
#     loggerfile = open(filename, 'w')
#     logger_header = '#'*10 + ' STARTING NEW SESSION: ' + current_time + ' ' + '#'*10 + '\n\n'
#     loggerfile.write(logger_header)
#     loggerfile.close()
#     FORMAT = 'OUTPUT %(asctime)s: %(message)s'
#     logging.basicConfig(filename=filename, format=FORMAT, filemode='a', level=logging.DEBUG)
#     #logging.info(" Starting session: %s" % current_time)
#     logging.info("Logger initialized")


if __name__ == '__main__':
    setuplogger(FILE_PATH)
