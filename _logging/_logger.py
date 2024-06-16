import logging
import sys
from os import path, mkdir

logs_path = path.join(path.dirname(path.realpath(__file__)), "../logs")
if not path.isdir(logs_path):
    mkdir(logs_path)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(f"{logs_path}/logs.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


def get_logger(name: str):
    return logging.getLogger(name)
