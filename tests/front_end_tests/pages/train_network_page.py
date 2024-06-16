from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from ..logging.logger_ import TestsLogger
from ..webdriver_wapper.webdriver_wrapper import WebDriverWrapper


class TrainNetworkPage:
    network_name_input = (By.NAME, "name")
    epochs_input = (By.NAME, "epochs")
    dat_set_select = (By.NAME, "data_set")
    batch_size_input = (By.NAME, "batch_size")
    input_shape_input = (By.NAME, "input_shape")
    test_sample_size_input = (By.NAME, "test_sample_size")
    train_network_button = (By.ID, "train")

    def __init__(self, logger: TestsLogger, web_driver_wrapper: WebDriverWrapper):
        self.logger = logger
        self.web_driver_wrapper = web_driver_wrapper

    def set_epochs(self, epochs: str) -> TrainNetworkPage:
        self.logger.log().info(f"Set epochs field: {epochs}")
        self.web_driver_wrapper.find_element(*TrainNetworkPage.epochs_input).send_keys(
            epochs
        )
        return self

    def set_batch_size(self, batch_size: str) -> TrainNetworkPage:
        self.logger.log().info(f"Set batch_size field: {batch_size}")
        self.web_driver_wrapper.find_element(
            *TrainNetworkPage.batch_size_input
        ).send_keys(batch_size)
        return self

    def set_input_shape(self, input_shape: str) -> TrainNetworkPage:
        self.logger.log().info(f"Set input_shape field: {input_shape}")
        self.web_driver_wrapper.find_element(
            *TrainNetworkPage.input_shape_input
        ).send_keys(input_shape)
        return self

    def set_test_sample_size(self, test_sample_size: str) -> TrainNetworkPage:
        self.logger.log().info(f"Set test_sample_size field: {test_sample_size}")
        self.web_driver_wrapper.find_element(
            *TrainNetworkPage.test_sample_size_input
        ).send_keys(test_sample_size)
        return self

    def set_data_set(self, dat_set: str) -> TrainNetworkPage:
        self.logger.log().info(f"Set dat_set field: {dat_set}")
        Select(
            self.web_driver_wrapper.find_element(*TrainNetworkPage.dat_set_select)
        ).select_by_value(dat_set)
        return self

    def click_train_network_button(self) -> TrainNetworkPage:
        self.logger.log().info(f"Click train network button")
        self.web_driver_wrapper.find_element(
            *TrainNetworkPage.train_network_button
        ).click()
        return self

    def check_if_network_is_trained(self, names: list):
        for name in names:
            self.logger.log().info(f"Check if networks f{name} is trained")
            label = self.web_driver_wrapper.find_element(
                By.XPATH, f'//*[@id="{name}"]/td/label[@id="trained"]'
            ).text
            assert label == "true"
