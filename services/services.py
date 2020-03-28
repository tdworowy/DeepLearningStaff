import json

import yaml
from keras.engine.saving import load_model

from _logging._logger import get_logger
from data.data_provider import get_keras_data_set
from data_base.mongo_wrapper import MongoWrapper
from wrapper.keras_wrapper import KerasWrapper, ModelBuilder, DenseLayerBuilder, ModelWrapper


def read_config():
    with open('../config.yaml') as file:
        return yaml.safe_load(file)


config = read_config()

logger = get_logger(__name__)
keras_wrapper = KerasWrapper()
mongo_wrapper = MongoWrapper(
    url=config.get('mong_url'),
    data_base=config.get('mongo_base'),
    collection=config.get('mongo_collection')
)
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
    response = keras_wrapper.get_models_names()
    response = {"Networks": response}
    return json.dumps(response)


def get_network_details(values: json):
    name = values["name"]
    model = keras_wrapper.get_model(name)
    compiled = model.compiled
    trained = model.trained
    model_json = model.model.to_json()
    response = {"Name": name, "Compiled": compiled, "Trained": trained, "Model": model_json}
    return json.dumps(response)


def delete_network(values: json):
    keras_wrapper.delete_network(values['name'])
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


def model_to_json(network_name: str):
    keras_wrapper.models[network_name].serialize_model(f'{network_name}.hdf5')
    return {
        "name": network_name,
        "compiled": keras_wrapper.models[network_name].compiled,
        "trained": keras_wrapper.models[network_name].trained,
        "model": open(f'{network_name}.hdf5').read(),
        "history": keras_wrapper.models[network_name].history_json,
        "time_stamp": keras_wrapper.models[network_name].update_time_stamp
    }


def json_to_model(data: json):
    return ModelWrapper(
        name=data["name"],
        compiled=data["compiled"],
        trained=data["trained"],
        model=load_model(data["model"]),
        history_json=data["history"],
        update_time_stamp=data["time_stamp"]

    )


def synchronize_data(*args):
    for network_name in keras_wrapper.get_models_names():
        if not mongo_wrapper.get_by_name(network_name):
            data = model_to_json(network_name)
            mongo_wrapper.insert(data)
        elif keras_wrapper.get_model(network_name).update_time_stamp > \
                mongo_wrapper.get_by_name(network_name)['time_stamp']:
            data = model_to_json(network_name)
            mongo_wrapper.replace(data)
    for network_name in keras_wrapper.get_deleted_models_names():
        mongo_wrapper.delete(network_name)

    for network in mongo_wrapper.get_all():
        model = json_to_model(network)
        keras_wrapper.add_model(network['name'], model)

    response = {"Message": "Data synchronized"}
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
services["synchronize_data"] = synchronize_data


def get_services():
    return services.copy()
