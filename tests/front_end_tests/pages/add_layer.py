from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


from ..webdriver_wapper.webdriver_wrapper import WebDriverWrapper

from ..logging.logger_ import TestsLogger


class AddDense:
    network_name_input = (By.NAME, "name")
    network_units_input = (By.NAME, "units")
    network_activation_select = (By.NAME, "activation")
    network_input_shape_input = (By.NAME, "input_shape")

    def __init__(self, logger: TestsLogger, web_driver_wrapper: WebDriverWrapper):
        self.logger = logger
        self.web_driver_wrapper = web_driver_wrapper

    def set_name(self, network_name: str) -> AddDense:
        self.logger.log().info(f"Set network name field: {network_name}")
        name_input = self.web_driver_wrapper.find_element(*AddDense.network_name_input)
        name_input.clear()
        name_input.send_keys(network_name)
        return self

    def set_units(self, units: str) -> AddDense:
        self.logger.log().info(f"Set units field: {units}")
        self.web_driver_wrapper.find_element(*AddDense.network_units_input).send_keys(
            units
        )
        return self

    def set_activation(self, activation: str) -> AddDense:
        self.logger.log().info(f"Set activation field: {activation}")
        Select(
            self.web_driver_wrapper.find_element(*AddDense.network_activation_select)
        ).select_by_value(activation)
        return self

    def set_input_shape(self, input_shape: str) -> AddDense:
        self.logger.log().info(f"Set input_shape field: {input_shape}")
        self.web_driver_wrapper.find_element(
            *AddDense.network_input_shape_input
        ).send_keys(input_shape)
        return self

    @staticmethod
    def generate_output_json(layer) -> dict:
        return {
            "units": layer.units,
            "activation": layer.activation,
            "input_shape": layer.input_shape,
            "layer": layer.type,
        }


class AddConv2D:
    network_name_input = (By.NAME, "name")
    network_filter_input = (By.NAME, "filters")
    network_kernel_size_input = (By.NAME, "kernel_size")
    network_activation_select = (By.NAME, "activation")
    network_input_shape_input = (By.NAME, "input_shape")

    def __init__(self, logger: TestsLogger, web_driver_wrapper: WebDriverWrapper):
        self.logger = logger
        self.web_driver_wrapper = web_driver_wrapper

    def set_name(self, network_name: str) -> AddConv2D:
        self.logger.log().info(f"Set network name field: {network_name}")
        name_input = self.web_driver_wrapper.find_element(*AddConv2D.network_name_input)
        name_input.clear()
        name_input.send_keys(network_name)
        return self

    def set_activation(self, activation: str) -> AddConv2D:
        self.logger.log().info(f"Set activation field: {activation}")
        Select(
            self.web_driver_wrapper.find_element(*AddConv2D.network_activation_select)
        ).select_by_value(activation)
        return self

    def set_input_shape(self, input_shape: str) -> AddConv2D:
        self.logger.log().info(f"Set input_shape field: {input_shape}")
        self.web_driver_wrapper.find_element(
            *AddConv2D.network_input_shape_input
        ).send_keys(input_shape)
        return self

    def set_filters(self, filters: str) -> AddConv2D:
        self.logger.log().info(f"Set filters field: {filters}")
        self.web_driver_wrapper.find_element(*AddConv2D.network_filter_input).send_keys(
            filters
        )
        return self

    def set_kernel_size(self, kernel_size: str) -> AddConv2D:
        self.logger.log().info(f"Set kernel_size field: {kernel_size}")
        self.web_driver_wrapper.find_element(
            *AddConv2D.network_kernel_size_input
        ).send_keys(kernel_size)
        return self

    @staticmethod
    def generate_output_json(layer) -> dict:
        return {
            "filters": layer.filters,
            "kernel_size": layer.filters,
            "activation": layer.activation,
            "input_shape": layer.input_shape,
            "layer": layer.type,
        }


class AddMaxPooling2D:
    network_name_input = (By.NAME, "name")
    network_pool_size_input = (By.NAME, "pool_size")
    network_strides_input = (By.NAME, "strides")

    def __init__(self, logger: TestsLogger, web_driver_wrapper: WebDriverWrapper):
        self.logger = logger
        self.web_driver_wrapper = web_driver_wrapper

    def set_name(self, network_name: str) -> AddMaxPooling2D:
        self.logger.log().info(f"Set network name field: {network_name}")
        name_input = self.web_driver_wrapper.find_element(
            *AddMaxPooling2D.network_name_input
        )
        name_input.clear()
        name_input.send_keys(network_name)
        return self

    def set_pool_size(self, pool_size: str) -> AddMaxPooling2D:
        self.logger.log().info(f"Set pool_size field: {pool_size}")
        self.web_driver_wrapper.find_element(
            *AddMaxPooling2D.network_pool_size_input
        ).send_keys(pool_size)
        return self

    def set_strides(self, strides: str) -> AddMaxPooling2D:
        self.logger.log().info(f"Set strides field: {strides}")
        self.web_driver_wrapper.find_element(
            *AddMaxPooling2D.network_strides_input
        ).send_keys(strides)
        return self

    @staticmethod
    def generate_output_json(layer) -> dict:
        return {
            "pool_size": layer.pool_size,
            "strides": layer.strides,
            "layer": layer.type,
        }
