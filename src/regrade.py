from typing import List, Tuple
from time import sleep

from utils.driver import Driver
from utils.utils import login
from utils.courses.courses import CollegeCourse
from argparse import ArgumentParser

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


answers = {
    (16, 9, -160, -54, 337):[
        (16.0, 9.0, -160.0, -54.0, 337.0),
        (1.0, 9/16, -10.0, -27/8, 337/16), 
        (16/9, 1.0, -160/9, -6.0, 337/9)
    ],
    (1, 4, 2, -32, 49):[
        (4.0, 16.0, 8.0, -128.0, 196.0),
        (1.0, 4.0, 2.0, -32.0, 49.0),
        (1/4, 1.0, 1/2, -8.0, 49/4)
    ],
    (16, 25, 32, 150, -159):[
        (16.0, 25.0, 32.0, 150.0, -159.0),
        (1.0, 25/16, 2.0, 75/8, -159/16),
        (16/25, 1.0, 32/25, 6.0, -159/25)
    ],
    (25, 16, 150, 64, -111):[
        (25.0, 16.0, 150.0, 64.0, -111.0),
        (1.0, 16/25, 6.0, 64/25, -111/25),
        (25/16, 1.0, 75/8, 4.0, -111/16)
    ],
    (9, 4, -36, 24, 36):[
        (9.0, 4.0, -36.0, 24.0, 36.0),
        (1.0, 4/9, -4.0, 8/3, 4.0),
        (9/4, 1.0, -9.0, 6.0, 9.0)
    ],
    (25, 4, -200, -24, 336):[
        (25.0, 4.0, -200.0, -24.0, 336.0),
        (1.0, 4/25, -8.0, -24/25, -336/25),
        (25/4, 1.0, -50.0, -6.0, 84.0)
    ]
}


def grade_answers(correct: Tuple[int], answer: Tuple[int]) -> int:
    # error constant
    EPSILON = 5e-2

    # parse through each grade possibility
    grade = 0
    for potential in answers[correct]:
        grade = max(grade, sum(2 if c - EPSILON <= a <= c + EPSILON else 0 for c, a in zip(potential, answer)))

    print(grade)
    return grade


def parse_answers(elems: List[str]) -> (Tuple[int], Tuple[int]):
    # initialize return values
    correct = [0]*5
    answer = [0]*5

    # answer pointer
    curr = 1

    # parse
    for i, text in enumerate(elems):
        if text == f"Answer {str(curr)}:":
            correct[curr-1] = int(eval(elems[i+4]))
            try:
                answer[curr-1] = float(eval(elems[i+2]))
            except:
                answer[curr-1] = 0
            curr += 1

    # convert to tuples
    correct = tuple(correct)
    answer = tuple(answer)

    return correct, answer


def grade_student(driver: 'Driver') -> None:
    # wait for questions to load
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div/div/span[contains(text(), 'Question 1') or contains(text(), 'Pregunta 1')]")))

    question = driver.find_element_by_xpath("//div/div/span[contains(text(), 'Question 1') or contains(text(), 'Pregunta 1')]/../..")
    score = int(question.find_element_by_xpath("//div[@class='header']/span/div[@class='user_points']/input[@class='question_input']").get_attribute('value'))

    if score == 0:
        total = float(driver.find_element_by_xpath("//span[@class='score_value']").text)

        fudge = driver.find_element_by_xpath("//input[@id='fudge_points_entry']")
        current_fudge = float(fudge.get_attribute('value') or 0)

        fudge.clear()

        points = round(round((total - current_fudge) * 10/9, 2) - (total - current_fudge), 2)
        fudge.send_keys(str(points))

    # submit
    driver.find_element_by_xpath("//button[@class='btn btn-primary update-scores']").click()

    # next student
    driver.switch_to.default_content()
    driver.find_element_by_xpath("//i[@class='icon-arrow-right next']").click()


def show_all_sections(driver) -> None:
    action = ActionChains(driver)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='students_selectmenu-button']")))
    dropdown = driver.find_element_by_xpath("//a[@id='students_selectmenu-button']")

    # click on dropdown menu
    action.move_to_element(dropdown).click(on_element=dropdown)

    # move mouse over to show all sections option
    # action.move_by_offset(0, 40).move_by_offset(-170, 0).click().perform()

    action.move_by_offset(0, 40).perform()
    action.move_by_offset(-170, 0).perform()
    action.click()

    action.perform()


def access_assignment(driver: 'Driver', url: str) -> int:
    driver.get(url)

    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '7 & 8')]"))).click()
    except:
        # not a valid high school course
        return 0

    # open survey tab
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a/i/span[contains(text(), 'SpeedGrader')]/../.."))).click()

    # switch to new tab
    driver.switch_to.window(driver.window_handles[1])

     # use actions to click on dropdown menu and show all sections
    show_all_sections(driver)

    # wait for speedgrader to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='x_of_x_students_frd' and contains(text(), '/')]")))

    student_fraction = driver.find_element_by_xpath("//div[@id='x_of_x_students_frd']")
    num_students = int(student_fraction.text.split("/")[1])

    return num_students


def run(driver: 'Driver', num_students: int) -> None:
    # parse
    for _ in range(num_students):
        WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, "//i[@class='icon-arrow-right next']")))
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//div[@id='this_student_does_not_have_a_submission' and @style='display: block;']")))
            WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, "//i[@class='icon-arrow-right next']"))).click()
            continue
        except:
            pass
        try:
            WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='speedgrader_iframe']")))
            grade_student(driver)
        except:
            driver.switch_to.default_content()
            driver.find_element_by_xpath("//i[@class='icon-arrow-right next']").click()
            continue
        

if __name__ == "__main__":
    url = "https://onramps.instructure.com/accounts/172690?"

    driver = Driver.initialize()
    login(driver, url)

    course = CollegeCourse()
    links = course.get_links(driver, url, range(6, 7))

    # run
    for link in links:
        num_students = access_assignment(driver, f"{link.link}/assignments")
        run(driver, num_students)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])