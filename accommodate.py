from typing import List
from utils.utils import login, parse_csv
from utils.driver import Driver
from utils.courses.courses import CollegeCourse
from argparse import ArgumentParser

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def run(driver: 'Driver', url: str, filename: str, course: 'Course') -> None:
    # login
    login(driver, url)

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

    # initialize driver with target download directory
    driver = Driver.initialize()

    # begin scraping
    run(driver, url, course, args.accom_file)    