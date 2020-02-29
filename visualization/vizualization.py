import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def plot(epochs: range, train_values: list, validation_values: list, metric: str) -> Figure:
    fig, _plt = plt.subplots()
    _plt.plot(epochs, train_values, 'bo', label=f"Training {metric}")
    _plt.plot(epochs, validation_values, 'b', label=f"Validation {metric}")
    _plt.set_title(f"Training and validation {metric}")
    _plt.set_xlabel('Epochs')
    _plt.set_ylabel(metric)
    _plt.legend()
    return fig
