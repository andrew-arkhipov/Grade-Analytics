from time import sleep
from typing import List, Callable
from functools import wraps
from .course import Course
import shutil
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def login(driver: 'Driver', url: str):

    # get login page
    driver.get(url)

    # wait for manual login
    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Discovery Precalculus - UT COLLEGE')]")))


def parse_page(driver: 'Driver', url: str) -> List[str]:
    # get page
    driver.get(url)

    # wait for page to load
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Discovery Precalculus - UT COLLEGE')]")))

    # fetch all links
    links = []
    for link in driver.find_elements_by_xpath("//a[@href]"):
        links.append(link.get_attribute("href"))

    # filter links for valid course numbers
    courses = []
    for link in links:
        if Course.valid(link):
            courses.append(link)

    return courses


def download_manager(func: Callable) -> Callable:

    @wraps(func)
    def inner(*args, **kwargs) -> None:
        # preprocessing
        driver = args[0]
        size = len(os.listdir(driver.download_directory))

        # run scraper
        func(*args, **kwargs)

        # wait for download to start
        while len(os.listdir(driver.download_directory)) == size:
            sleep(0.05)

    return inner