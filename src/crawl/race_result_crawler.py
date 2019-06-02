# -*- coding=utf8 =*-
import re
import pandas as pd
import itertools
import time
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../conf/'))
sys.path.append(os.path.join(current_dir, '../simulation/'))
# my module
import boatrace_crawler_conf
import summarizer_motorboat_data_filename


def crawle_race_result(soup, rno, jcd, hd):
    """
    soupをパースし, 順位、選手登録番号、枠番、線署名といった情報scrapeする
    cols, rno, jcd, hdというinputは、そのままoutputに入れるために入力値にしている（内部で計算なし）
    :param soup:
    :return race_result_list: [日付、レース場、レース、順位、枠番、登録番号、選手名、タイム]のリストを一位から6位までネストしたリスト
    """

    race_result_dict = {"日付": hd, "レース場": jcd, "レース": rno}
    table = soup.find(class_="grid_unit").find(class_="table1")
    rows = table.find_all("tbody")

    for i, row in enumerate(rows, 1):
        rank = i  # 順位
        frame = row.find("td", {"class": re.compile("is-fs14 is-fBold")}).text  # 枠番
        registration_number = row.find("span", {"class": "is-fs12"}).text  # 選手登録番号
        racer_name = row.find("span", {"class": "is-fs18 is-fBold"}).text  # 選手名
        race_time = row.find_all("td")[3].text
        # race_result_listの要素としてクロールした結果のリストを追加
        race_result_dict["着_{0}".format(frame)] = rank
        race_result_dict["登録番号_{0}".format(frame)] = registration_number
        race_result_dict["ボートレーサー_{0}".format(frame)] = racer_name
        race_result_dict["レースタイム_{0}".format(frame)] = race_time

    # スタート情報を追記する
    start_time_souplist = soup.find_all("div", {"class": "table1_boatImage1"})
    for start_time in start_time_souplist:
        boat_number = start_time.find("span", {"class": "table1_boatImage1Number"}).text
        boat_start_time = start_time.find("span", {"class": "table1_boatImage1TimeInner"}).text[:3]
        # Late, Flingの際に、L1改行みたいに書かれており、改行が混ざることがあるので
        if boat_start_time[0] == "L" or boat_start_time[0] == "F":
            boat_start_time = boat_start_time[0]

        race_result_dict["スタートタイム_{0}".format(boat_number)] = boat_start_time

    # dictをdfに変換
    race_result_df = pd.io.json.json_normalize([race_result_dict])

    return race_result_df


if __name__ == "__main__":

    #################### inputs ########################

    # crawl開始日付、終了日付の指定
    the_date_from = '20181109'
    the_date_to = '20181201'

    ####################################################

    # 以下で定義する全てのリストの要素の組み合わせについてcrawlを行う.
    # race noのリスト
    the_rno_list = [str(i + 1) + "R" for i in range(12)]
    # 会場のリスト
    the_jcd_dict = boatrace_crawler_conf.make_jcd_dict()
    the_jcd_list = list(the_jcd_dict.keys())
    # 日付のリスト
    the_hd_list = boatrace_crawler_conf.make_hd_list(the_date_from, the_date_to)
    print(the_hd_list)


    for the_hd in the_hd_list:
        this_race_result_df_list = []
        for the_rno, the_jcd in itertools.product(the_rno_list, the_jcd_list):

            # 以下、crawl実行部分
            # クロール対象サイトのurl作成
            the_raceResult_url = boatrace_crawler_conf.make_url("raceresult", the_rno, the_jcd, the_hd)
            print(the_raceResult_url)

            # 存在しないraceをinputしてしまった時のためのtry-except
            try:
                # 対象サイトをパースしてcrawl
                the_soup = boatrace_crawler_conf.html_parser(the_raceResult_url)
                this_race_result_df = crawle_race_result(the_soup, the_rno, the_jcd, the_hd)
                this_race_result_df_list.append(this_race_result_df)
                # print(this_race_result_df)

            except AttributeError:
                pass

            time.sleep(0.1)

        # その日のraceResultを一つのdfにまとめる
        the_race_result_df = pd.concat(this_race_result_df_list)
        # output csvファイルの指定
        the_boatrace_results_file = summarizer_motorboat_data_filename.make_csv_race_results(the_hd)
        # 書きだし
        the_race_result_df.to_csv(the_boatrace_results_file, index=False)