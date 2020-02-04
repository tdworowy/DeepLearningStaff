import json
import pytest
import requests

with open("../resources/new_network_json.json") as json_file:
    new_network_json = json.load(json_file)

with open("../resources/compile_network_json.json") as json_file:
    compile_network_json = json.load(json_file)

with open("../resources/train_network_json.json") as json_file:
    train_network_json = json.load(json_file)

host = "http://localhost:5000"


@pytest.fixture(autouse=True, scope="module")
def add_new_network():
    end_point = f"{host}/network/new"
    new_network_response = requests.post(url=end_point, json=new_network_json,
                                         headers={"content-type": "application/json"})
    return new_network_response


@pytest.fixture(autouse=True, scope="module")
def compile_network():
    end_point = f"{host}/network/compile"
    compile_network_response = requests.post(url=end_point, json=compile_network_json,
                                             headers={"content-type": "application/json"})
    return compile_network_response


def test_add_network(add_new_network):
    assert add_new_network.status_code is 200
    assert add_new_network.json()['Message'] == f"New Network {new_network_json['name']} added."


def test_compile_network(compile_network):
    assert compile_network.status_code is 200
    assert compile_network.json()['Message'] == f"Network {new_network_json['name']} compiled."


def test_train_network():
    end_point = f"{host}/network/train"
    train_network_response = requests.post(url=end_point, json=train_network_json,
                                           headers={"content-type": "application/json"})
    assert train_network_response.status_code is 200
    assert train_network_response.json()["Message"] == f"Network {new_network_json['name']} training complete."
