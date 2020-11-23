from typing import List, Tuple, Dict
from utils.utils import login, get_students, get_course_type, get_unit_number
from utils.utils import Assignment
from utils.driver import Driver
from utils.courses.courses import CollegeCourse
from argparse import ArgumentParser
from math import ceild

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


def add_accommodations(driver: 'Driver', url: str, duration: int, students: List['Student']) -> None:
    # go to exam
    driver.get(f"{url}/moderate")

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
        extra_time = get_extra_time(duration, eval(student.multiplier))
        add_extensions(driver, extra_time)

        # refresh
        driver.refresh()


def get_exam_link(driver: 'Driver', unit: int, part: int) -> str:
    # get element
    elem = driver.find_element_by_xpath(f"//a[contains(text(), 'Exam Unit {str(unit)}: Part {str(part)}')]")

    # extract link
    link = elem.get_attribute("href")

    return link


def get_exam_links(driver: 'Driver', unit: int) -> Tuple[str, str]:
    # wait for table with quizzes to load
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//h2[@aria-controls='assignment-quizzes']")))

    # get links for each part
    part_one_link = get_exam_link(driver, unit, 1)
    part_two_link = get_exam_link(driver, unit, 2)

    return part_one_link, part_two_link


def run(driver: 'Driver', url: str, students: Dict[str, List['Student']], unit: int, course: 'Course') -> None:
    # get course links
    links = course.get_links(driver, url)

    for link in links:
        # access exams
        driver.get(f"{link.link}/quizzes")
        part_one, part_two = get_exam_links(driver, unit)

        # part one
        add_accommodations(driver, part_one, 45, students[link.name])

        # part two
        add_accommodations(driver, part_two, 30, students[link.name])


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
    unit = get_unit_number()

    # get students
    students = get_students(args.accom_file)

    # initialize driver
    driver = Driver.initialize()
    login(driver, url)

    # begin scraping
    run(driver, url, students, unit, course)    