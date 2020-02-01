import json

from flask import Flask, jsonify, request

from wrapper.keras_wrapper import KerasWrapper, ModelBuilder, DenseLayerBuilder


def get_model(values: json):
    model = ModelBuilder().model()
    for _layer in values['layers']:
        layer = DenseLayerBuilder(). \
            units(_layer['units']). \
            activation(_layer['activation'])
        if "input_shape" in _layer:
            layer = layer.input_shape(_layer['input_shape'])

        model = model.layer(layer.build())
    return model


app = Flask(__name__)


class API:

    @staticmethod
    def start(app, host, port):
        app.run(host=host, port=port)

    @staticmethod
    def new_api():
        keras_wrapper = KerasWrapper()
        app = Flask(__name__)

        @app.route('/network/new', methods=['POST'])
        def new_transaction():
            values = request.get_json()
            required = ['name', 'optimizer', 'loss', 'metrics', 'layers']
            if not all(k in values for k in required):
                return 'Missing values', 400
            else:

                keras_wrapper.add_model(values['name'], get_model(values).build())
                response = {
                    "Message": "New Network added."
                }
                return jsonify(response), 200

        @app.route('/', methods=['GET'])
        def default():
            response = {
                "Message": "API running"
            }
            return jsonify(response), 200

        return app


if __name__ == '__main__':
    API.start(API.new_api(), host='0.0.0.0', port=5000)
