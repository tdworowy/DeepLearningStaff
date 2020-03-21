import json

from _logging._logger import get_logger
from data.data_provider import get_keras_data_set
from wrapper.keras_wrapper import KerasWrapper, ModelBuilder, DenseLayerBuilder

logger = get_logger(__name__)
keras_wrapper = KerasWrapper()

services = {}
test_data_dict = {}


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


def health_check_service(*args):
    logger.info("Call service:health_check")
    return '{"health": "Live"}'


def new_network_service(values: json):
    keras_wrapper.add_model(values['name'], build_model(values))
    response = {
        "Message": f"New Network {values['name']} added."
    }
    return json.dumps(response)


def compile_network(values: json):
    keras_wrapper.compile(model_name=values['name'],
                          optimizer=values['optimizer'],
                          loss=values['loss'],
                          metrics=values['metrics'])
    response = {
        "Message": f"Network {values['name']} compiled."
    }
    return json.dumps(response)


def train_network(values: json):
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
    return json.dumps(response)


def get_networks(*args):
    response = list(keras_wrapper.models.keys()) if keras_wrapper.models.keys() else [""]
    response = {"Networks": response}
    return json.dumps(response)


def get_network_details(values: json):
    name = values["name"]
    compiled = keras_wrapper.models[name].compiled
    trained = keras_wrapper.models[name].trained
    model_json = keras_wrapper.models[name].model.to_json()
    response = {"Name": name, "Compiled": compiled, "Trained": trained, "Model": model_json}
    return json.dumps(response)


def delete_network(values: json):
    keras_wrapper.models.pop(values['name'])
    response = {
        "Message": f"Network {values['name']} deleted."
    }
    return json.dumps(response)


def evaluate_network(values: json):
    test_loss, test_acc = keras_wrapper.evaluate(model_name=values['name'],
                                                 test_data=test_data_dict[values['name']][0],
                                                 test_labels=test_data_dict[values['name']][1])
    response = {
        "Test_accuracy": test_acc,
        "Test_loss": test_loss
    }
    return json.dumps(response)


def get_network_history(values: json):
    name = values['name']
    history_json = keras_wrapper.models[name].history_json
    response = {"Name": name, "History": history_json}
    return json.dumps(response)


services["health_check"] = health_check_service
services["new_network"] = new_network_service
services["compile_network"] = compile_network
services["get_networks"] = get_networks
services["get_network_details"] = get_network_details
services["train_network"] = train_network
services["delete_network"] = delete_network
services["evaluate_network"] = evaluate_network
services["get_network_history"] = get_network_history


def get_services():
    return services.copy()
