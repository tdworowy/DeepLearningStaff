from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from .webdrover_factory import get_driver


class WebDriverWrapper:
    def __init__(self, browser: str):
        self.driver = get_driver(browser)

    def open_page(self, server: str):
        self.driver.get(server)
        self.driver.implicitly_wait(5)

    def tear_down(self):
        self.driver.quit()

    def wait_for_element(self, locator: By, element: str):
        wait = WebDriverWait(self.driver, 45)
        wait.until(expected_conditions.visibility_of_element_located((locator, element)))

    def find_element(self, locator: By, element: str) -> WebElement:
        self.wait_for_element(locator, element)
        return self.driver.find_element(locator, element)
