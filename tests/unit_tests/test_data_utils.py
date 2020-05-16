from data_utils.data_utils import vectorized_sequences
import numpy as np


def test_add_model_vectorized_sequences():
    expected = np.array([[0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
    result = vectorized_sequences([1, 2, 3], 4)
    assert np.array_equal(result, expected)

def test_get_data_sources():
    response = data_sources()