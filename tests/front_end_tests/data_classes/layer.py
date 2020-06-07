from dataclasses import dataclass


# TODO generate it (?)

@dataclass
class DenseLayer:
    units: int
    activation: str
    input_shape: str
    type: str = "Dense"


@dataclass
class Conv2DLayer:
    filters: str
    kernel_size: str
    activation: str
    input_shape: str
    type: str = "Conv2D"


@dataclass
class MaxPooling2DLayer:
    pool_size: str
    strides: int
    type: str = "MaxPooling2D"


layers = {"Dense": DenseLayer,
          "Conv2D": Conv2DLayer,
          "MaxPooling2D": MaxPooling2DLayer}


def get_layer(layer_type: str):
    return layers[layer_type]


if __name__ == "__main__":
    import json

    test_json = "{'name': 'Test_network','layer': {'type': 'Dense', 'units': 16, 'activation': 'relu', 'input_shape': '1000'}}".replace("'",'"')
    values = json.loads(test_json)
    layer_type = values["layer"]["type"]
    test_layer = get_layer(layer_type)(**values["layer"])
    print(test_layer)
