import numpy as np
from data_utils.data_utils import vectorized_sequences


def get_keras_data_set(data_set_name: str, sample: int, test_set_size: int):
    return data_sets[data_set_name](sample, test_set_size)


def get_imdb_data_set(num_words: int, test_set_size: int):
    from keras.datasets import imdb
    (train_data, train_labels), (val_data, val_labels) = imdb.load_data(num_words=num_words)

    train_data = vectorized_sequences(train_data, dimension=num_words)
    val_data = vectorized_sequences(val_data, dimension=num_words)

    train_labels = np.asarray(train_labels)
    val_labels = np.asarray(val_labels)

    test_data = train_data[:test_set_size]
    train_data = train_data[test_set_size:]

    test_labels = train_labels[:test_set_size]
    train_labels = train_labels[test_set_size:]

    return (train_data, train_labels), \
           (val_data, val_labels), \
           (test_data, test_labels)


data_sets = {'imdb': get_imdb_data_set}


def get_data_sources():
    return data_sets.keys()
