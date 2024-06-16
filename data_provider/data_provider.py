from os import path

import numpy as np
import requests
import yaml

from data_utils.data_utils import vectorized_sequences
from keras.utils import to_categorical
from functools import partial


def read_config():
    current_dir = path.join(path.dirname(path.realpath(__file__)))
    with open(path.join(current_dir, "../config.yaml")) as file:
        return yaml.safe_load(file)


def get_keras_data_set(data_set_name: str, sample: int, test_set_size: int):
    return data_sets[data_set_name](sample, test_set_size)


def get_imdb_data_set(size: int, test_set_size: int):
    from keras.datasets import imdb

    (train_data, train_labels), (val_data, val_labels) = imdb.load_data(num_words=size)

    train_data = vectorized_sequences(train_data, dimension=size)
    val_data = vectorized_sequences(val_data, dimension=size)

    train_labels = np.asarray(train_labels)
    val_labels = np.asarray(val_labels)

    test_data = train_data[:test_set_size]
    train_data = train_data[test_set_size:]

    test_labels = train_labels[:test_set_size]
    train_labels = train_labels[test_set_size:]

    return (train_data, train_labels), (val_data, val_labels), (test_data, test_labels)


def get_minst_data_set(size: int, test_set_size: int):
    from keras.datasets import mnist

    (train_images, train_labels), (val_images, val_labels) = mnist.load_data()

    train_images = train_images.reshape((size, 28, 28, 1))
    train_images = train_images.astype("float32") / 255

    val_images = val_images.reshape((test_set_size, 28, 28, 1))
    val_images = val_images.astype("float32") / 255

    train_labels = to_categorical(train_labels)
    val_labels = to_categorical(val_labels)

    test_images = train_images[:test_set_size]
    test_labels = train_labels[:test_set_size]

    return (
        (train_images, train_labels),
        (val_images, val_labels),
        (test_images, test_labels),
    )


data_sets = {"imdb": get_imdb_data_set, "minst": get_minst_data_set}


def data_sources():
    return list(data_sets.keys())


def add_data_set_from_file(file_name: str):
    function = partial(get_file_data_set, file_name)
    data_sets[file_name] = function


def get_file_data_set(file_name: str, size: int, test_set_size: int):
    """File should be pickle"""
    assert ".pickle" in file_name
    if not path.exists(file_name):
        config = read_config()
        url = f"http://{config.get('api_host')}:{config.get('port')}/download-data-sources-file/{file_name}"
        response = requests.get(url, allow_redirects=True)
        with open(file_name, "wb") as dat_set_file:
            dat_set_file.write(response.content)

    with np.load(file_name, allow_pickle=True) as f:
        x_train, labels_train = f["x_train"], f["y_train"]
        x_val, val_labels = f["x_test"], f["y_test"]

    x_train = x_train[:size]
    labels_train = labels_train[:size]

    x_test = x_train[:test_set_size]
    labels_test = labels_train[:test_set_size]

    return (x_train, labels_train), (x_val, val_labels), (x_test, labels_test)
