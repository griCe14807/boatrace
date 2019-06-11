# -*- coding=utf8 =*-

import matplotlib.pyplot as plt
from pandas import plotting
import pandas as pd
import numpy as np
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../conf/'))
sys.path.append(os.path.join(current_dir, '../../crawl/'))

# my module
import csv_loader


def show_piled_bar_plot(second_place_count_df):
    """
    順位ごとの積み上げ棒グラフを作成

    :param second_place_count_df:
    :return:
    """
    plt.rcParams['font.family'] = 'Hiragino Sans'  # 日本語に対応
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # 積み上げ棒グラフ作成時の、積み上げ元の位置を決める変数
    bottom_array = np.zeros(len(second_place_count_df.columns))
    selected_racer_array = second_place_count_df.columns.values
    for index, row in second_place_count_df.iterrows():
        count_array = row.values
        ax.bar(selected_racer_array, count_array, bottom=bottom_array)
        bottom_array = bottom_array + count_array

    # ax.legend()
    plt.show()


if __name__ == "__main__":

    # 過去のレース結果をdfとして取得
    the_raceresult_summary_df = csv_loader.load_all_raceResults_as_a_df()

    # 一号艇で走ったことのある選手を取得（重複なし）
    # racer_array = the_raceresult_summary_df["ボートレーサー_1"].unique()

    racer_array = ['吉川\u3000\u3000元浩', '山一\u3000\u3000鉄也',
                   '金田\u3000\u3000\u3000諭', '田中\u3000信一郎',
                   '原田\u3000\u3000篤志', '原田\u3000\u3000幸哉',
                   '菊地\u3000\u3000孝平'
                   ]

    # 各枠が2着になった回数を要素としてもつdf
    second_place_count_df = pd.DataFrame()
    # 各枠が2着になった回数を確率を要素としてもつdf.上とは行列も入れ替えることに注意
    second_place_ratio_df = pd.DataFrame(columns=["着_{0}".format(i) for i in range(1, 7)])
    for racer in racer_array:
        # 選手かつ1枠でfiltering
        filtered_df = the_raceresult_summary_df[(the_raceresult_summary_df["ボートレーサー_1"] == racer) & (the_raceresult_summary_df["着_1"] == 1)]

        # 2-6枠の選手が2着になった場所だけが1, 他が0のbooleanを作成
        second_place_boolean_df = filtered_df[["着_{0}".format(i) for i in range(1, 7)]] == 2
        # print(racer, second_place_boolean_df)

        # 列で和をとって、枠番ごとの2着の回数にする
        second_place_count_series = second_place_boolean_df.sum()
        # 同上、ただし確率にする
        second_place_ratio_series = second_place_count_series / second_place_count_series.sum()
        second_place_ratio_series.name = racer

        # たくさんレースを指定ないデータは信頼度が低いので30レースより多い人のデータに絞る（あと表示が大変）
        if second_place_count_series.sum() > 30:
            second_place_count_df[racer] = second_place_count_series
            second_place_ratio_df = second_place_ratio_df.append(second_place_ratio_series)

    print(second_place_count_df)
    print(second_place_ratio_df)


    # 順位ごとの積み上げ棒グラフを作成
    show_piled_bar_plot(second_place_count_df)

    # 枠ごとの二着になる確率を全ての組み合わせで散布図作成
    plotting.scatter_matrix(second_place_ratio_df.iloc[:, 1:], figsize=(8, 8), alpha=0.5)
    plt.show()