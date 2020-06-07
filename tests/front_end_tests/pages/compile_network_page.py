from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from front_end_tests._tests_logging._logger import TestsLogger
from front_end_tests.webdriver_wapper.webdriver_wrapper import WebDriverWrapper
from selenium.common.exceptions import TimeoutException

class CompileNetworkPage:
    network_name = (By.NAME, "name")
    network_optimizer_select = (By.NAME, "optimizer")
    network_loss_select = (By.NAME, "loss")
    network_metrics_select = (By.NAME, "metrics")
    compile_network_button = (By.ID, "compile")

    def __init__(self, logger: TestsLogger, web_driver_wrapper: WebDriverWrapper):
        self.logger = logger
        self.web_driver_wrapper = web_driver_wrapper

    def set_optimizer(self, optimizer: str) -> CompileNetworkPage:
        self.logger.log().info(f"Set optimizer field: {optimizer}")
        Select(self.web_driver_wrapper.driver.find_element(*CompileNetworkPage.network_optimizer_select)) \
            .select_by_value(optimizer)
        return self

    def set_loss(self, loss: str) -> CompileNetworkPage:
        self.logger.log().info(f"Set loss field: {loss}")
        Select(self.web_driver_wrapper.driver.find_element(*CompileNetworkPage.network_loss_select)) \
            .select_by_value(loss)
        return self

    def set_metrics(self, metrics: str) -> CompileNetworkPage:
        self.logger.log().info(f"Set metrics field: {metrics}")
        Select(self.web_driver_wrapper.driver.find_element(*CompileNetworkPage.network_metrics_select)) \
            .select_by_value(metrics)
        return self

    def click_compile_network_button(self) -> CompileNetworkPage:
        self.logger.log().info(f"Click compile network button")
        self.web_driver_wrapper.driver.find_element(*CompileNetworkPage.compile_network_button) \
            .click()
        return self

    def check_if_network_is_compiled(self, names: list):
        for name in names:
            self.logger.log().info(f"Check if networks f{name} is compiled")
            label = self.web_driver_wrapper.driver.find_element(By.XPATH,
                                                                f'//*[@id="{name}"]/td/label[@id="compiled"]').text
            assert label == "true"

