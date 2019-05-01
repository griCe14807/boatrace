# -*- coding=utf8 =*-
import sys
import numpy as np
import collections
import matplotlib.pyplot as plt
sys.path.append("../.")

# my module
import summarizer_motorboat_data_filename
import raceResult_filter



def simulate_a_race(filtered_df_list, simulation_times):
    # TODO: 70秒台のレース結果（多分二周）はfilteringをかけといた方がいい

    simulation_result_list = []
    for i in range(simulation_times):
        picked_racetime_array = np.array([])   # 1枠から6枠までの選手の、これまでのレースタイムをランダムにピック
        for filtered_df in filtered_df_list:
            random_picked_racetime = filtered_df.sample()["racetime_float"]
            picked_racetime_array = np.append(picked_racetime_array, random_picked_racetime)

        # 着順を 1-2-3-4-5-6 のようなstrとして取得
        order_of_arrival_array = np.argsort(picked_racetime_array) + 1
        # 三着までの結果しかいらないので4着以下はここで切る（一個上で切ってももちろんOK)
        order_of_arrival_list = [str(element) for element in order_of_arrival_array][:3]
        order_of_arrival_str = "-".join(order_of_arrival_list)

        simulation_result_list.append(order_of_arrival_str)

    # simulation_result_listの各要素数をカウント
    c = collections.Counter(simulation_result_list)
    # print(c)
    number, counts = zip(*c.most_common(20))

    return number, counts



if __name__ == "__main__":
    ################inputs#################

    the_rno = "10R"
    the_jcd = "大　村"
    the_hd = "2019/04/19"

    # 読み込み先のファイルを指定
    the_race_results_file = summarizer_motorboat_data_filename.make_csv_race_results()

    #######################################

    the_filtered_df_list_racer_frame = raceResult_filter.raceResult_filter(the_race_results_file,
                                                         the_rno, the_jcd, the_hd)

    the_number, the_counts = simulate_a_race(the_filtered_df_list_racer_frame, 100)


    # 棒グラフで表示
    plt.bar(the_number, the_counts)
    plt.show()

