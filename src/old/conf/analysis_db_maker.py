# -*- coding=utf8 =*-

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../../conf/'))

# my module
import csv_loader
import summarizer_motorboat_data_filename

def add_stochastic_and_previous_data(x):
    """
    これまでの色々なデータの平均や、x走前のデータを追加したりなどして解析用のデータベースを作成。
    :param x:
    :return:
    """

    for i in range(1, 7):
        # 指定したレースのメンツに対して、前走の順位、前走タイム、前走スタートおよびレース結果をカラムにしたdfを作成。
        racer = x["ボートレーサー_{0}".format(i)]
        filtered_df = the_race_result_df[the_race_result_df["ボートレーサー_{0}".format(i)] == racer]
        x["ave_starttime_{0}".format(i)] = filtered_df["starttime_float_{0}".format(i)].mean()
        x["ave_着_{0}".format(i)] = filtered_df["着_{0}".format(i)].mean()

    return x


if __name__ == "__main__":

    # 過去のraceresultをcsvからload
    the_race_result_df = csv_loader.load_all_raceResults_as_a_df()

    # dateおよびrace_float (レース番号）を基準に並び替え
    the_race_result_df = the_race_result_df.sort_values(["日付", "race_float"])

    # dfを小さくする (※テスト用）
    # the_race_result_df = the_race_result_df.iloc[1::1000]

    # これまでのその選手の平均スタートタイムや平均着順などのカラムを追加
    for_analysis_df = the_race_result_df.apply(add_stochastic_and_previous_data, axis=1)

    # csvに書きだし
    for_analysis_df.to_csv(summarizer_motorboat_data_filename.make_csv_for_analysis())