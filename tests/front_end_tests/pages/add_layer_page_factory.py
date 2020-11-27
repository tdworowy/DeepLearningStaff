from .add_layer import AddDense, AddConv2D, AddMaxPooling2D

from ..logging.logger_ import TestsLogger
from ..webdriver_wapper.webdriver_wrapper import WebDriverWrapper


class AddLayerPageFactory:
    add_layer_pages = {
        "Dense": AddDense,
        "Conv2D": AddConv2D,
        "MaxPooling2D": AddMaxPooling2D
    }

    def __init__(self, logger: TestsLogger, web_driver_wrapper: WebDriverWrapper):
        self.logger = logger
        self.web_driver_wrapper = web_driver_wrapper
        self.add_layer_pages_objects = {}

    def get_add_layer_page(self, layer_type: str):
        if layer_type in self.add_layer_pages_objects.keys():
            return self.add_layer_pages_objects[layer_type]
        else:
            layer_page = AddLayerPageFactory.add_layer_pages[layer_type](self.logger, self.web_driver_wrapper)
            self.add_layer_pages_objects[layer_type] = layer_page
        return layer_page
