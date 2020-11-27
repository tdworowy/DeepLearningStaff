import logging
import os
import string
import time
from importlib import reload
from random import choice


class TestsLogger:

    def __init__(self):
        logging.shutdown()
        reload(logging)
        logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S', )
        self.loggers = []

    def add_log_file(self, path):
        self.log_file = path
        for logger in self.loggers:
            if self.log_file in [handler.baseFilename for handler in logger.handlers if
                                 hasattr(handler, 'baseFilename')]:
                self.logger = logger
        else:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setFormatter(logging.Formatter("%(levelname)s|%(asctime)s|%(message)s"))
            file_handler.setLevel(logging.DEBUG)

            new_logger = logging.getLogger("Logger%s" % get_millis())
            new_logger.setLevel(logging.DEBUG)
            new_logger.addHandler(file_handler)

            self.loggers.append(new_logger)
            self.logger = new_logger

    def clear_loggers(self):
        while self.loggers: self.loggers.pop()

    def log(self):
        return self.logger


random_string = lambda length: ''.join([choice(string.ascii_letters + string.digits) for n in range(length)])


def take_screenshot(driver, path, file):
    forbidden_characters = ["{", "}", " ", ",", ";", "(", ")", '"', '"', ":"]
    for character in forbidden_characters:
        file = file.replace(character, "_")
    driver.save_screenshot(os.path.join(path, f"{file}_{random_string(5)}_.png"))


def get_millis():
    return int(round(time.time() * 1000))
