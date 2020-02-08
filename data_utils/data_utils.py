import numpy as np


def vectorized_sequences(sequence, dimension=20000):
    results = np.zeros((len(sequence), dimension))
    for i, sequence in enumerate(sequence):
        results[i, sequence] = 1
    return results
