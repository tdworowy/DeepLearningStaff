from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


def chromedriver(executable_path: str) -> webdriver.Chrome:
    DesiredCapabilities.CHROME['goog:loggingPrefs'] = {'browser': 'ALL'}
    return webdriver.Chrome(executable_path=executable_path)


drivers = {}
drivers['chrome'] = chromedriver


def get_driver(browser: str):
    return drivers[browser]
