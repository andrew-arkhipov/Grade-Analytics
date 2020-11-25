from typing import List
from utils.courses.course_utils import GetLinksMixin


class CollegeCourse(GetLinksMixin):
    ID = 'UT COLLEGE'
    def __init__(self, class_type: 'Classes'):
        self.class_type = class_type

    def valid(element: 'WebElement') -> bool:
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
        return super().get_links(driver, url, self.class_type['CO'],  self.__class__)
        

class HighSchoolCourse(GetLinksMixin):
    ID = 'HS'
    def __init__(self, class_type: 'Classes'):
        self.class_type = class_type

    def valid(element: 'WebElement') -> bool:
        text = element.text
        link = element.get_attribute('href')

        if link[32:37] == 'users':
            return False
        elif 'HS' not in text:
            return False
        elif link[-1].isdigit() and link[-7].isdigit():
            return True
        else:
            return False

    def get_links(self, driver: 'Driver', url: str) -> List['CourseDescriptor']:
        return super().get_links(driver, url, self.class_type['HS'], self.__class__)
