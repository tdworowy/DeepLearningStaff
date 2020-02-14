import json
import pytest
import requests
import yaml

with open("../resources/new_network_json.json") as json_file:
    new_network_json = json.load(json_file)

with open("../resources/compile_network_json.json") as json_file:
    compile_network_json = json.load(json_file)

with open("../resources/train_network_json.json") as json_file:
    train_network_json = json.load(json_file)


def read_config():
    with open('../../config.yaml') as file:
        return yaml.safe_load(file)


config = read_config()
host = f"http://{config.get('host')}:{config.get('port')}"


@pytest.fixture(autouse=True)
def add_new_network():
    new_network_end_point = f"{host}/network/new"
    delete_network_end_point = f"{host}/network/delete"
    new_network_response = requests.post(url=new_network_end_point, json=new_network_json,
                                         headers={"content-type": "application/json"})
    yield new_network_response
    requests.delete(url=delete_network_end_point, json={'name': new_network_json['name']})


def test_add_network(add_new_network):
    assert add_new_network.status_code is 200
    assert add_new_network.json()['Message'] == f"New Network {new_network_json['name']} added."


def test_get_networks():
    get_networks_end_point = f"{host}/networks"
    get_networks_response = requests.get(url=get_networks_end_point, headers={"content-type": "application/json"})

    assert get_networks_response.status_code is 200
    assert get_networks_response.json()['Networks'] == [new_network_json['name']]


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
