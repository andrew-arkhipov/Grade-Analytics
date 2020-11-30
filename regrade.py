from typing import List, Tuple
from utils.driver import Driver
from argparse import ArgumentParser

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
    # get question 7
    try:
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='speedgrader_iframe']")))
    except:
        driver.switch_to.default_content()
        driver.find_element_by_xpath("//i[@class='icon-arrow-right next']").click()
        return

    # determine the version type
    question = driver.find_element_by_xpath("//div/div/span[contains(text(), 'Question 7')]/../..")

    words = []
    for elem in question.find_elements_by_class_name("answer_group"):
        words.extend(elem.text.split("\n"))

    # get the answers in a readable format
    correct, answer = parse_answers(words)

    # grade answers
    grade = grade_answers(correct, answer)

    # input grade
    grade_input = driver.find_element_by_xpath("//div/div/span[contains(text(), 'Question 7')]/../span[@class='question_points_holder']/div[@class='user_points']/input[@class='question_input']")
    grade_input.clear()
    grade_input.send_keys(grade)

    # submit
    driver.find_element_by_xpath("//button[@class='btn btn-primary update-scores']").click()

    # next student
    driver.switch_to.default_content()
    driver.find_element_by_xpath("//i[@class='icon-arrow-right next']").click()


def login(driver: 'Driver', url: str) -> None:
    # get page
    driver.get(url)

    # wait for login
    WebDriverWait(driver, 35).until(EC.element_to_be_clickable((By.XPATH, "//iframe[@id='speedgrader_iframe']")))


def run(driver: 'Driver', num_students: int) -> None:
    # parse
    for _ in range(num_students):
        grade_student(driver)
        


if __name__ == "__main__":
    # url
    url = input("Enter url: ")

    # get range of students
    num_students = int(input("Number of students: "))

    # initialize driver
    driver = Driver.initialize()
    login(driver, url)

    # run
    run(driver, num_students)