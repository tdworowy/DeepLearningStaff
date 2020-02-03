import numpy as np
import pytest
import json

from data.data_provider import get_keras_data_set
from data_utils.data_utils import vectorized_sequences
from wrapper.keras_wrapper import KerasWrapper, ModelBuilder, DenseLayerBuilder

with open("../resources/new_network_json.json") as json_file:
    new_network_json = json.load(json_file)

with open("../resources/compile_network_json.json") as json_file:
    compile_network_json = json.load(json_file)

with open("../resources/train_network_json.json") as json_file:
    train_network_json = json.load(json_file)


def build_model(values: json):
    model = ModelBuilder().model()
    for _layer in values['layers']:

        layer = DenseLayerBuilder(). \
            units(int(_layer['units'])). \
            activation(_layer['activation'])

        if "input_shape" in _layer:
            layer = layer.input_shape(tuple(map(int, _layer['input_shape'].split(','))))

        model = model.layer(layer.build())
    return model.build()


@pytest.fixture(autouse=True)
def keras_wrapper():
    return KerasWrapper()


def test_add_model(keras_wrapper):
    model = build_model(new_network_json)
    keras_wrapper.add_model(new_network_json['name'], model)

    assert keras_wrapper.models.get(new_network_json['name'])
    assert not keras_wrapper.models.get(new_network_json['name']).trained
    assert not keras_wrapper.models.get(new_network_json['name']).compiled
    assert keras_wrapper.models.get(new_network_json['name']).model == model


def test_compile_model(keras_wrapper):
    model = build_model(new_network_json)
    keras_wrapper.add_model(new_network_json['name'], model)

    keras_wrapper.compile(compile_network_json['name'],
                          optimizer=compile_network_json['optimizer'],
                          loss=compile_network_json['loss'],
                          metrics=compile_network_json['metrics'])

    assert keras_wrapper.models.get(new_network_json['name'])
    assert keras_wrapper.models.get(new_network_json['name']).compiled
    assert not keras_wrapper.models.get(new_network_json['name']).trained
    assert keras_wrapper.models.get(new_network_json['name']).model == model


def test_train_model(keras_wrapper):
    model = build_model(new_network_json)
    keras_wrapper.add_model(new_network_json['name'], model)

    keras_wrapper.compile(compile_network_json['name'],
                          optimizer=compile_network_json['optimizer'],
                          loss=compile_network_json['loss'],
                          metrics=compile_network_json['metrics'])

    (train_data, train_labels), (val_data, val_labels) = get_keras_data_set(train_network_json["data_set"],
                                                                            int(new_network_json['layers'][0]['input_shape']))

    keras_wrapper.train(train_network_json["name"],
                        train_data=train_data,
                        train_labels=train_labels,
                        val_data=val_data,
                        val_labels=val_labels,
                        epochs=train_network_json['epochs'],
                        batch_size=train_network_json['batch_size'])

    assert keras_wrapper.models.get(new_network_json['name'])
    assert keras_wrapper.models.get(new_network_json['name']).compiled
    assert keras_wrapper.models.get(new_network_json['name']).trained
    assert keras_wrapper.models.get(new_network_json['name']).model == model
