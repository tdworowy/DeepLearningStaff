import yaml
import asyncio
from nats.aio.client import Client as NATS

from _logging._logger import get_logger

services = {}
logger = get_logger(__name__)


def read_config():
    with open('../config.yaml') as file:
        return yaml.safe_load(file)


async def call_service(nats_port: str, topic: str, loop):
    nc = NATS()

    await nc.connect(servers=["nats://127.0.0.1:4222"], loop=loop)

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print(f"Received a message on '{subject} {reply}': {data}")
        logger.info(f"Received a message on '{subject} {reply}': {data}")

    sid = await nc.subscribe(topic, cb=message_handler)


if __name__ == "__main__":
    config = read_config()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(call_service(nats_port=config.get('nats_port'),
                                         topic=config.get('topic'),
                                         loop=loop))  # TODO different run
    loop.close()
