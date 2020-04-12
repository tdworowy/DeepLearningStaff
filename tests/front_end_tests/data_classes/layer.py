from dataclasses import dataclass


@dataclass
class Layer:
    type: str
    units: int
    activation: str
    input_shape: str