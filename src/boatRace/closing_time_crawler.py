# -*- coding=utf8 =*-
# 1. 朝、このスクリプトを回し、その日のレーススケジュールcronを作成
# 2. レーススケジュールcronに、automated_voterを実行させる

import datetime
import pandas as pd

def crawle_race_schedule(soup, rno, jcd, hd):
    """
    soupをパースし, 日付、会場、レースナンバー、締め切り時刻のdfを返す
    :param soup:
    :return race_result_list: [日付、レース場、レース、順位、枠番、登録番号、選手名、タイム]のリストを一位から6位までネストしたリスト
    """
    cols = ["日付", "会場"、"レースナンバー"、"締め切り時刻"]
    closing_time_list = []

    table = soup.find(class_="table1")
    row = table.find("tr")
    closing_times = row.find_all("td", {"class": " "})

    # 各レースについて、[日付、会場, レース名, 締め切り時刻]のリストを要素にとるリストを作成
    for i, closing_time in enumerate(closing_times, 1):
        race_number = str(i) + "R"
        closing_time_text = closing_time.text
        closing_time_time = datetime.datetime.strftime(closing_time_text, '%H:%M')
        closing_time_list.append([hd, jcd, race_number, closing_time_time])

    closing_time_df = pd.DataFrame(closing_time_list, columns=cols)

    return closing_time_df


def cron_generater():

    """
    closing_time_dfをインプットにして、その日のcronをgenerateする関数
    generateしたcronはshファイルで書きだして、それを実際に食わせるのはとりあえず手動でOK
    :return:
    """

if __name__ == "__main__":

