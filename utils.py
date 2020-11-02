from time import sleep
import shutil
import os

def wait_for_download(func):

    SOURCE_DIR = "/Users/andrew/Downloads"
    TARGET_DIR = "/Users/andrew/Side Projects/Grade Analytics/Reports"

    def inner(*args, **kwargs):
        # run scraper
        func(*args, **kwargs)

        # wait for download to start
        while not any(filename.endswith(".csv") for filename in os.listdir(SOURCE_DIR)):
            sleep(0.1)

        # move files
        for filename in os.listdir(SOURCE_DIR):
            shutil.move(os.path.join(SOURCE_DIR, filename), TARGET_DIR)

    return inner