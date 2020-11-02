from typing import List
from utils import wait_for_download

from webdriver_manager.chrome import ChromeDriverManager
from seleniumrequests.request import RequestMixin

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Driver(RequestMixin, webdriver.Chrome):
    @classmethod
    def initialize(cls) -> 'Driver':
        return cls(ChromeDriverManager().install())


def parse_page(driver: Driver, url: str) -> List[str]:
    # get page
    driver.get(url)

    # wait for page to load
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Discovery Precalculus - UT COLLEGE')]")))

    # fetch all links
    links = []
    for link in driver.find_elements_by_xpath("//a[@href]"):
        links.append(link.get_attribute("href"))

    # filter links for valid course numbers
    courses = []
    for link in links:
        if link[32:37] == "users":
            break
        elif link[-1].isdigit() and link[-7].isdigit():
            courses.append(link)

    return courses[:-1]


def get_links(driver: Driver, url: str) -> List[str]:
    # get login page
    driver.get(url)

    # wait for manual login
    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Discovery Precalculus - UT COLLEGE')]")))

    # get all course links
    course_links = []
    for page in range(1, 8):
        course_links.extend(parse_page(driver, f"{url}page={str(page)}"))

    return course_links


@wait_for_download
def download(driver: Driver, url: str) -> None:
    # visit the course page
    driver.get(url)

    # wait for download button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@data-component='ActionMenu']"))).click()

    # download grade report
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Export']"))).click()


def main():
    # courses main page
    url = 'https://onramps.instructure.com/accounts/169964?'

    # initialize
    driver = Driver.initialize()
    course_links = get_links(driver, url)
    
    # parse
    for link in course_links:
        download(driver, f"{link}/gradebook")


if __name__ == "__main__":
    main()