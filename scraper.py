from typing import List
from utils import download_manager, login
from driver import Driver
from argparse import ArgumentParser
from courses import Course

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def parse_page(driver: Driver, url: str, course: Course) -> List[str]:
    # get page
    driver.get(url)

    # wait for page to load
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Discovery Precalculus - UT COLLEGE')]")))

    # fetch all links
    links = []
    for link in driver.find_elements_by_xpath("//a[@href]"):
        links.append(link.get_attribute("href"))

    # filter links for valid course numbers
    courses = []
    for link in links:
        if course.valid(link):
            courses.append(link)

    return courses


def get_links(driver: Driver, url: str) -> List[str]:
    # get all course links
    course_links = []
    for page in range(1, 8):
        course_links.extend(parse_page(driver, f"{url}page={str(page)}", Course.COLLEGE))

    return course_links


@download_manager
def download(driver: Driver, url: str) -> None:
    # visit the course page
    driver.get(url)

    # wait for download button
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@data-component='ActionMenu']"))).click()

    # download grade report
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Export']"))).click()


def run(driver, url):
    # login
    login(driver, url)

    # initialize
    course_links = get_links(driver, url)
    
    # parse
    for link in course_links:
        download(driver, f"{link}/gradebook")


if __name__ == "__main__":
    # courses main page
    url = 'https://onramps.instructure.com/accounts/169964?'

    # parse command line arguments
    parser = ArgumentParser()
    parser.add_argument("target_dir", nargs='?')
    args = parser.parse_args()

    # initialize driver with target download directory
    driver = Driver.initialize(args.target_dir)

    # begin scraping
    run(driver, url)
