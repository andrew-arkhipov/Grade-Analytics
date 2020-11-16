from typing import List
from utils.utils import login, parse_page, download_manager
from utils.driver import Driver
from utils.courses import Courses
from argparse import ArgumentParser

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By