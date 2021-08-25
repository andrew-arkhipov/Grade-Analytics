import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from math import ceil
from typing import List, Tuple, Dict
from utils.driver import Driver
from utils.utils import get_course_type, get_assignments

import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@dataclass
class Student:
    firstName: str
    lastName: str
    multiplier: float


def login(driver, url):
    # get login page
    driver.get(url)

    # wait for manual login
    WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Dashboard')]")))


def get_students() -> Dict[str, List[Student]]:
    filename: str = input("\nEnter the filename of the accommodations csv: ")
    df: pd.DataFrame = pd.read_csv(f"{os.path.dirname(sys.executable)}/{filename}")
    # df: pd.DataFrame = pd.read_csv(filename)

    students_by_course: Dict[str, List[Student]] = defaultdict(list)
    for _, row in df.iterrows():
        if not row["Accommodation Request"].startswith("Extended time"):
            continue

        # parse through accommodation to get time multipler
        accom = row["Accommodation Request"].split(" ")
        multiplier = accom[5][1:-1]

        # create new instance of a student
        students_by_course[row["College Course.1"]].append(
            Student(
                firstName=row["Student First Name"],
                lastName=row["Student Last Name"],
                multiplier=multiplier
            )
        )
    return students_by_course


def add_extensions(driver: 'Driver', extra_time: int) -> None:
    # find menu and submit time
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='extension_extra_time']")))
    input_box = driver.find_element_by_xpath("//input[@id='extension_extra_time']")
    input_box.clear()
    input_box.send_keys(extra_time)

    # save
    driver.find_element_by_xpath("//button/span[contains(text(), 'Save')]/..").click()


def add_accommodations(driver: 'Driver', assignment_links: List['str'], assignments: List['Assignment'], students: List[Student]) -> None:
    # loop through all assignments
    for assignment, link in zip(assignments, assignment_links):
        # go to exam
        driver.get(f"{link}/moderate")

        # calculate extra time
        get_extra_time = lambda duration, multiplier: int(ceil(duration * multiplier - duration))

        # get utils
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='search_term']")))

        # loop through students
        for student in students:
            if str(student.firstName) == "nan" or str(student.lastName) == "nan":
                continue

            # get utils
            input_box = driver.find_element_by_xpath("//input[@id='search_term']")
            submit = driver.find_element_by_xpath("//input[@value='Filter']")

            # find student
            input_box.clear()
            input_box.send_keys(f"{student.firstName} {student.lastName}")
            submit.click()

            # click on extensions menu and add acommodations
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//i/span[contains(text(), 'Change user extensions')]/.."))).click()
            extra_time = get_extra_time(assignment.duration, eval(student.multiplier))
            add_extensions(driver, extra_time)

            # refresh
            driver.refresh()


def get_assignment_links(driver: 'Driver', url: str, assignments: List['Assignment']) -> List['str']:
    # get url
    driver.get(url)

    # wait for table with quizzes to load
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//h2[@aria-controls='assignment-quizzes']")))

    # get link for each assignment
    links = []
    for assignment in assignments:
        elem = driver.find_element_by_xpath(f"//a[contains(text(), '{assignment.name}')]")
        link = elem.get_attribute("href")
        links.append(link)

    return links


def run(driver: 'Driver', students: Dict[str, List[Student]], assignments: List['Assignment']) -> None:
    # get course links

    for link, student_list in students.items():
        # access exams
        assignment_links = get_assignment_links(driver, f"{link}/quizzes", assignments)

        # add accommodations to each students for the given course
        add_accommodations(driver, assignment_links, assignments, student_list)


if __name__ == "__main__":
    URL: str = "https://onramps.instructure.com"

    # assignments
    assignments = get_assignments()

    # get students
    students = get_students()

    # initialize driver
    driver = Driver.initialize()
    login(driver, URL)

    # begin scraping
    run(driver, students, assignments)