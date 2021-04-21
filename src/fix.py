from utils.utils import login
from utils.driver import Driver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

url = "https://onramps.instructure.com/courses/3018359/gradebook/speed_grader?assignment_id=28391460&student_id=11661169"

def grade_student(driver):
    # get question 7
    try:
        WebDriverWait(driver, 4).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='speedgrader_iframe']")))
    except:
        driver.switch_to.default_content()
        driver.find_element_by_xpath("//i[@class='icon-arrow-right next']").click()
        return

    fudge = driver.find_element_by_xpath("//input[@id='fudge_points_entry']")
    fudge.clear()
    fudge.send_keys(0)

    # submit
    driver.find_element_by_xpath("//button[@class='btn btn-primary update-scores']").click()

    # next student
    driver.switch_to.default_content()
    driver.find_element_by_xpath("//i[@class='icon-arrow-right next']").click()


if __name__ == "__main__":
    driver = Driver.initialize()
    driver.get(url)
    time.sleep(30)
    for _ in range(141):
        grade_student(driver)
