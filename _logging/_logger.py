import logging
from os import path

logs_path = path.join(path.dirname(path.realpath(__file__)), "../logs")
logging.basicConfig(filename=path.join(logs_path, 'logs.log'),
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger('logger')


def get_logger():
    return logger
