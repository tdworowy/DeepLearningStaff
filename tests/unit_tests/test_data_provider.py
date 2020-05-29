import json

from data_provider.data_provider import data_sources


def test_get_data_sources():
    response = data_sources()
    assert response is not None


def test_get_data_sources_json_dump():
    response = data_sources()
    response = {"Data_Sources": response}
    response = json.dumps(response)
    assert response is not None
