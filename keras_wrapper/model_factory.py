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
        self._layer = "Dense"
        self.kwargs = {}

    def units(self, units: int):
        self.kwargs['units'] = units
        return self

    def activation(self, activation: str):
        self.kwargs['activation'] = activation
        return self

    def input_shape(self, input_shape: str):
        input_shape = tuple(map(int, input_shape.split(',')))
        self.kwargs['input_shape'] = input_shape
        return self

    def build(self):
        return getattr(layers, self._layer)(**self.kwargs)


class Conv2DBuilder:
    def __init__(self):
        self._layer = "Conv2D"
        self.kwargs = {}

    def filters(self, filters: int):
        self.kwargs['filters'] = filters

    def kernel_size(self, kernel_size: str):
        kernel_size = tuple(map(int, kernel_size.split(',')))
        self.kwargs['kernel_size'] = kernel_size

    def activation(self, activation: str):
        self.kwargs['activation'] = activation
        return self

    def input_shape(self, input_shape: str):
        input_shape = tuple(map(int, input_shape.split(',')))
        self.kwargs['input_shape'] = input_shape
        return self

    def build(self):
        return getattr(layers, self._layer)(**self.kwargs)


class MaxPooling2DBuilder:
    def __init__(self):
        self._layer = "MaxPooling2D"
        self.kwargs = {}

    def pool_size(self, pool_size: str):
        pool_size = tuple(map(int, pool_size.split(',')))
        self.kwargs['pool_size'] = pool_size

    def strides(self, strides: int):
        self.kwargs['strides'] = strides

    def build(self):
        return getattr(layers, self._layer)(**self.kwargs)


layer_types = {'Dense': DenseLayerBuilder,
               'Conv2D': Conv2DBuilder,
               'MaxPooling2D': MaxPooling2DBuilder}


def build_layer(_layer: json):
    layer = layer_types[_layer['layer']]()
    for key in _layer.keys():
        if key != 'layer':
            getattr(layer, key)(_layer[key])
    return layer


def build_model(values: json) -> models.Sequential:
    model = ModelBuilder().model()
    for _layer in values['layers']:
        layer = build_layer(_layer)
        model = model.layer(layer.build())
    return model.build()
