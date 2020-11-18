from typing import List, Tuple
from utils.utils import login, parse_csv, get_course_type, get_unit_number
from utils.driver import Driver
from argparse import ArgumentParser

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def add_accommodations(driver: 'Driver', url: str, students: List['Student']) -> None:
    # go to exam
    driver.get(url)


def get_exam_links(driver: 'Driver', unit: int) -> Tuple(str, str):
    # wait for table with quizzes to load
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//h2[contains(text(), 'Assignment Quizzes)]")))

    # link lambda
    exam_link = lambda driver, unit, part: driver.find_element_by_xpath(f"//a[contains(text(), 'Exam Unit {unit}: Part {part}").get_attribute("href")

    # get links for each part
    part_one_link = exam_link(driver, unit, 1)
    part_two_link = exam_link(driver, unit, 2)

    return part_one_link, part_two_link


def run(driver: 'Driver', url: str, filename: str, unit: int, course: 'Course') -> None:
    # get course links
    links = course.get_links()

    # parse csv
    students = parse_csv(filename)

    for link in links:
        # access exams
        driver.get(f"{link.link}quizzes")
        part_one, part_two = get_exam_links(driver, unit)

        # part one
        add_accommodations(driver, part_one, students[link.name])

        # part two
        add_accommodations(driver, part_two, students[link.name])



if __name__ == "__main__":
    # courses main page
    url = 'https://onramps.instructure.com/accounts/169964?'

    # parse command line arguments
    parser = ArgumentParser()
    parser.add_argument('accom_file', nargs='?')
    args = parser.parse_args()

    # course type
    course_type = get_course_type()

    # unit number
    unit = get_unit_number()

    # initialize driver
    driver = Driver.initialize()
    login(driver, url)

    # begin scraping
    run(driver, url, args.accom_file, unit, course)    