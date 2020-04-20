import json
import time
from os import path

import pytest
import requests
import yaml

current_dir = path.join(path.dirname(path.realpath(__file__)))
with open(path.join(current_dir, "../resources/new_network_json.json")) as json_file:
    new_network_json = json.load(json_file)

with open(path.join(current_dir, "../resources/compile_network_json.json")) as json_file:
    compile_network_json = json.load(json_file)

with open(path.join(current_dir, "../resources/train_network_json.json")) as json_file:
    train_network_json = json.load(json_file)


def read_config():
    current_dir = path.join(path.dirname(path.realpath(__file__)))
    with open(path.join(current_dir, '../../config.yaml')) as file:
        return yaml.safe_load(file)


config = read_config()
host = f"http://{config.get('test_host')}:{config.get('port')}"


@pytest.fixture(autouse=True)
def add_new_network():
    new_network_end_point = f"{host}/network/new"
    delete_network_end_point = f"{host}/network/delete"
    new_network_response = requests.post(url=new_network_end_point, json=new_network_json,
                                         headers={"content-type": "application/json"})
    yield new_network_response
    requests.delete(url=delete_network_end_point, json={'name': new_network_json['name']})
    time.sleep(15)


def test_add_network(add_new_network):
    assert add_new_network.status_code is 200
    assert add_new_network.json()['Message'] == f"New Network {new_network_json['name']} added."


def test_get_networks():
    get_networks_end_point = f"{host}/networks"
    get_networks_response = requests.get(url=get_networks_end_point, headers={"content-type": "application/json"})

    assert get_networks_response.status_code is 200
    assert new_network_json['name'] in get_networks_response.json()['Networks']


def test_compile_network():
    end_point = f"{host}/network/compile"
    compile_network_response = requests.post(url=end_point, json=compile_network_json,
                                             headers={"content-type": "application/json"})

    assert compile_network_response.status_code is 200
    assert compile_network_response.json()['Message'] == f"Network {new_network_json['name']} compiled."


def test_train_network():
    end_point_train = f"{host}/network/train"
    end_point_compile = f"{host}/network/compile"

    requests.post(url=end_point_compile, json=compile_network_json,
                  headers={"content-type": "application/json"})

    train_network_response = requests.post(url=end_point_train, json=train_network_json,
                                           headers={"content-type": "application/json"})

    assert train_network_response.status_code is 200
    assert train_network_response.json()["Message"] == f"Network {new_network_json['name']} training complete."


def test_evaluate_network():
    end_point_train = f"{host}/network/train"
    end_point_compile = f"{host}/network/compile"
    end_point_evaluate = f"{host}/network/evaluate"

    requests.post(url=end_point_compile, json=compile_network_json,
                  headers={"content-type": "application/json"})

    requests.post(url=end_point_train, json=train_network_json,
                  headers={"content-type": "application/json"})

    evaluate_network_response = requests.post(url=end_point_evaluate, json={"name": train_network_json["name"]},
                                              headers={"content-type": "application/json"})

    assert evaluate_network_response.status_code is 200
    assert evaluate_network_response.json()["Test_accuracy"] is not None
    assert evaluate_network_response.json()["Test_loss"] is not None


def test_get_network_training_history():
    end_point_train = f"{host}/network/train"
    end_point_compile = f"{host}/network/compile"
    end_point_get_history = f"{host}/network/history/{train_network_json['name']}"

    requests.post(url=end_point_compile, json=compile_network_json,
                  headers={"content-type": "application/json"})

    requests.post(url=end_point_train, json=train_network_json,
                  headers={"content-type": "application/json"})

    get_history_response = requests.get(url=end_point_get_history,
                                        headers={"content-type": "application/json"})

    assert get_history_response.status_code is 200
    assert get_history_response.json()["History"] is not {}, get_history_response


def test_get_network_details():
    get_network_details_end_point = f"{host}/network/{new_network_json['name']}"
    get_networks_response = requests.get(url=get_network_details_end_point,
                                         headers={"content-type": "application/json"})

    assert get_networks_response.status_code is 200
    assert get_networks_response.json()['Name'] == new_network_json['name']
    assert get_networks_response.json()['Compiled'] is False
    assert get_networks_response.json()['Trained'] is False


def test_health_check():
    health_check_end_point = f"{host}/healthCheck"
    get_networks_response = requests.get(url=health_check_end_point,
                                         headers={"content-type": "application/json"})

    assert get_networks_response.status_code is 200
    assert get_networks_response.json()["Message"] == {"health": "Live"}


def test_get_plots():
    end_point_train = f"{host}/network/train"
    end_point_compile = f"{host}/network/compile"
    end_point_loos_plt = f"{host}/network/plot/loss/{new_network_json['name']}"
    end_point_accuracy_plt = f"{host}/network/plot/accuracy/{new_network_json['name']}"

    requests.post(url=end_point_compile, json=compile_network_json,
                  headers={"content-type": "application/json"})

    requests.post(url=end_point_train, json=train_network_json,
                  headers={"content-type": "application/json"})

    loss_response = requests.get(url=end_point_loos_plt, json=train_network_json,
                                 headers={"content-type": "application/json"})

    acc_response = requests.get(url=end_point_accuracy_plt, json=train_network_json,
                                headers={"content-type": "application/json"})

    assert loss_response.status_code is 200
    assert acc_response.status_code is 200
