import json
import uuid

import yaml
import asyncio
from nats.aio.client import Client as NATS

from services import get_services
from _logging._logger import get_logger

services = get_services()
logger = get_logger("Node_" + str(uuid.uuid4()))


def read_config():
    with open('../config.yaml') as file:
        return yaml.safe_load(file)


async def call_service(nats_port: str, service_topic: str, response_topic, loop):
    nc = NATS()

    await nc.connect(servers=[f"nats://127.0.0.1:{nats_port}"], loop=loop)

    async def message_handler(msg):
        try:
            subject = msg.subject
            data = msg.data.decode()
            logger.info(f"Received a message on '{subject}': {data}")
            data = json.loads(data)
            response = services[data['service_name']](data['data'])
            logger.info(f"Response from service'{data['service_name']}': {response}")
            await nc.publish(response_topic, response.encode())
        except Exception as ex:
            logger.error(ex)

    sid = await nc.subscribe(service_topic, cb=message_handler)


if __name__ == "__main__":
    config = read_config()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(call_service(nats_port=config.get('nats_port'),
                                         service_topic=config.get('service_topic'),
                                         response_topic=config.get('response_topic'),
                                         loop=loop))
    loop.run_forever()
