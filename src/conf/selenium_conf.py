# -*- coding=utf8 =*-

import os
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def load_driver():

    # driverへのパス
    DRIVER_WIN = "chromedriver.exe"
    DRIVER_MAC = '/usr/local/bin/chromedriver'

    # ブラウザ起動
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver_path = DRIVER_WIN if os.name == "nt" else DRIVER_MAC
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    return driver

if __name__ == "__main__":
    driver = load_driver()