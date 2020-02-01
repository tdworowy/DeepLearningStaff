import importlib


def get_keras_data_set(data_set: str):
    data_set = importlib.import_module(f"keras.datasets.{data_set}")
    return data_set.load_data()



