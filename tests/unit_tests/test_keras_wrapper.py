import json
import pytest
from data.data_provider import get_keras_data_set
from keras_wrapper.keras_wrapper import KerasWrapper
import os

from keras_wrapper.model_factory import build_model

with open("../resources/new_network_json.json") as json_file:
    new_network_json = json.load(json_file)

with open("../resources/compile_network_json.json") as json_file:
    compile_network_json = json.load(json_file)

with open("../resources/train_network_json.json") as json_file:
    train_network_json = json.load(json_file)


@pytest.fixture(autouse=True)
def keras_wrapper():
    return KerasWrapper()


@pytest.fixture(autouse=True)
def model():
    return build_model(new_network_json)


def test_add_model(keras_wrapper, model):
    keras_wrapper.add_model(new_network_json['name'], model)

    assert keras_wrapper.models.get(new_network_json['name'])
    assert not keras_wrapper.models.get(new_network_json['name']).trained
    assert not keras_wrapper.models.get(new_network_json['name']).compiled
    assert keras_wrapper.models.get(new_network_json['name']).model == model


def test_save_model(keras_wrapper, model):
    file_name = "test.hdf5"
    keras_wrapper.add_model(new_network_json['name'], model)
    keras_wrapper.serialize_model(new_network_json['name'], file_name)
    assert os.path.isfile(file_name)


def test_compile_model(keras_wrapper, model):
    keras_wrapper.add_model(new_network_json['name'], model)

    keras_wrapper.compile(model_name=compile_network_json['name'],
                          optimizer=compile_network_json['optimizer'],
                          loss=compile_network_json['loss'],
                          metrics=compile_network_json['metrics'])

    assert keras_wrapper.models.get(new_network_json['name'])
    assert keras_wrapper.models.get(new_network_json['name']).compiled
    assert not keras_wrapper.models.get(new_network_json['name']).trained
    assert keras_wrapper.models.get(new_network_json['name']).model == model


def test_train_model(keras_wrapper, model):
    keras_wrapper.add_model(new_network_json['name'], model)

    keras_wrapper.compile(model_name=compile_network_json['name'],
                          optimizer=compile_network_json['optimizer'],
                          loss=compile_network_json['loss'],
                          metrics=compile_network_json['metrics'])

    (train_data, train_labels), \
    (val_data, val_labels), \
    (test_data, test_labels) = get_keras_data_set(
        train_network_json["data_set"],
        int(train_network_json['input_shape']),
        int(train_network_json['test_sample_size']))

    keras_wrapper.train(model_name=train_network_json["name"],
                        train_data=train_data,
                        train_labels=train_labels,
                        val_data=val_data,
                        val_labels=val_labels,
                        epochs=int(train_network_json['epochs']),
                        batch_size=int(train_network_json['batch_size']))

    assert keras_wrapper.models.get(new_network_json['name'])
    assert keras_wrapper.models.get(new_network_json['name']).compiled
    assert keras_wrapper.models.get(new_network_json['name']).trained
    assert keras_wrapper.models.get(new_network_json['name']).model == model


def test_evaluate_model(keras_wrapper, model):
    keras_wrapper.add_model(new_network_json['name'], model)

    keras_wrapper.compile(model_name=compile_network_json['name'],
                          optimizer=compile_network_json['optimizer'],
                          loss=compile_network_json['loss'],
                          metrics=compile_network_json['metrics'])

    (train_data, train_labels), \
    (val_data, val_labels), \
    (test_data, test_labels) = get_keras_data_set(
        train_network_json["data_set"],
        int(train_network_json['input_shape']),
        int(train_network_json['test_sample_size']))

    keras_wrapper.train(model_name=train_network_json["name"],
                        train_data=train_data,
                        train_labels=train_labels,
                        val_data=val_data,
                        val_labels=val_labels,
                        epochs=int(train_network_json['epochs']),
                        batch_size=int(train_network_json['batch_size']))

    evaluate_results = keras_wrapper.evaluate(model_name=train_network_json["name"],
                                              test_data=test_data,
                                              test_labels=test_labels)
    assert evaluate_results is not None
    assert keras_wrapper.models.get(new_network_json['name'])
    assert keras_wrapper.models.get(new_network_json['name']).compiled
    assert keras_wrapper.models.get(new_network_json['name']).trained
    assert keras_wrapper.models.get(new_network_json['name']).model == model
