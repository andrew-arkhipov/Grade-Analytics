from typing import List
from utils.utils import login, parse_csv, get_course_type, get_unit_number
from utils.driver import Driver
from argparse import ArgumentParser

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def run(driver: 'Driver', url: str, filename: str, unit: int, course: 'Course') -> None:
    # get course links
    links = course.get_links()

    # parse csv
    students = parse_csv(filename)




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