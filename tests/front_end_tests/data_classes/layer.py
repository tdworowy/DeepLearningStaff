from dataclasses import dataclass


@dataclass
class Layer:
    units: int
    activation: str
    input_shape: str