from typing import List, Tuple, Dict
from utils.utils import login, get_students, get_course_type, get_unit_number, get_assignments
from utils.driver import Driver
from utils.courses.courses import CollegeCourse
from argparse import ArgumentParser
from math import ceil

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def add_extensions(driver: 'Driver', extra_time: int) -> None:
    # find menu and submit time
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='extension_extra_time']")))
    input_box = driver.find_element_by_xpath("//input[@id='extension_extra_time']")
    input_box.clear()
    input_box.send_keys(extra_time)

    # save
    driver.find_element_by_xpath("//button/span[contains(text(), 'Save')]/..").click()


def add_accommodations(driver: 'Driver', assignment_links: List['str'], assignments: List['Assignment'], students: List['Student']) -> None:
    # loop through all assignments
    for assignment, link in zip(assignments, assignment_links):
        # go to exam
        driver.get(f"{link}/moderate")

        # calculate extra time
        get_extra_time = lambda duration, multiplier: int(ceil(duration * multiplier - duration))

        # get utils
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='search_term']")))

        # loop through students
        for student in students:
            # get utils
            input_box = driver.find_element_by_xpath("//input[@id='search_term']")
            submit = driver.find_element_by_xpath("//input[@value='Filter']")

            # find student
            input_box.clear()
            input_box.send_keys(f"{student.first} {student.last}")
            submit.click()

            # click on extensions menu and add acommodations
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//i/span[contains(text(), 'Change user extensions')]/.."))).click()
            extra_time = get_extra_time(assignment.duration, eval(student.multiplier))
            add_extensions(driver, extra_time)

            # refresh
            driver.refresh()


def get_assignment_links(driver: 'Driver', assignments: List['Assignment']) -> List['str']:
    # wait for table with quizzes to load
    WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, "//h2[@aria-controls='assignment-quizzes']")))

    # get link for each assignment
    links = []
    for assignment in assignments:
        elem = driver.find_element_by_xpath(f"//a[contains(text(), '{assignment.name}')]")
        link = elem.get_attribute("href")
        links.append(link)

    return links


def run(driver: 'Driver', url: str, students: Dict[str, List['Student']], assignments: List['Assignment'], course: 'Course') -> None:
    # get course links
    course_links = course.get_links(driver, url)

    for course_link in course_links:
        # access exams
        driver.get(f"{course_link.link}/quizzes")
        assignment_links = get_assignment_links(driver, assignments)

        # add accommodations to each students for the given course
        add_accommodations(driver, assignment_links, assignments, students[course_link.name])


if __name__ == "__main__":
    # courses main page
    url = 'https://onramps.instructure.com/accounts/169964?'

    # parse command line arguments
    parser = ArgumentParser()
    parser.add_argument('accom_file', nargs='?')
    args = parser.parse_args()

    # course type
    course = CollegeCourse()

    # unit number
    assignments = get_assignments()

    # get students
    students = get_students(args.accom_file)

    # initialize driver
    driver = Driver.initialize()
    login(driver, url)

    # begin scraping
    run(driver, url, students, assignments, course)    