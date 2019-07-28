# -*- coding=utf8 =*-

import os
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def load_driver():

    # driverへのパス
    DRIVER_WIN = "chromedriver.exe"
    DRIVER_MAC = '/Users/grice/Desktop/Selenium/chromedriver'

    # ブラウザ起動
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver_path = DRIVER_WIN if os.name == "nt" else DRIVER_MAC
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    return driver

if __name__ == "__main__":
    driver = load_driver()