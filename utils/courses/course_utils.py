from typing import List
from dataclasses import dataclass
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@dataclass
class CourseDescriptor:
    name: str
    link: str


class GetLinksMixin:
    def get_links(self, driver: 'Driver', url: str, start: int, end: int, course: 'Course') -> List['CourseDescriptor']:
        # get course links
        course_links = []
        for page in range(start, end):
            course_links.extend(self._parse_page(driver, f"{url}page={str(page)}", course))

        return course_links

    def _parse_page(self, driver: 'Driver', url: str, course: 'Course') -> List[str]:
        # get page
        driver.get(url)

        # wait for page to load
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"//tbody/tr/td/a[contains(text(), '{course.ID}')]")))

        # fetch all potential courses
        elements = [elem for elem in driver.find_elements_by_xpath("//a")]

        # filter links for valid course numbers
        courses = []
        for elem in elements:
            if course.valid(elem):
                name = elem.text
                link = elem.get_attribute('href')
                courses.append(CourseDescriptor(name=name, link=link))

        return courses