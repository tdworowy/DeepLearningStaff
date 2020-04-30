from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from front_end_tests._tests_logging._logger import TestsLogger
from front_end_tests.webdriver_wapper.webdriver_wrapper import WebDriverWrapper


class TrainingReportPage:

    def __init__(self, logger: TestsLogger, web_driver_wrapper: WebDriverWrapper):
        self.logger = logger
        self.web_driver_wrapper = web_driver_wrapper
    #TODO