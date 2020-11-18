from time import sleep
from typing import List, Callable
from functools import wraps
from dataclasses import dataclass
from collections import defaultdict
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


@dataclass
class Student:
    first: str
    last: str
    multiplier: str


def parse_csv(filename: str) -> Dict[str, List['Student']]:
    # dictionary of students
    students = collections.defaultdict(list)

    with open(filename, "r") as f:
        # ignore first line
        _ = f.readline()

        # parse through students
        for line in f.readlines():
            line = line.split(',')

            # check if the student has time accommodations
            if not line[6].startswith("Extended time"):
                continue

            # extract information
            first = line[1]
            last = line[2]
            course = line[5]
            multiplier = ""

            i = line[6].find("(") + 1
            while line[6][i] != "x":
                multiplier += line[6][i]

            students.append(Student(first=first, last=last, multiplier=multiplier))

    return students