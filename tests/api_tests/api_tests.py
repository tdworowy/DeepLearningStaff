import json

import pytest
import requests

with open("../resources/new_network_json.json") as json_file:
    new_network_json = json.load(json_file)

with open("../resources/compile_network_json.json") as json_file:
    compile_network_json = json.load(json_file)

with open("../resources/train_network_json.json") as json_file:
    train_network_json = json.load(json_file)


@pytest.fixture(autouse=True, scope="module")
def add_new_network():
    end_point = "http://localhost:5000/network/new"
    new_network_response = requests.post(url=end_point, data=new_network_json,
                                         headers={"content-type": "application/json",
                                                  "Host": "localhost:5000"})
    return new_network_response


@pytest.fixture(autouse=True, scope="module")
def compile_network():
    end_point = "http://localhost:5000/network/compile"
    compile_network_response = requests.post(url=end_point, data=compile_network_json,
                                             headers={"content-type": "application/json",
                                                      "Host": "localhost:5000"})
    return compile_network_response


def test_add_network(add_new_network):
    assert 200 in add_new_network
    assert f'"Message": f"New Network {new_network_json["name"]} added."' in add_new_network


def test_compile_network(compile_network):
    assert 200 in compile_network
    assert f'"Message": "Network {new_network_json["name"]} compiled."' in compile_network


def test_train_network():
    end_point = "http://localhost:5000/network/train"
    train_network_response = requests.post(url=end_point, data=train_network_json,
                                           headers={"content-type": "application/json",
                                                    "Host": "localhost:5000"})
    assert 200 in train_network_response
    assert f'"Message": f"Network {new_network_json["name"]} training complete."' in train_network_response
