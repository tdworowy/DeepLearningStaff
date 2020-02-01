import logging

from keras import models, layers

logger = logging.getLogger('logger')


class ModelWrapper:
    def __init__(self, name: str, model: models, compiled: bool, trained: bool):
        self.trained = trained
        self.compiled = compiled
        self.model = model
        self.name = name
        self.history = None


class KerasWrapper:
    def __init__(self, _models=None):
        self.models = _models

    def add_model(self, name: str, model: models):
        self.models[name] = ModelWrapper(name, model, False, False)

    def compile(self, model_name: str, optimizer: str, loss: str, metrics: list):
        if self.models[model_name].compiled:
            logger.info(f"Model {model_name} already compiled")
        else:
            self.models[model_name].model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
            self.models[model_name].compiled = True

    def train(self, model_name: str, train_data, train_labels, val_data, val_labels, epochs: int, batch_size: int):
        history = self.models[model_name].model.fit(train_data, train_labels,
                                                    epochs=epochs, batch_size=batch_size,
                                                    validation_data=(val_data, val_labels))
        self.models[model_name].trained = True
        self.models[model_name].history = history


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
        return layers.Dense(units=self._units,
                            activation=self._activation,
                            input_shape=self._input_shape)
