from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from front_end_tests.webdriver_wapper.webdrover_factory import get_driver


class WebDriverWrapper:
    def __init__(self, browser: str, executable_path: str):
        self.driver = get_driver(browser)(executable_path)

    def open_page(self, server: str):
        self.driver.get(server)
        self.driver.implicitly_wait(5)

    def tear_down(self):
        self.driver.quit()

    def wait_for_element(self, locator, element: str):
        wait = WebDriverWait(self.driver, 45)
        wait.until(expected_conditions.visibility_of_element_located((locator, element)))
