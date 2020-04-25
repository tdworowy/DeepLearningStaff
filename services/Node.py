import uuid
from os import path

import yaml
import asyncio
from nats_wrapper.nats_wrapper import call_service
from _logging._logger import get_logger


def read_config():
    current_dir = path.join(path.dirname(path.realpath(__file__)))
    with open(path.join(current_dir, '../config.yaml')) as file:
        return yaml.safe_load(file)


async def synchronize(services, logger):
    while 1:
        response = services["synchronize_data"]("")
        logger.info(response)
        await asyncio.sleep(10)


def start_node(config: dict):
    import services
    services = services.get_services()
    logger = get_logger("Node_" + str(uuid.uuid4()))
    loop = asyncio.new_event_loop()

    async def run(config):
        await asyncio.gather(
            call_service(
                nats_host=config.get('nats_host'),
                nats_port=config.get('nats_port'),
                service_topic=config.get('service_topic'),
                response_topic=config.get('response_topic'),
                loop=loop,
                logger=logger,
                services=services),
            synchronize(services, logger)
        )

    loop.run_until_complete(run(config))
    loop.run_forever()


if __name__ == "__main__":
    config = read_config()
    start_node(config)
