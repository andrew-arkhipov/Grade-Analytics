from time import sleep
from functools import wraps
import shutil
import os


def download_manager(func):

    @wraps(func)
    def inner(*args, **kwargs):
        # preprocessing
        driver = args[0]
        size = len(os.listdir(driver.download_directory))

        # run scraper
        func(*args, **kwargs)

        # wait for download to start
        while len(os.listdir(driver.download_directory)) == size:
            sleep(0.05)

    return inner