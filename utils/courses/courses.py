from typing import List
from utils.courses.course_utils import GetLinksMixin

class Course:
    pass

class CollegeCourse(Course, GetLinksMixin):
    ID = 'Discovery Precalculus - UT COLLEGE'

    @staticmethod
    def valid(element: 'selenium.webdriver.remote.webelement.WebElement') -> bool:
        text = element.text
        link = element.get_attribute('href')

        if link[32:37] == 'users':
            return False
        elif 'UT COLLEGE' not in text:
            return False
        elif link[-1].isdigit() and link[-7].isdigit():
            return True
        else:
            return False

    def get_links(self, driver: 'Driver', url: str) -> List['CourseDescriptor']:
        return super().get_links(driver, url, 1, 8, self.__class__)
        

class HighSchoolCourse(Course, GetLinksMixin):
    ID = 'Discovery Precalculus - HS'

    @staticmethod
    def valid(element: 'selenium.webdriver.remote.webelement.WebElement') -> bool:
        text = element.text
        link = element.get_attribute('href')

        if link[32:37] == 'users':
            return False
        elif 'Precalculus - HS' not in text:
            return False
        elif link[-1].isdigit() and link[-7].isdigit():
            return True
        else:
            return False

    def get_links(self, driver: 'Driver', url: str) -> List['CourseDescriptor']:
        return super().get_links(driver, url, 7, 20, self.__class__)