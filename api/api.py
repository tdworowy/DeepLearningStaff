from flask import Flask, jsonify, request

from wrapper.keras_wrapper import KerasWrapper, ModelBuilder, DenseLayerBuilder


class API:
    @staticmethod
    def start(host, port):
        app = Flask(__name__)
        keras_wrapper = KerasWrapper()
        app.run(host=host, port=port)

        @app.route('/network/new', methods=['POST'])
        def new_transaction():
            values = request.get_json()
            required = ['name', 'optimizer', 'loss', 'metrics', 'layers']
            if not all(k in values for k in required):
                return 'Missing values', 400
            else:
                model = ModelBuilder().model()
                for _layer in values['layers']:
                    layer = DenseLayerBuilder().\
                        units(_layer['units']).\
                        activation(_layer['activation'])

                    if "input_shape" in _layer:
                        layer = layer.input_shape(_layer['input_shape'])

                    model = model.layer(layer.build())

                keras_wrapper.add_model(values['name'], model.build())


if __name__ == '__main__':
    API.start(host='0.0.0.0', port=5000)
