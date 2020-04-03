import os

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


class WebDriverWrapper:
    def __init__(self, executable_path: str):
        assert os.path.isfile(executable_path), f"File {executable_path} don't exist"
        #self.driver = webdriver.Firefox(executable_path=executable_path)
        self.driver = webdriver.Chrome(executable_path=executable_path)

    def open_page(self, server: str):
        self.driver.get(server)
        self.driver.implicitly_wait(5)

    def tear_down(self):
        self.driver.quit()

    def wait_for_element(self, locator, element: str):
        wait = WebDriverWait(self.driver, 10)
        wait.until(expected_conditions.visibility_of_element_located((locator, element)))
