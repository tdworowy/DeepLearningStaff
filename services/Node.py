import time
import uuid
import yaml
import asyncio
from nats_wrapper.nats_wrapper import call_service, send_message
from _logging._logger import get_logger
from multiprocessing import Process
from threading import Thread


def read_config():
    with open('../config.yaml') as file:
        return yaml.safe_load(file)


def synchronize(logger):
    while 1:
        send_message(service_name="synchronize_data", # TODO fix it 
                     data="",
                     logger=logger,
                     config=read_config())
        time.sleep(2)


def start_node(config: dict):
    from services import get_services
    services = get_services()

    logger = get_logger("Node_" + str(uuid.uuid4()))
    loop = asyncio.new_event_loop()
    loop.run_until_complete(call_service(nats_port=config.get('nats_port'),
                                         service_topic=config.get('service_topic'),
                                         response_topic=config.get('response_topic'),
                                         loop=loop,
                                         logger=logger,
                                         services=services))

    thread = Thread(target=synchronize, args=(logger,))
    thread.start()
    loop.run_forever()


if __name__ == "__main__":
    nods_count = 1
    config = read_config()
    for i in range(nods_count):
        node_process = Process(target=start_node, args=(config,))
        node_process.start()
