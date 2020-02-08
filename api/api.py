import json
from flask import Flask, jsonify, request, make_response
from data.data_provider import get_keras_data_set
from wrapper.keras_wrapper import KerasWrapper, ModelBuilder, DenseLayerBuilder


def build_model(values: json):
    model = ModelBuilder().model()
    for _layer in values['layers']:

        layer = DenseLayerBuilder(). \
            units(_layer['units']). \
            activation(_layer['activation'])

        if "input_shape" in _layer:
            layer = layer.input_shape(tuple(map(int, _layer['input_shape'].split(','))))

        model = model.layer(layer.build())
    return model.build()


def prepare_response(message: json, method: str, status: int):
    response = make_response(jsonify(message), status)
    response.headers.extend({"Access-Control-Allow-Origin": "*"})
    response.headers.extend({"Access-Control-Allow-Methods": method})
    response.headers.extend({"Access-Control-Allow-Headers", "accept, content-type"})
    return response


app = Flask(__name__)


@app.route('/network/new', methods=['POST'])
def new_network():
    values = request.get_json()
    required = ['name', 'layers']
    if not all(k in values for k in required):
        return prepare_response('Missing values', 'POST, OPTIONS', 400)
    else:

        keras_wrapper.add_model(values['name'], build_model(values))
        response = {
            "Message": f"New Network {values['name']} added."
        }
        return prepare_response(jsonify(response), 'POST, OPTIONS', 200)


@app.route('/network/compile', methods=['POST'])
def compile_network():
    values = request.get_json()
    required = ['name', 'optimizer', 'loss', 'metrics']
    if not all(k in values for k in required):
        prepare_response(jsonify({"Message": "Missing value"}), 'POST, OPTIONS', 400)
    else:
        if not keras_wrapper.models.get(values["name"], None):
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(jsonify(response), 'POST, OPTIONS', 200)

        keras_wrapper.compile(model_name=values['name'],
                              optimizer=values['optimizer'],
                              loss=values['loss'],
                              metrics=values['metrics'])
        response = {
            "Message": f"Network {values['name']} compiled."
        }
        return prepare_response(jsonify(response), 'POST, OPTIONS', 200)


@app.route('/network/train', methods=['POST'])
def train_network():
    values = request.get_json()
    required = ['name', 'data_set', 'epochs', 'batch_size']
    if not all(k in values for k in required):
        return prepare_response(jsonify({"Message": "Missing value"}), 'POST, OPTIONS', 400)
    else:

        if not keras_wrapper.models.get(values["name"], None):
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(jsonify(response), 'POST, OPTIONS', 200)

        if not keras_wrapper.models.get(values["name"], None).compiled:
            response = {
                "Message": f"Network {values['name']} need to be compiled."
            }
            return prepare_response(jsonify(response), 'POST, OPTIONS', 200)

        (train_data, train_labels), (val_data, val_labels) = get_keras_data_set(values["data_set"],
                                                                                int(values['input_shape']))
        keras_wrapper.train(model_name=values["name"],
                            train_data=train_data,
                            train_labels=train_labels,
                            val_data=val_data,
                            val_labels=val_labels,
                            epochs=values['epochs'],
                            batch_size=values['batch_size'])
        response = {
            "Message": f"Network {values['name']} training complete."
        }
        return prepare_response(jsonify(response), 'POST, OPTIONS', 200)


@app.route('/network/delete', methods=['DELETE'])
def delete_network():
    values = request.get_json()
    required = ['name']
    if not all(k in values for k in required):
        return 'Missing values', 400
    else:
        if not keras_wrapper.models.get(values["name"], None):
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(jsonify(response), 'DELETE, OPTIONS', 200)
        keras_wrapper.models.pop(values['name'])
        response = {
            "Message": f"Network {values['name']} deleted."
        }
        return prepare_response(jsonify(response), 'DELETE, OPTIONS', 200)


@app.route('/', methods=['GET'])
def default():
    response = {
        "Message": "API running"
    }
    return prepare_response(jsonify(response), 'GET', 200)


@app.route('/networks', methods=['GET'])
def get_networks():
    response = {
        keras_wrapper.models.keys()
    }
    return prepare_response(jsonify(response), 'GET', 200)


@app.route('/data-sources', methods=['GET'])
def get_data_sources():
    response = {
        get_data_sources()
    }
    return prepare_response(jsonify(response), 'GET', 200)


if __name__ == '__main__':
    keras_wrapper = KerasWrapper()
    app.run(host='0.0.0.0', port=5000, threaded=False)
