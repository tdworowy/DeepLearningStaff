import asyncio

import yaml
from nats.aio.client import Client as NATS


def read_config():
    with open("../config.yaml") as file:
        return yaml.safe_load(file)


async def run(nats_port: str, topic: str, loop):
    nc = NATS()
    await nc.connect(servers=[f"nats://127.0.0.1:{nats_port}"], loop=loop)

    await nc.publish(topic, b'{"service_name":"health_check", "data":{}}')

    await nc.flush()
    await nc.close()


if __name__ == "__main__":
    config = read_config()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        run(
            nats_port=config.get("nats_port"),
            topic=config.get("service_topic"),
            loop=loop,
        )
    )
    loop.close()
