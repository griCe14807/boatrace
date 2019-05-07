# -*- coding=utf8 =*-
import numpy as np
import collections
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))
sys.path.append(os.path.join(current_dir, '../crawl/'))


# my module
import summarizer_motorboat_data_filename
import raceResult_filter
import boatrace_crawler_conf


# 以下関数内で引かれている関数
def convert_time_into_float(x):
    """

    :param x:
    :return:
    """
    # 5位6位のタイムは空なのでif文
    if len(x) == 6:
        return int(x[0]) * 60 + int(x[2:4]) + int(x[5])/10

    else:
    # 5位6位の時はタイムは一律125として表示
        return 125


def load_raceResults_as_a_df():
    the_raceResults_directory_path = summarizer_motorboat_data_filename.return_directory_path("raceResults")
    the_raceResults_files = os.listdir(the_raceResults_directory_path)

    # レース結果を全てのファイルからロード
    raceResults_file_list = [os.path.join(the_raceResults_directory_path, the_raceResults_file)
                           for the_raceResults_file in the_raceResults_files
                           if not os.path.isdir(the_raceResults_file) and the_raceResults_file[-4:] == ".csv"]
    receResults_df_list = [pd.read_csv(raceResult_file, parse_dates=["日付"]) for raceResult_file in raceResults_file_list]

    # レース結果を一つのdfにまとめる
    race_results_df = pd.concat(receResults_df_list)

    # racetimeをstrから秒数（float）に直す
    racetime_float = race_results_df["レースタイム"].map(convert_time_into_float)
    race_results_df["racetime_float"] = racetime_float

    # cmapで指定するため、枠番もfloat型にする
    race_results_df["枠"] = race_results_df["枠"].map(float)

    return race_results_df


def simulate_a_race(filtered_df_list, simulation_times):
    # TODO: 70秒台のレース結果（多分二周）はfilteringをかけといた方がいい

    simulation_result_list_3t = []
    simulation_result_list_2t = []
    for i in range(simulation_times):
        picked_racetime_array = np.array([])   # 1枠から6枠までの選手の、これまでのレースタイムをランダムにピック
        for filtered_df in filtered_df_list:
            random_picked_racetime = filtered_df.sample()["racetime_float"]
            picked_racetime_array = np.append(picked_racetime_array, random_picked_racetime)

        # 着順を 1-2-3-4-5-6 のようなstrとして取得
        # 順序のリストを作成
        order_of_arrival_array = np.argsort(picked_racetime_array) + 1
        # 三着までの結果しかいらないので4着以下はここで切る
        order_of_arrival_list = [str(element) for element in order_of_arrival_array]
        order_of_arrival_list_3t = order_of_arrival_list[:3]
        order_of_arrival_list_2t = order_of_arrival_list[:2]

        order_of_arrival_str_3t = "-".join(order_of_arrival_list_3t)
        order_of_arrival_str_2t = "-".join(order_of_arrival_list_2t)

        simulation_result_list_3t.append(order_of_arrival_str_3t)
        simulation_result_list_2t.append(order_of_arrival_str_2t)

    # simulation_result_listの各要素数をカウント
    c3t = collections.Counter(simulation_result_list_3t)
    c2t = collections.Counter(simulation_result_list_2t)

    # print(c)
    number_3t, counts_3t = zip(*c3t.most_common(20))
    number_2t, counts_2t = zip(*c2t.most_common(20))

    return number_3t, counts_3t, number_2t, counts_2t



if __name__ == "__main__":
    """
    過去の結果からレースのシミュレーションを行い、それぞれの着順がどのくらいの確率になるかを計算しcsvにして保存
    """
    ################inputs#################
    the_hd = "2019/05/07"

    # simulationの試行回数
    the_num_simulation = 10000

    #######################################

    # race noのリストを作成
    the_rno_list = [str(i + 1) + "R" for i in range(12)]
    # 会場のリスト作成
    the_jcd_dict = boatrace_crawler_conf.make_jcd_dict()
    the_jcd_list = list(the_jcd_dict.keys())

    # レース結果を読み込みdfとして保持
    the_race_results_df = load_raceResults_as_a_df()
    print(the_race_results_df)

    # main
    simulation_result_df_list_3t = []
    simulation_result_df_list_2t = []
    for the_rno, the_jcd in itertools.product(the_rno_list, the_jcd_list):
        # try-except IndexErrorはそんなレースない時。
        try:

            the_filtered_df_list_racer_frame = raceResult_filter.raceResult_filter(the_race_results_df,
                                                                 the_rno, the_jcd, the_hd)

            # ２レース以下しか走っていない選手がいた場合、シミュレーションの不確実性が著しく高まるためそのレースはパスする
            if any([(len(filtered_df_racer_frame) < 3) for filtered_df_racer_frame in the_filtered_df_list_racer_frame]):
                print("{0}の{1}は過去のレース数3レース以下の選手がいるためスキップ".format(the_jcd, the_rno))

            else:
                the_number_3t, the_counts_3t, the_number_2t, the_counts_2t, = simulate_a_race(the_filtered_df_list_racer_frame, the_num_simulation)

                simulation_result_list_3t = [[" " + tn3t for tn3t in list(the_number_3t)],
                                             [the_count_3t/the_num_simulation for the_count_3t in the_counts_3t]]
                simulation_result_list_2t = [[" " + tn2t for tn2t in list(the_number_2t)],
                                             [the_count_2t / the_num_simulation for the_count_2t in the_counts_2t]]

                this_simulation_result_df_3t = pd.DataFrame(list(zip(*simulation_result_list_3t)), columns=["組番", "くる率"])
                this_simulation_result_df_2t = pd.DataFrame(list(zip(*simulation_result_list_2t)), columns=["組番", "くる率"])
                this_simulation_result_df_3t["レース"] = the_rno
                this_simulation_result_df_3t["レース場"] = the_jcd
                this_simulation_result_df_3t["日付"] = the_hd
                this_simulation_result_df_2t["レース"] = the_rno
                this_simulation_result_df_2t["レース場"] = the_jcd
                this_simulation_result_df_2t["日付"] = the_hd

                simulation_result_df_list_3t.append(this_simulation_result_df_3t)
                simulation_result_df_list_2t.append(this_simulation_result_df_2t)
                # print(simulation_result_df_list)

        except IndexError:
            pass

    simulation_result_df_3t = pd.concat(simulation_result_df_list_3t)
    simulation_result_df_2t = pd.concat(simulation_result_df_list_2t)

    # csv書きだし
    simulation_result_file_3t = summarizer_motorboat_data_filename.make_csv_simulation_results2(the_hd, "3t")
    simulation_result_file_2t = summarizer_motorboat_data_filename.make_csv_simulation_results2(the_hd, "2t")

    simulation_result_df_3t.to_csv(simulation_result_file_3t, index=False)
    simulation_result_df_2t.to_csv(simulation_result_file_2t, index=False)

    # 棒グラフで表示
    #plt.bar(the_number, the_counts)
    # plt.show()

