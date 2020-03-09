import json

import mpld3
import yaml
from flask import Flask, jsonify, request
from _logging._logger import get_logger
from data.data_provider import get_keras_data_set, data_sources
from visualization.vizualization import plot
from wrapper.keras_wrapper import KerasWrapper, ModelBuilder, DenseLayerBuilder
# TODO rewrite to use NATS message brocker
logger = get_logger(__name__)


def build_model(values: json):
    model = ModelBuilder().model()
    for _layer in values['layers']:

        layer = DenseLayerBuilder(). \
            units(_layer['units']). \
            activation(_layer['activation'])

        if "input_shape" in _layer:
            if _layer["input_shape"] != "":
                layer = layer.input_shape(tuple(map(int, _layer['input_shape'].split(','))))

        model = model.layer(layer.build())
    return model.build()


def prepare_response(message: json, status: int):
    logger.info(f"Response:{message}")
    response = jsonify(message)
    return response, status


test_data_dict = dict()
keras_wrapper = KerasWrapper()
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

        keras_wrapper.add_model(values['name'], build_model(values))
        response = {
            "Message": f"New Network {values['name']} added."
        }
        return prepare_response(response, 200)


@app.route('/network/compile', methods=['POST'])
def compile_network():
    values = request.get_json()
    required = ['name', 'optimizer', 'loss', 'metrics']
    if not all(k in values for k in required):
        return prepare_response({"Message": "Missing value"}, 400)
    else:
        if not keras_wrapper.models.get(values["name"], None):
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(response, 200)

        keras_wrapper.compile(model_name=values['name'],
                              optimizer=values['optimizer'],
                              loss=values['loss'],
                              metrics=values['metrics'])
        response = {
            "Message": f"Network {values['name']} compiled."
        }
        return prepare_response(response, 200)


@app.route('/network/train', methods=['POST'])
def train_network():
    values = request.get_json()
    required = ['name', 'data_set', 'epochs', 'batch_size', 'test_sample_size']
    if not all(k in values for k in required):
        return prepare_response({"Message": "Missing value"}, 400)
    else:

        if not keras_wrapper.models.get(values["name"], None):
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(response, 200)

        if not keras_wrapper.models.get(values["name"], None).compiled:
            response = {
                "Message": f"Network {values['name']} need to be compiled."
            }
            return prepare_response(response, 200)

        (train_data, train_labels), \
        (val_data, val_labels), \
        (test_data, test_labels) = get_keras_data_set(values["data_set"],
                                                      int(values['input_shape']),
                                                      int(values['test_sample_size']))

        test_data_dict[values['name']] = (test_data, test_labels)

        keras_wrapper.train(model_name=values["name"],
                            train_data=train_data,
                            train_labels=train_labels,
                            val_data=val_data,
                            val_labels=val_labels,
                            epochs=int(values['epochs']),
                            batch_size=int(values['batch_size']))
        response = {
            "Message": f"Network {values['name']} training complete."
        }
        return prepare_response(response, 200)


@app.route('/network/delete', methods=['DELETE'])
def delete_network():
    values = request.get_json()
    required = ['name']
    if not all(k in values for k in required):
        return prepare_response({'Massage': 'Missing values'}, 400)
    else:
        if not keras_wrapper.models.get(values["name"], None):
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(response, 200)

        keras_wrapper.models.pop(values['name'])
        response = {
            "Message": f"Network {values['name']} deleted."
        }
        return prepare_response(response, 200)


@app.route('/network/evaluate', methods=['POST'])
def evaluate_network():
    values = request.get_json()
    required = ['name']
    if not all(k in values for k in required):
        return prepare_response({'Massage': 'Missing values'}, 400)
    else:
        if not keras_wrapper.models.get(values["name"], None):
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(response, 200)

        test_loss, test_acc = keras_wrapper.evaluate(model_name=values['name'],
                                                     test_data=test_data_dict[values['name']][0],
                                                     test_labels=test_data_dict[values['name']][1])
        response = {
            "Test_accuracy": test_acc,
            "Test_loss": test_loss
        }
        return prepare_response(response, 200)


@app.route('/', methods=['GET'])
def default():
    response = {
        "Message": "API running"
    }
    return prepare_response(response, 200)


@app.route('/networks', methods=['GET'])
def get_networks():
    response = list(keras_wrapper.models.keys()) if keras_wrapper.models.keys() else [""]
    response = {"Networks": response}
    return prepare_response(response, 200)


@app.route('/network/<name>', methods=['GET'])
def get_network_details(name):
    compiled = keras_wrapper.models[name].compiled
    trained = keras_wrapper.models[name].trained
    model_json = keras_wrapper.models[name].model.to_json()
    response = {"Name": name, "Compiled": compiled, "Trained": trained, "Model": model_json}
    return prepare_response(response, 200)


@app.route('/network/history/<name>', methods=['GET'])
def get_network_history(name):
    history_json = keras_wrapper.models[name].history_json
    response = {"Name": name, "History": history_json}
    return prepare_response(response, 200)


@app.route('/network/plot/accuracy/<name>', methods=['GET'])
def get_plot_accuracy(name):
    history = json.loads(keras_wrapper.models[name].history_json)
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
    history = json.loads(keras_wrapper.models[name].history_json)
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


def get_app():
    return app


def read_config():
    with open('../config.yaml') as file:
        return yaml.safe_load(file)
