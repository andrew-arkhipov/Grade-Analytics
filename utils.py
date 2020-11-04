from time import sleep
from functools import wraps
import shutil
import os

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


class Driver(webdriver.Chrome):
    @classmethod
    def initialize(cls, target_dir="") -> 'Driver':
        options = Options()
        if target_dir:
            prefs = {
                "download.default_directory": target_dir
            }
            options.add_experimental_option('prefs', prefs)
        setattr(cls, 'download_directory', target_dir)
        return cls(ChromeDriverManager().install(), options=options)


def download_manager(func):

    @wraps(func)
    def inner(*args, **kwargs):
        # preprocessing
        driver = args[0]
        size = len(os.listdir(driver.download_directory))

        # run scraper
        func(*args, **kwargs)

        # wait for download to start
        while len(os.listdir(driver.download_directory)) == size:
            sleep(0.05)

    return inner


def login(driver, url):

    # get login page
    driver.get(url)

    # wait for manual login
    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Discovery Precalculus - UT COLLEGE')]")))