from time import sleep
from typing import List, Callable
from functools import wraps
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


def parse_page(driver: 'Driver', url: str, course: 'Course') -> List[str]:
    # get page
    driver.get(url)

    # wait for page to load
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Discovery Precalculus - UT COLLEGE')]")))

    # fetch all potential courses
    elements = [elem for elem in driver.find_elements_by_xpath("//a")]

    # filter links for valid course numbers
    courses = []
    for elem in elements:
        if course.valid(elem):
            courses.append(elem.get_attribute('href'))

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