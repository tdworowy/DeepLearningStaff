import os

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import platform

from selenium.webdriver.chrome.options import Options

systems = {"Windows": "win.exe", "Linux": "lin"}


def chromedriver() -> webdriver.Chrome:
    system = platform.system()
    current_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    executable_path = os.path.join(current_dir, f"../../chromedriver/chromedriver_{systems[system]}")

    assert os.path.isfile(executable_path), f"File {executable_path} don't exist"

    DesiredCapabilities.CHROME['goog:loggingPrefs'] = {'browser': 'ALL'}

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    return webdriver.Chrome(executable_path=executable_path, options=chrome_options)


drivers = {'chrome': chromedriver}


def get_driver(browser: str) -> webdriver:
    return drivers[browser]()
