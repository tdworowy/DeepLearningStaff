import pandas as pd
from keras import models, layers
from _logging._logger import get_logger

logger = get_logger(__name__)


class ModelWrapper:
    def __init__(self, name: str, model: models, compiled: bool, trained: bool):
        self.trained = trained
        self.compiled = compiled
        self.model = model
        self.name = name
        self.history_json = None


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class KerasWrapper(metaclass=Singleton):

    def __init__(self, _models: dict = None):
        if _models:
            self.models = _models
        else:
            self.models = dict()

    def add_model(self, name: str, model: models):
        logger.info(f"Add new Model {name}")
        self.models[name] = ModelWrapper(name, model, False, False)

    def compile(self, model_name: str, optimizer: str, loss: str, metrics: list):
        logger.info(f"Compiled model {model_name}")
        self.models[model_name].model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        self.models[model_name].compiled = True

    def train(self, model_name: str, train_data, train_labels, val_data, val_labels, epochs: int, batch_size: int):
        logger.info(f"Train model {model_name}")
        history = self.models[model_name].model.fit(train_data, train_labels,
                                                    epochs=epochs, batch_size=batch_size,
                                                    validation_data=(val_data, val_labels))
        self.models[model_name].trained = True
        self.models[model_name].history_json = pd.DataFrame.from_dict(history.history).to_json()

    def evaluate(self, model_name: str, test_data, test_labels):
        logger.info(f"Evaluate model {model_name}")
        return self.models[model_name].model.evaluate(test_data, test_labels)


class ModelBuilder:
    def model(self):
        self._model = models.Sequential()
        return self

    def layer(self, layer: layers):
        self._model.add(layer)
        return self

    def build(self):
        return self._model


class DenseLayerBuilder:

    def __init__(self):
        self._input_shape = None

    def units(self, units: int):
        self._units = units
        return self

    def activation(self, activation: str):
        self._activation = activation
        return self

    def input_shape(self, input_shape: tuple):
        self._input_shape = input_shape
        return self

    def build(self):
        if self._input_shape:
            return layers.Dense(units=self._units,
                                activation=self._activation,
                                input_shape=self._input_shape)
        else:
            return layers.Dense(units=self._units,
                                activation=self._activation)
