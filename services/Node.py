import uuid
import yaml
import asyncio
from nats_wrapper.nats_wrapper import call_service
from services import get_services
from _logging._logger import get_logger

services = get_services()
logger = get_logger("Node_" + str(uuid.uuid4()))


def read_config():
    with open('../config.yaml') as file:
        return yaml.safe_load(file)


if __name__ == "__main__":
    config = read_config()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(call_service(nats_port=config.get('nats_port'),
                                         service_topic=config.get('service_topic'),
                                         response_topic=config.get('response_topic'),
                                         loop=loop,
                                         logger=logger,
                                         services=services))
    loop.run_forever()
