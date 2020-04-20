import sys

if sys.version_info[1] == 7:
    from __future__ import annotations


import json

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from front_end_tests._tests_logging._logger import TestsLogger
from front_end_tests.webdriver_wapper.webdriver_wrapper import WebDriverWrapper


class AddNetworkPage:
    network_name_input = (By.NAME, "name")
    network_units_input = (By.NAME, "units")
    network_activation_select = (By.NAME, "activation")
    network_input_shape_input = (By.NAME, "input_shape")
    add_layer_button = (By.ID, "add_layer")
    add_network_button = (By.ID, "add_network_button")
    clear_network_button = (By.ID, "clear_network_button")
    layers_details = (By.ID, "new_layer_details")
    choose_layer_button = (By.ID, "choose_layer")
    layer_select = (By.NAME, "layer")

    def __init__(self, url: str, logger: TestsLogger, web_driver_wrapper: WebDriverWrapper):
        self.logger = logger
        self.url = url
        self.web_driver_wrapper = web_driver_wrapper

    def open_page(self):
        self.logger.log().info(f"Open page {self.url}")
        self.web_driver_wrapper.open_page(self.url)

    def set_name(self, network_name: str) -> AddNetworkPage:
        self.logger.log().info(f"Set network name field: {network_name}")
        name_input = self.web_driver_wrapper.driver.find_element(*AddNetworkPage.network_name_input)
        name_input.clear()
        name_input.send_keys(network_name)
        return self

    def set_units(self, units: str) -> AddNetworkPage:
        self.logger.log().info(f"Set units field: {units}")
        self.web_driver_wrapper.driver.find_element(*AddNetworkPage.network_units_input) \
            .send_keys(units)
        return self

    def set_activation(self, activation: str) -> AddNetworkPage:
        self.logger.log().info(f"Set activation field: {activation}")
        Select(self.web_driver_wrapper.driver.find_element(*AddNetworkPage.network_activation_select)) \
            .select_by_value(activation)
        return self

    def set_input_shape(self, input_shape: str) -> AddNetworkPage:
        self.logger.log().info(f"Set input_shape field: {input_shape}")
        self.web_driver_wrapper.driver.find_element(*AddNetworkPage.network_input_shape_input) \
            .send_keys(input_shape)
        return self

    def click_add_layer_button(self) -> AddNetworkPage:
        self.logger.log().info(f"Click add layer button")
        self.web_driver_wrapper.driver.find_element(*AddNetworkPage.add_layer_button) \
            .click()
        return self

    def click_add_network_button(self) -> AddNetworkPage:
        self.logger.log().info(f"Click add network button")
        self.web_driver_wrapper.driver.find_element(*AddNetworkPage.add_network_button) \
            .click()
        return self

    def clear_layers(self):
        self.logger.log().info(f"Clear layers")
        self.web_driver_wrapper.driver.find_element(*AddNetworkPage.clear_network_button) \
            .click()
        return self

    def choose_layer_type(self, layer_type: str):
        self.logger.log().info(f"Choose layer type: {layer_type}")
        Select(self.web_driver_wrapper.driver.find_element(*AddNetworkPage.layer_select)) \
            .select_by_value(layer_type)
        self.web_driver_wrapper.driver.find_element(*AddNetworkPage.choose_layer_button)\
            .click()
        return self

    def assert_layer(self, expected_name: str, expected_layers: list):
        self.logger.log().info(f"Assert network data")

        actual_value = self.web_driver_wrapper.driver.find_element(*AddNetworkPage.layers_details).text
        actual_value = json.loads(actual_value)

        expected_value = self._generate_output_json(expected_name, expected_layers)

        self.logger.log().info(f"actual: {actual_value} expected: {expected_value}")
        assert actual_value == expected_value, f"{actual_value} is not equal to {expected_value}"

    def check_networks_lists(self, names: str):
        self.logger.log().info(f"Check if networks f{names} exists")
        for name in names:
            try:
                self.web_driver_wrapper.wait_for_element(By.XPATH, f'//*[@id="{name}"]/label')
            except TimeoutException:
                self.logger.log().info(f"Network {name} not found")
                raise AssertionError(f"Network {name} not found")

    def delete_network(self, name: str):
        self.logger.log().info(f"Delete network {name}")
        delete_button = (By.XPATH, f'//*[@id="{name}"]/button[@id="delete"]')
        self.web_driver_wrapper.wait_for_element(*delete_button)
        self.web_driver_wrapper.driver.find_element(*delete_button).click()

    @staticmethod
    def _generate_output_json(name: str, layers: list) -> dict:
        return {"name": name, "layers": [
            {
                "layer": layer.type,
                "units": layer.units,
                "activation": layer.activation,
                "input_shape": layer.input_shape,
            }
            for layer in layers
        ]}
