import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../crawl/'))
sys.path.append(os.path.join(current_dir, 'voting_algolithms/'))

# my module
import boatrace_crawler_conf
import LR_voter


def argparser():
    """
    TODO bet amountなど、required=Falseにする系のinputを定義しておく。
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-rno", "--race_number",
                        help=u"'12R', '1R' のように、数字+Rの形で指定",
                        required=True
                        )
    parser.add_argument("-jcd", "--venue_name",
                        help=u"会場名。'大　村'、'　津　'のように、合計三文字になるよう全角スペースでパディング",
                        required=True
                        )
    parser.add_argument("-hd", "--holding_date",
                        help=u"日時。'2919/05/01'のように、yyyy/mm/ddの形で指定",
                        required=True
                        )
    args = parser.parse_args()

    return args


def bet_using_selenium(KanyusyaNo, AnsyoNo, PassWord, jcd, bet_amount, the_bet_list):
    """

    :param KanyusyaNo:
    :param AnsyoNo:
    :param PassWord:
    :param jcd:
    :param bet_amount:
    :param the_bet_list:
    :return:
    """
    # 2.1 操作するブラウザを開く
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome('/Users/grice/Desktop/Selenium/chromedriver', chrome_options=options)

    # 2.2 ログイン
    driver.get('https://boatrace.jp/owpc/pc/login?authAfterUrl=/pc/extra/tb/index.html%3FvoteTagId%3DcommonHead')
    driver.find_element_by_name("in_KanyusyaNo").send_keys(KanyusyaNo)
    driver.find_element_by_name("in_AnsyoNo").send_keys(AnsyoNo)
    driver.find_element_by_name("in_PassWord").send_keys(PassWord)
    driver.find_element_by_class_name("is-login1").click()
    # print(driver.current_url)

    # 2.3 投票ページへ移動
    driver.find_element_by_id("commonHead").click()
    handle_array = driver.window_handles
    driver.close()  # 元のページは閉じる
    driver.switch_to.window(handle_array[-1])
    # print(driver.current_url)

    # 投票するレースを指定
    time.sleep(2)   # jsを実行するための待機時間
    driver.find_element_by_id("jyo" + the_jcd_dict[jcd]).click()
    print(driver.current_url)

    time.sleep(2)   # JSを実行するための待機時間
    # print(driver.page_source)

    # オッズ投票のタブに移動
    driver.execute_script("document.querySelector('#betmsthod2 > a').click();")
    # bet額を入力
    driver.find_element_by_id("amount").send_keys(bet_amount)

    # the_bet_listに入っているボタン全てをクリック
    for the_bet_number in the_bet_list:
        btn_click_js = "document.querySelector('#oddskumiban" + the_bet_number + " > a').click();"
        # print(btn_click_js)
        driver.execute_script(btn_click_js)

    # 「ベットリストに追加」をクリック
    driver.execute_script('document.querySelector("#oddsAmountBtn > a").click();')
    time.sleep(2)

    # 「投票入力完了」をクリック→ページ遷移
    driver.find_element_by_link_text("投票入力完了").click()
    time.sleep(2)

    # passwardと合計金額を入力し、bet完了
    sum_bet_amount = bet_amount * 100 * len(the_bet_list)
    driver.find_element_by_id("amount").send_keys(sum_bet_amount)
    driver.find_element_by_id("pass").send_keys(vote_pass)

    # 「投票する」ボタンをクリック
    driver.find_element_by_id("submitBet").click()
    time.sleep(2)

    # 確認のポップアップをクリック
    driver.execute_script('document.querySelector("#ok").click();')

    # windowを閉じる
    driver.close()


################### Input ###################

# passwards
KanyusyaNo = "08421741"
AnsyoNo = "4563"
PassWord = "vFAY9R"
vote_pass = "65taka"

# betを行う際の基準
the_odds_threshold = 2.0
the_coming_rate_threshold = 0.03

# 一つの組番に対するbet額 (1なら100円、10なら100円)
bet_amount = 1

"""
# テスト用
the_rno = "10R"
the_jcd = "桐　生"
the_hd = "2019/07/07"
"""

threshold_1 = 0.7
threshold_2 = 0.65
threshold_3 = 0.3

the_args = argparser()
the_rno = the_args.race_number
the_jcd = the_args.venue_name
the_hd = the_args.holding_date

the_method = "LR"


##############################################

# レース場を指定するためのdictを作っておく(投票時に使用)
the_jcd_dict = boatrace_crawler_conf.make_jcd_dict()

# 1.bet listを作成
if __name__ == '__main__':
    the_bet_list = LR_voter.main(the_rno, the_jcd, the_hd, threshold_1, threshold_2, threshold_3)

    # if elseは投票先がない（基準値を超えるnumberが一つもない）時の対策
    if not the_bet_list:
        print("{0}{1}は投票候補なし".format(the_jcd, the_rno))
        pass
    else:
        bet_using_selenium(KanyusyaNo, AnsyoNo, PassWord, the_jcd, bet_amount, the_bet_list)