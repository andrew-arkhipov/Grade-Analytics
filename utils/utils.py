from time import sleep
from typing import List, Callable, Dict
from functools import wraps
from dataclasses import dataclass
from collections import defaultdict
from utils.courses.courses import HighSchoolCourse, CollegeCourse
from utils.courses.course_utils import Classes
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
    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'UT COLLEGE')]")))


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
    course_type = input("High school or college [HS/CO]: ").lower().strip()

    # error checking
    while course_type not in {'hs', 'co'}:
        print('Please enter a valid course type.')
        course_type = input("High school or college [HS/CO]: ").lower().strip()

    # get desired class type from stdin
    classname = input("Precalculus or College Algebra [PC/CA]: ").lower().strip()

    # error checking
    while course_type not in {'pc', 'ca'}:
        print('Please enter a valid class type.')
        course_type = input("Precalculus or College Algebra [PC/CA]: ").lower().strip()

    # assign class
    if classname == 'pc':
        class_type = Classes.PC
    else:
        class_type = Classes.CA

    # assign course
    if course_type == 'hs':
        course = HighSchoolCourse(class_type)
    else:
        course = CollegeCourse(class_type)
    
    return course


def get_unit_number() -> str:
    # get unit number for grading purposes from stdin
    unit = input("Enter the unit number: ").strip()

    # error checking
    while not unit.isdigit():
        print('Please enter a valid unit number.')
        unit = input("Enter the unit number: ").strip()

    return unit


def get_survey_inputs() -> Dict[str, str]:
    # get inputs from stdin
    inputs = {
        'url': input('Enter Qualtrics survey URL: '),
        'intro': input('Enter intro text: '),
        'finish': input('Enter finished text: ')
    }
    
    return inputs


@dataclass
class Assignment:
    name: str
    duration: int


def get_assignments() -> List['Assignment']:
    # prompt user
    print()
    print("Please enter the names and durations of the assignments you would like to add accommodations to exactly as they appear in Canvas.")
    print("Enter 'q' into the assignment name to indicate all assignments have been added.")
    print()

    # get first assignment
    name = input("Assignment name (e.g. Exam Unit 3: Part 2): ").strip()
    duration = int(input("Duration (e.g. 30): ").strip())
    print()
    res = [Assignment(name, duration)]

    # continue adding assignments as desired 
    while True:
        name = input("Assignment name: ").strip()
        if name == 'q':
            break
        duration = int(input("Duration: ").strip())
        print()
        res.append(Assignment(name, duration))

    return res


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