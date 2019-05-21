# -*- coding=utf8 =*-
# boatraceの結果をloadする際に、改行が混じってしまったやつを見つけ出す
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../conf/'))

import summarizer_motorboat_data_filename
import pandas as pd


# 以下関数内で引かれている関数
def convert_time_into_float(x):
    """

    :param x:
    :return:
    """
    # 5位6位のタイムは空なのでif文
    if type(x) == float or len(x) is not 6:
        # 5位6位の時はタイムは一律125として表示
        return 125

    if len(x) == 6:
        return int(x[0]) * 60 + int(x[2:4]) + int(x[5])/10


def load_all_raceResults_as_a_df(race_results_df):

    # racetime, start timeを全てfloatに変換
    searchfor = ["F", "L"]
    for i in range(1, 7):
        # racetimeをstrから秒数（float）に直す
        racetime_float = race_results_df["レースタイム_{0}".format(i)].map(convert_time_into_float)
        race_results_df["racetime_float_{0}".format(i)] = racetime_float

        # strメソッドを使うため、一旦strに変換
        race_results_df["スタートタイム_{0}".format(i)] = race_results_df["スタートタイム_{0}".format(i)].astype(str)
        # フライング, Lateがあったレースのデータは取り除く
        race_results_df = race_results_df[~(race_results_df["スタートタイム_{0}".format(i)].str.contains("|".join(searchfor), na=False))]
        # start timeもfloatに。
        race_results_df["starttime_float_{0}".format(i)] = race_results_df["スタートタイム_{0}".format(i)].map(float)

    return race_results_df


if __name__ == "__main__":

    the_raceResults_directory_path = summarizer_motorboat_data_filename.return_directory_path("raceResults")
    the_raceResults_files = os.listdir(the_raceResults_directory_path)

    # レース結果を全てのファイルからロード
    raceResults_file_list = [os.path.join(the_raceResults_directory_path, the_raceResults_file)
                           for the_raceResults_file in the_raceResults_files
                           if not os.path.isdir(the_raceResults_file) and the_raceResults_file[-4:] == ".csv"]
    receResults_df_list = [pd.read_csv(raceResult_file, parse_dates=["日付"]) for raceResult_file in raceResults_file_list]

    for raceresult_df in receResults_df_list:
        print(raceresult_df["日付"][1])
        load_all_raceResults_as_a_df(raceresult_df)

