from time import sleep
from typing import List, Callable
from functools import wraps
from dataclasses import dataclass
from utils.courses.courses import HighSchoolCourse, CollegeCourse
import shutil
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def login(driver: 'Driver', url: str):
    # get login page
    driver.get(url)

    # wait for manual login
    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Discovery Precalculus')]")))


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


def get_course_type() -> str:
    # get desired course type from stdin
    course_type = input("High school or college [HS/CO]: ").lower()
    while course_type not in {'hs', 'co'}:
        print('Please enter a valid course type.')
        course_type = input("High school or college [HS/CO]: ").lower()

    # assign course
    if course_type == 'hs':
        course = HighSchoolCourse()
    else:
        course = CollegeCourse()
    
    return course


def parse_csv(filename: str) -> None:
    pass
