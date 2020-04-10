import json

from keras import models, layers


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
        self._layer = "Dense"

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
            return getattr(layers, self._layer)(units=self._units,
                                                activation=self._activation,
                                                input_shape=self._input_shape)
        else:
            return getattr(layers, self._layer)(units=self._units,
                                                activation=self._activation)


def build_dense(_layer: json) -> DenseLayerBuilder:
    layer = DenseLayerBuilder(). \
        units(_layer['units']). \
        activation(_layer['activation'])

    if "input_shape" in _layer:
        if _layer["input_shape"] != "":
            layer = layer.input_shape(tuple(map(int, _layer['input_shape'].split(','))))
    return layer


def layer_factory(layer_type: str):
    if layer_type == "Dense":
        return build_dense


def build_model(values: json) -> models.Sequential:
    model = ModelBuilder().model()
    for _layer in values['layers']:
        layer = layer_factory(_layer['layer'])(_layer)

        model = model.layer(layer.build())
    return model.build()
