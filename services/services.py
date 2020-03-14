from _logging._logger import get_logger
from wrapper.keras_wrapper import KerasWrapper

logger = get_logger(__name__)
keras_wrapper = KerasWrapper()

services = {}


def health_check_service(*args):
    logger.info("Call service:health_check")
    return '{"health": "Live"}'


services["health_check"] = health_check_service


def get_services():
    return services.copy()
