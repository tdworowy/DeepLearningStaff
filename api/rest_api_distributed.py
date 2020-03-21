import json

import mpld3
import yaml
from flask import Flask, jsonify, request

from _logging._logger import get_logger
from data.data_provider import data_sources
from nats_wrapper.nats_wrapper import send_message
from visualization.vizualization import plot


logger = get_logger(__name__)


def prepare_response(message: json, status: int):
    logger.info(f"Response:{message}")
    response = jsonify(message)
    return response, status


app = Flask(__name__)


@app.after_request
def after_request(response):
    logger.info(f"Request:{request}")

    logger.info(f"Request json:{request.get_json(silent=True)}")

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route('/network/new', methods=['POST'])
def new_network():
    values = request.get_json()
    required = ['name', 'layers']
    if not all(k in values for k in required):
        return prepare_response({'Massage': 'Missing values'}, 400)
    else:

        response = send_message(service_name="new_network",
                                data=values,
                                logger=logger,
                                config=read_config())

        return prepare_response(response, 200)


@app.route('/network/compile', methods=['POST'])
def compile_network():
    values = request.get_json()
    required = ['name', 'optimizer', 'loss', 'metrics']
    if not all(k in values for k in required):
        return prepare_response({"Message": "Missing value"}, 400)
    else:
        networks = send_message(service_name="get_networks",
                                data="",
                                logger=logger,
                                config=read_config())
        if values["name"] not in networks['Networks']:
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(response, 200)

    response = send_message(service_name="compile_network",
                            data=values,
                            logger=logger,
                            config=read_config())

    return prepare_response(response, 200)


@app.route('/network/train', methods=['POST'])
def train_network():
    values = request.get_json()
    required = ['name', 'data_set', 'epochs', 'batch_size', 'test_sample_size']
    if not all(k in values for k in required):
        return prepare_response({"Message": "Missing value"}, 400)
    else:
        networks = send_message(service_name="get_networks",
                                data="",
                                logger=logger,
                                config=read_config())
        if values["name"] not in networks['Networks']:
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(response, 200)

        network_details = send_message(service_name="get_network_details",
                                       data={'name': values["name"]},
                                       logger=logger,
                                       config=read_config())
        if not network_details["Compiled"]:
            response = {
                "Message": f"Network {values['name']} need to be compiled."
            }
            return prepare_response(response, 200)

        response = send_message(service_name="train_network",
                                data=values,
                                logger=logger,
                                config=read_config())
        return prepare_response(response, 200)


@app.route('/network/delete', methods=['DELETE'])
def delete_network():
    values = request.get_json()
    required = ['name']
    if not all(k in values for k in required):
        return prepare_response({'Massage': 'Missing values'}, 400)
    else:
        networks = send_message(service_name="get_networks",
                                data="",
                                logger=logger,
                                config=read_config())
        if values["name"] not in networks['Networks']:
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(response, 200)

        response = send_message(service_name="delete_network",
                                data=values,
                                logger=logger,
                                config=read_config())
        return prepare_response(response, 200)


@app.route('/network/evaluate', methods=['POST'])
def evaluate_network():
    values = request.get_json()
    required = ['name']
    if not all(k in values for k in required):
        return prepare_response({'Massage': 'Missing values'}, 400)
    else:
        networks = send_message(service_name="get_networks",
                                data="",
                                logger=logger,
                                config=read_config())
        if values["name"] not in networks['Networks']:
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(response, 200)

        response = send_message(service_name="evaluate_network",
                                data=values,
                                logger=logger,
                                config=read_config())
        return prepare_response(response, 200)


@app.route('/', methods=['GET'])
def default():
    response = {
        "Message": "API running"
    }
    return prepare_response(response, 200)


@app.route('/networks', methods=['GET'])
def get_networks():
    response = send_message(service_name="get_networks",
                            data="",
                            logger=logger,
                            config=read_config())
    return prepare_response(response, 200)


@app.route('/network/<name>', methods=['GET'])
def get_network_details(name):
    response = send_message(service_name="get_network_details",
                            data={'name': name},
                            logger=logger,
                            config=read_config())
    return prepare_response(response, 200)


@app.route('/network/history/<name>', methods=['GET'])
def get_network_history(name):
    response = send_message(service_name="get_network_history",
                            data={'name': name},
                            logger=logger,
                            config=read_config())
    return prepare_response(response, 200)


@app.route('/network/plot/accuracy/<name>', methods=['GET'])
def get_plot_accuracy(name):
    history = send_message(service_name="get_network_history",
                           data={'name': name},
                           logger=logger,
                           config=read_config())
    history = history["History"]
    acc = list(history['acc'].values())
    val_acc = list(history['val_acc'].values())
    epochs = range(1, len(acc) + 1)

    plt_html = mpld3.fig_to_html(plot(epochs=epochs,
                                      train_values=acc,
                                      validation_values=val_acc,
                                      metric="Accuracy"))
    return plt_html


@app.route('/network/plot/loss/<name>', methods=['GET'])
def get_plot_loss(name):
    history = send_message(service_name="get_network_history",
                           data={'name': name},
                           logger=logger,
                           config=read_config())
    history = history["History"]
    loss = list(history['loss'].values())
    val_loss = list(history['val_loss'].values())
    epochs = range(len(loss))

    plt_html = mpld3.fig_to_html(plot(epochs=epochs,
                                      train_values=loss,
                                      validation_values=val_loss,
                                      metric="Loss"))
    return plt_html


@app.route('/data-sources', methods=['GET'])
def get_data_sources():
    response = data_sources()
    response = {"Dat_Sources": response}
    return prepare_response(response, 200)


@app.route('/healthCheck', methods=['GET'])
def health_check():
    response = send_message(service_name="health_check",
                            data="",
                            logger=logger,
                            config=read_config())
    response = {
        "Message": response
    }
    return prepare_response(response, 200)


def get_app():
    return app


def read_config():
    with open('../config.yaml') as file:
        return yaml.safe_load(file)
