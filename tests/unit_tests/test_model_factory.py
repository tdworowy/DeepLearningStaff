import json
from os import path

from keras_wrapper.model_factory import build_layer

current_dir = path.join(path.dirname(path.realpath(__file__)))
with open(path.join(current_dir, "../resources/build_layers_test_network_json.json")) as json_file:
    new_network_json = json.load(json_file)


def test_build_layers():
    for layer in new_network_json['layers']:
        layer = build_layer(layer)
        layer.build()
