from __future__ import annotations

import json

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from front_end_tests._tests_logging._logger import TestsLogger
from front_end_tests.webdriver_wapper.webdriver_wrapper import WebDriverWrapper

from front_end_tests.pages.add_layer_page_factory import AddLayerPageFactory


class AddNetworkPage:
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
        self.add_layer_page_factory = AddLayerPageFactory(logger=self.logger,
                                                          web_driver_wrapper=self.web_driver_wrapper)

    def open_page(self):
        self.logger.log().info(f"Open page {self.url}")
        self.web_driver_wrapper.open_page(self.url)

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
        self.web_driver_wrapper.driver.find_element(*AddNetworkPage.choose_layer_button) \
            .click()
        return self.add_layer_page_factory.get_add_layer_page(layer_type)

    def generate_output_json(self, name: str, layers: list) -> dict:

        return {"name": name, "layers": [

            self.add_layer_page_factory. \
                get_add_layer_page(layer.type).generate_output_json(layer)

            for layer in layers
        ]}

    def assert_layer(self, expected_name: str, expected_layers: list):
        self.logger.log().info(f"Assert network data")

        actual_value = self.web_driver_wrapper.driver.find_element(*AddNetworkPage.layers_details).text
        actual_value = json.loads(actual_value)

        expected_value = self.generate_output_json(expected_name, expected_layers)

        self.logger.log().info(f"actual: {actual_value} expected: {expected_value}")
        assert actual_value == expected_value, f"{actual_value} is not equal to {expected_value}"

    def check_networks_lists(self, names: str):
        self.logger.log().info(f"Check if networks f{names} exists")
        for name in names:
            try:
                self.web_driver_wrapper.wait_for_element(By.XPATH, f'//*[@id="{name}"]/td/label')
            except TimeoutException:
                self.logger.log().info(f"Network {name} not found")
                raise AssertionError(f"Network {name} not found")

    def delete_network(self, name: str):
        self.logger.log().info(f"Delete network {name}")
        delete_button = (By.XPATH, f'//*[@id="{name}"]/td/button[@id="delete"]')
        self.web_driver_wrapper.wait_for_element(*delete_button)
        self.web_driver_wrapper.driver.find_element(*delete_button).click()
