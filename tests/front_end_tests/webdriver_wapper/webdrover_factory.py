import os

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import platform
from typing import Callable

systems = {"Windows": "_win.exe", "Linux": "_lin"}


def chromedriver(executable_path: str) -> webdriver.Chrome:
    system = platform.system()
    executable_path = executable_path + systems[system]
    assert os.path.isfile(executable_path), f"File {executable_path} don't exist"

    DesiredCapabilities.CHROME['goog:loggingPrefs'] = {'browser': 'ALL'}
    return webdriver.Chrome(executable_path=executable_path)


drivers = {}
drivers['chrome'] = chromedriver


def get_driver(browser: str) -> Callable:
    return drivers[browser]
