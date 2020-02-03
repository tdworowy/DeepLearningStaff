import importlib

import numpy as np
from keras.datasets import imdb

from data_utils.data_utils import vectorized_sequences


def get_keras_data_set(data_set_name: str, sample: int):
    return data_set[data_set_name](sample)


def get_imdb_data_set(num_words: int):
    from keras.datasets import imdb
    (train_data, train_labels), (val_data, val_labels) = imdb.load_data(num_words=num_words)
    train_data = vectorized_sequences(train_data, dimension=num_words)
    val_data = vectorized_sequences(val_data, dimension=num_words)
    train_labels = np.asarray(train_labels)
    val_labels = np.asarray(val_labels)
    return (train_data, train_labels), (val_data, val_labels)


data_set = {'imdb': get_imdb_data_set}
