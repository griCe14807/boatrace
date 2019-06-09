# -*- coding=utf8 =*-

"""
新しい特徴量を生み出すことはせず、

"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../conf/'))
sys.path.append(os.path.join(current_dir, '../../crawl/'))
sys.path.append(os.path.join(current_dir, '../../data_preparing/'))


# my module
import loader
import boatrace_crawler_conf


def crawle_race_list(soup):
    """
    soupから選手名をリストとして取得
    :return racer_list: 出場選手名を枠順に並べたリスト
    """

    racer_list = []
    table = soup.find(class_="contentsFrame1_inner").find_all(class_="table1")[1]
    rows = table.find_all("tbody", {"class": "is-fs12"})

    for row in rows:
        # 選手名を取得。最後の[1:-1]は改行を削除するため
        racer_name = row.find(class_="is-fs18 is-fBold").text[1:-1]
        # race_result_listの要素としてクロールした結果のリストを追加
        racer_list.append(racer_name)

        # racerの書式をダウンロードファイルに合わせる
        racer_list_mod = []
        for racer_ in racer_list:
            racer_ = racer_.split("\u3000")
            if len(racer_[0]) == 1:
                racer_[0] = racer_[0] + "\u3000\u3000"
            elif len(racer_[0]) == 2:
                racer_[0] = racer_[0][0] + "\u3000" + racer_[0][1]

            if len(racer_[-1]) == 1:
                racer_[-1] == "\u3000\u3000" + racer_[-1]
                racer = racer_[0] + "\u3000\u3000\u3000\u3000" + racer_[-1]

            elif len(racer_[-1]) == 2:
                racer_[-1] = racer_[-1][0] + "\u3000" + racer_[-1][1]
                racer = racer_[0] + "\u3000\u3000" + racer_[-1]

            racer_list_mod.append(racer)

    print(racer_list_mod)

    return racer_list_mod



if __name__ == "__main__":

    ################inputs#################

    rno = "12R"
    jcd = "住之江"
    hd = "2019/06/09"

    # 過去のレース結果をdfとして取得
    the_race_result_df = loader.load_race_results()
    print(the_race_result_df)

    #  Filteringを行うためのレーサーネームをcrawle
    raceList_url = boatrace_crawler_conf.make_url("racelist", rno, jcd, hd)
    soup = boatrace_crawler_conf.html_parser(raceList_url)
    racer_list = crawle_race_list(soup)

    # 散布図
    plt.rcParams['font.family'] = 'Hiragino Sans'
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # 積み上げ棒グラフ
    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(1, 1, 1)
    # 積み上げ棒グラフ作成時の、積み上げ元の位置を決める変数
    bottom_array = np.array([0, 0, 0, 0, 0, 0])

    for i, racer in enumerate(racer_list, 1):
        # plot用データを作成: racername+枠番でfiltering
        filtered_df = the_race_result_df[the_race_result_df["racerName_{0}".format(i)] == racer]
        print(filtered_df[["racerName_{0}".format(i), "date", "venue", "raceNumber", "rank_{0}".format(i), "startTime_{0}".format(i)]])

        # 散布図を作成 (日付 vs racetime)
        x = filtered_df["date"]
        y = filtered_df["raceTime_{0}".format(i)]
        ax.plot_date(x, y, label="{0}号艇_{1}".format(i, racer))

        # 順位ごとの積み上げ棒グラフを作成
        count_array = np.array([sum(filtered_df["rank_{0}".format(i)] == j) for j in range(1, 7)])
        ax2.bar(np.array(["1着", "2着", "3着", "4着", "5着", "6着"]), count_array, bottom=bottom_array)
        bottom_array = bottom_array + count_array

    ax.legend()
    plt.show()
