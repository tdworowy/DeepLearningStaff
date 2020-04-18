import json
import sys
from multiprocessing import Queue
import asyncio
from threading import Thread
from nats.aio.client import Client as NATS


async def call_service(nats_host: str, nats_port: str, service_topic: str, services, response_topic, logger, loop):
    nc = NATS()

    await nc.connect(servers=[f"nats://{nats_host}:{nats_port}"], loop=loop)

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
            logger.error(f"Exception in service {data['service_name']}: {ex}")

    sid = await nc.subscribe(service_topic, cb=message_handler)


def send_message(service_name: str, data: json, logger, config):
    responses = Queue()

    async def call_service(nats_host: str, nats_port: str, service_topic: str, response_topic: str, loop):
        nc = NATS()

        await nc.connect(servers=[f"nats://{nats_host}:{nats_port}"], loop=loop)
        message = {'service_name': service_name, 'data': data}

        async def message_handler(msg):
            try:
                subject = msg.subject
                data = msg.data.decode()
                logger.info(f"Received a message on '{subject}': {data}")
                data = json.loads(data)
                responses.put(data)
            except Exception as ex:
                type, value, traceback = sys.exc_info()
                logger.error(f"Exception in service {data['service_name']}: {ex}")
                logger.error(f"Type: {type} Value: {value} Traceback: {traceback}")

        sid = await nc.subscribe(response_topic, cb=message_handler)
        await nc.publish(service_topic, json.dumps(message).encode())

    loop = asyncio.new_event_loop()
    loop.run_until_complete(call_service(
        nats_host=config.get('nats_host'),
        nats_port=config.get('nats_port'),
        service_topic=config.get('service_topic'),
        response_topic=config.get('response_topic'),
        loop=loop))

    Thread(target=loop.run_forever).start()  # might not be the best solution

    response = responses.get(timeout=900)
    loop.stop()
    return response
