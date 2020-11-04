class Course:
    pass

class CollegeCourse(Course):
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

class HighSchoolCourse(Course):
    @staticmethod
    def valid(element: 'selennium.webdriver.remote.webelement.WebElement') -> bool:
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

class Courses:
    COLLEGE = CollegeCourse
    HIGHSCHOOL = HighSchoolCourse