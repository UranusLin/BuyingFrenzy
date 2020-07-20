import logging
import os
from datetime import datetime
import logging.handlers
from pytz import timezone

path = r"../log/"
log = r".log"

# set to timezone to Taipei
tz = timezone('Asia/Taipei')

def timetz(*args):
    return datetime.now(tz).timetuple()

def setup_logger(logger_name, log_file, level=logging.INFO):
    logging.Formatter.converter = timetz
    l = logging.getLogger(logger_name)
    log_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s ', '%Y-%m-%d %H:%M:%S %p %z %Z')
    fileHandler = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight')
    fileHandler.setFormatter(log_formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(log_formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)

def check_path(endpoints):
    for create_path in endpoints:
        try:
            os.makedirs(path + create_path)
        except FileExistsError:
            pass


def init_log(endpoints, new_path):
    global path
    path = new_path
    check_path(endpoints)
    for endpoint in endpoints:
        setup_logger(endpoint, path + endpoint + '/' + endpoint + log)
