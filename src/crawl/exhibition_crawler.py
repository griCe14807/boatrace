# -*- coding=utf8 =*-
import glob
import os
import os.path
import time

from selenium import webdriver


target_url = "http://livebb.jlc.ne.jp/bb_top/new_bb/index.php?tpl=12"

DRIVER_WIN = "chromedriver.exe"
DRIVER_MAC = "/Users/grice/Desktop/Selenium"

# 各動作間の待ち時間（秒）
INTERVAL = 3

# ブラウザ起動
driver_path = DRIVER_WIN if os.name == "nt" else DRIVER_MAC
driver = webdriver.Chrome(executable_path=driver_path)
driver.maximize_window()
time.sleep(INTERVAL)

# 対象サイトへアクセス
driver.get(target_url)
time.sleep(INTERVAL)


# ブラウザを閉じる
driver.quit()