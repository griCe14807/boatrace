# -*- coding=utf8 =*-
import time
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../conf/'))

# my module
import boatrace_crawler_conf
import selenium_conf


def get_start_time():

    # スタート展示タブへ移動
    driver.find_element_by_xpath("// *[ @ id = 'raceheader_board'] / a[3]").click()
    time.sleep(INTERVAL)

    # スタート展示のタイムを取得しリストへ格納
    start_time_list = []
    for i in range(2, 8):
        start_time = driver.find_element_by_xpath('//*[@id="board_stt"]/div[1]/table/tbody/tr[{0}]/td[5]'.format(i)).text
        # print(start_time)
        start_time_list.append(start_time)
    time.sleep(INTERVAL)

    return start_time_list


def get_exhibition_time(driver, INTERVAL):
    # 直前情報タブへ移動
    driver.find_element_by_xpath('//*[@id="raceheader_board"]/a[4]').click()
    time.sleep(INTERVAL)

    # 展示タイムを取得しリストへ格納
    exhibition_time_list = []
    for i in range(6):
        exhibition_time = driver.find_element_by_xpath(
            '// *[ @ id = "board_tkz"] / div[1] / table / tbody / tr[{0}] / td[3]'.format(3 + 2 * i)).text
        print(exhibition_time)
        exhibition_time_list.append(exhibition_time)
    time.sleep(INTERVAL)

    return exhibition_time_list


def main(input_jcd, INTERVAL):

    # crawle先のurlを作成
    jcd_number = boatrace_crawler_conf.make_jcd_dict()[input_jcd]
    target_url = "http://livebb.jlc.ne.jp/bb_top/new_bb/index.php?tpl={0}".format(jcd_number)

    # driver
    driver = selenium_conf.load_driver()
    time.sleep(INTERVAL)

    # 対象サイトへアクセス
    driver.get(target_url)
    time.sleep(INTERVAL)

    # 展示タイムを取得
    exhibition_time_list = get_exhibition_time(driver, INTERVAL)

    # floatに変換
    exhibition_time_list = [float(time) for time in exhibition_time_list]

    # ブラウザを閉じる
    # driver.quit()

    return exhibition_time_list



if __name__ == "__main__":

    # ------------input-------------- #

    input_jcd = "若　松"

    # 各動作間の待ち時間（秒）
    INTERVAL = 3

    # ------------------------------- #

    the_exhibition_time_list = main(input_jcd, INTERVAL)