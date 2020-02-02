import json
from flask import Flask, jsonify, request

from data.data_provider import get_keras_data_set
from wrapper.keras_wrapper import KerasWrapper, ModelBuilder, DenseLayerBuilder


def build_model(values: json):
    model = ModelBuilder().model()
    for _layer in values['layers']:

        layer = DenseLayerBuilder(). \
            units(_layer['units']). \
            activation(_layer['activation'])

        if "input_shape" in _layer:
            layer = layer.input_shape(_layer['input_shape'])

        model = model.layer(layer.build())
    return model.build()


keras_wrapper = KerasWrapper()
app = Flask(__name__)


@app.route('/network/new', methods=['POST'])
def new_network():
    values = request.get_json()
    required = ['name', 'layers']
    if not all(k in values for k in required):
        return 'Missing values', 400
    else:

        keras_wrapper.add_model(values['name'], build_model(values))
        response = {
            "Message": f"New Network {values['name']} added."
        }
        return jsonify(response), 200


@app.route('/network/compile', methods=['POST'])
def compile_network():
    values = request.get_json()
    required = ['name', 'optimizer', 'loss', 'metrics']
    if not all(k in values for k in required):
        return 'Missing values', 400
    else:

        keras_wrapper.compile(values['name'],
                              optimizer=values['optimizer'],
                              loss=values['loss'],
                              metrics=values['metrics'])
        response = {
            "Message": f"Network {values['name']} compiled."
        }
        return jsonify(response), 200


@app.route('/network/train', methods=['POST'])
def train_network():
    values = request.get_json()
    required = ['name', 'data_set', 'epochs', 'batch_size']
    if not all(k in values for k in required):
        return 'Missing values', 400
    else:

        if keras_wrapper.models.get(values["name"], None):
            response = {
                "Message": f"Network {values['name']} not find."
            }
            return jsonify(response), 200

        if not keras_wrapper.models.get(values["name"], None).compiled:
            response = {
                "Message": f"Network {values['name']} need to be compiled."
            }
            return jsonify(response), 200

        (train_data, train_labels), (val_data, val_labels) = get_keras_data_set(values["data_set"])
        keras_wrapper.train(values["name"],
                            train_data=train_data,
                            train_labels=train_labels,
                            val_data=val_data,
                            val_labels=val_labels,
                            epochs=values['epochs'],
                            batch_size=values['batch_size'])
        response = {
            "Message": f"Network {values['name']} training complete."
        }
        return jsonify(response), 200


@app.route('/', methods=['GET'])
def default():
    response = {
        "Message": "API running"
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
