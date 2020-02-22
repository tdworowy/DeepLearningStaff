import logging
import sys
from os import path

logs_path = path.join(path.dirname(path.realpath(__file__)), "../logs")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    handlers=[
                        logging.FileHandler("{0}/{1}.log".format(logs_path, "logs")),
                        logging.StreamHandler(sys.stdout)
                    ]
                    )


def get_logger(name: str):
    return logging.getLogger(name)