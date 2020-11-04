from typing import List, Dict
from utils.utils import login, parse_page
from utils.driver import Driver
from utils.courses import Courses
from argparse import ArgumentParser

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_links(driver: 'Driver', url: str) -> List[str]:
    # get all course links
    course_links = []
    for page in range(7, 8):
        course_links.extend(parse_page(driver, f"{url}page={str(page)}", Courses.HIGHSCHOOL))

    return course_links


def access_survey(driver: 'Driver', url: str) -> bool:
    # assignments page
    driver.get(url)

    # click on survey link
    try:
        WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Student Perspective Survey Fall 1')]"))).click()
    except:
        # not a valid high school course
        return False

    # open survey tab
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Load Student Perspective Survey')]"))).click()

    # switch to new tab
    driver.switch_to.window(driver.window_handles[1])

    return True


def survey_helper(driver: 'Driver', text: str, frame_id: str) -> None:
    # wait for iframe and switch to it
    WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,f"//iframe[contains(@id, '{frame_id}')]")))

    # input text
    body = driver.find_element_by_css_selector("body")
    body.clear()
    body.send_keys(text)

    # switch back to global frame
    driver.switch_to.default_content()


def fill_survey(driver: 'Driver', inputs: Dict[str, str]) -> None:
    # wait
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input")))

    # input url
    url_input = driver.find_element_by_xpath("//input")
    url_input.clear()
    url_input.send_keys(inputs['url'])

    # input intro text
    survey_helper(driver, inputs['intro'], 'intro_text_ifr')

    # input finished text
    survey_helper(driver, inputs['finish'], 'finish_text_ifr')

    # submit
    driver.find_element_by_xpath("//button[@type='submit']").click()

    # switch to original tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def run(driver: 'Driver', url: str, inputs: Dict[str, str]) -> None:
    # login
    login(driver, url)

    # get links
    course_links = get_links(driver, url)

    # fill out forms
    for link in course_links:
        flag = access_survey(driver, f"{link}/assignments")
        if flag:
            fill_survey(driver, inputs)


if __name__ == "__main__":
    # courses main page
    url = 'https://onramps.instructure.com/accounts/169964?'

    # get user inputs
    inputs = {
        'url': input('Enter Qualtrics survey URL: '),
        'intro': input('Enter intro text: '),
        'finish': input('Enter finished text: ')
    }

    # initialize driver
    driver = Driver.initialize()

    # begin scraping
    run(driver, url, inputs)