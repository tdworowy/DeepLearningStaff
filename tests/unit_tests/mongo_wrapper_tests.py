import pytest
import yaml

from data_base.mongo_wrapper import MongoWrapper


def read_config():
    with open('../../config.yaml') as file:
        return yaml.safe_load(file)


config = read_config()


@pytest.fixture(autouse=True)
def mongo_wrapper():
    return MongoWrapper(
        url=config.get('mong_url'),
        data_base="Test_Base",
        collection="Test_Collection"
    )


def test_insert_data(mongo_wrapper):
    mongo_wrapper.insert({'data': 'test'})
    assert len(mongo_wrapper.get_all()) == 1
    assert mongo_wrapper.get_all()[0]['data'] == 'test'
    mongo_wrapper.drop_db()


def test_get_by_name(mongo_wrapper):
    mongo_wrapper.insert({'name': 'test', 'data': 'test_data'})
    assert len(mongo_wrapper.get_all()) == 1
    assert mongo_wrapper.get_by_name('test')['data'] == 'test_data'
    mongo_wrapper.drop_db()


def test_get_empty(mongo_wrapper):
    assert len(mongo_wrapper.get_all()) == 0
