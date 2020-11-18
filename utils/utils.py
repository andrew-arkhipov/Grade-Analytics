from time import sleep
from typing import List, Callable, Dict
from functools import wraps
from dataclasses import dataclass
from collections import defaultdict
from utils.courses.courses import HighSchoolCourse, CollegeCourse
import shutil
import pandas as pd
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

    # error checking
    while course_type not in {'hs', 'co'}:
        print('Please enter a valid course type.')
        course_type = input("High school or college [HS/CO]: ").lower()

    # assign course
    if course_type == 'hs':
        course = HighSchoolCourse()
    else:
        course = CollegeCourse()
    
    return course


def get_unit_number() -> str:
    # get unit number for grading purposes from stdin
    unit = input("Enter the unit number: ").strip()

    # error checking
    while not unit.isdigit():
        print('Please enter a valid unit number.')
        unit = input("Enter the unit number: ").strip()

    return unit


@dataclass
class Student:
    first: str
    last: str
    multiplier: str


def get_students(filename: str) -> Dict[str, List['Student']]:
    # dictionary of students
    students = defaultdict(list)

    with open(filename, "r") as f:
        # get dataframe
        df = pd.read_csv(filename)

        # parse through students
        for i, row in df.iterrows():
            if not row['Accommodation Request'].startswith("Extended time"):
                continue

            # parse through accommodation to get time multipler
            accom = row['Accommodation Request'].split(" ")
            multiplier = accom[5][1:-1]

            # create new instance of a student
            students[row['College Course']].append(Student(first=row['Student First Name'], last=row['Student Last Name'], multiplier=multiplier))

    return students