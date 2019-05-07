# -*- coding=utf8 =*-
import matplotlib.pyplot as plt
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))
sys.path.append(os.path.join(current_dir, '../crawl/'))

# my module
import summarizer_motorboat_data_filename
import raceResult_filter
import make_figure
import simulate_race
import motorboat_odds_crawler
import calc_refund_rate

if __name__ == "__main__":

    """
    - これまでの結果を散布図としてプロットする
    - 10000回のレースシミュレーションを行い、どの組みがどの程度の割合できそうかを棒グラフで表示
    
    """

    ################inputs#################

    # 読み込み先のファイルを指定
    the_race_results_file = summarizer_motorboat_data_filename.make_csv_race_results()

    the_rno = "12R"
    the_jcd = "蒲　郡"
    the_hd = "2019/05/07"

    # simulationの試行回数
    the_num_simulation = 10000
    # betする組番の基準
    the_odds_threshold = 2
    the_coming_rate_threshold = 0.03

    #######################################
    # 対象レースと同じ人・枠の過去データを抽出
    the_race_results_df = raceResult_filter.load_data_into_df(the_race_results_file)
    the_filtered_df_list_racer_frame = raceResult_filter.raceResult_filter(the_race_results_df,
                                                                           the_rno, the_jcd, the_hd)
    # 過去のデータを用いてシミュレート
    the_number_tuple, the_counts_tuple, num_2t, count_2t = simulate_race.simulate_a_race(the_filtered_df_list_racer_frame, the_num_simulation)

    # 現在のオッズをcrawleし、結果をdfに格納して返す
    the_odds_df = motorboat_odds_crawler.main(the_rno, the_jcd, the_hd, "odds3t")

    # 組番ごとの期待値を計算し、期待値が1を超えるものはbetするリスト（good_list)に追加
    the_expected_value_list, the_good_list = calc_refund_rate.calc_expect_value_of_each_number(the_number_tuple,
                                                                                               the_counts_tuple,
                                                                                               the_odds_df,
                                                                                               the_num_simulation,
                                                                                               the_odds_threshold,
                                                                                               the_coming_rate_threshold
                                                                                               )
    print(the_good_list)

    # 散布図を作成
    make_figure.plot_result_on_single_figure(the_filtered_df_list_racer_frame)
    # 組番 vs くる率の棒グラフを作成
    fig2 = plt.figure(2)
    ax = fig2.add_subplot(1, 1, 1)
    ax.bar(the_number_tuple, the_counts_tuple)
    # 組番 vs 期待値の棒グラフを作成
    fig3 = plt.figure(3)
    ax_3 = fig3.add_subplot(1, 1, 1)
    ax_3.bar(the_number_tuple, the_expected_value_list)


    plt.show()

    # figureに名前をつけて保存
    # filename_scatterPlot = "_".join(["".join(the_hd.split("/")), the_rno, the_jcd, "frameFiltered"])