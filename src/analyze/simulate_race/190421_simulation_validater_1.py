# -*- coding=utf8 =*-
import itertools
import pandas as pd
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))
sys.path.append(os.path.join(current_dir, 'simulation/'))
# my module
import summarizer_motorboat_data_filename
import raceResult_filter
import simulate_race
import boatrace_crawler_conf
import argparse


"""
過去のデータを用いて、しミューレーションを回してオッズと考え合わせて賭けたとして、どのように賭けたら実際勝てるのか？？のシミュレーション
- 期待値+のところ全て
- 期待値+かつ確率20位以内
- 確率20位以内全て
"""

def argparser():
    """
    start_date = 2019/05/01
    end_date = 2019/05/02という指定で、2019年5月1日のシミュレーション結果が得られる
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start_date",
                        help=u"日時。'2919/05/01'のように、yyyy/mm/ddの形で指定",
                        required=True
                        )
    parser.add_argument("-e", "--end_date",
                        help=u"日時。'2019/05/01'のように、yyyy/mm/ddの形で指定",
                        required=True
                        )
    parser.add_argument("-vt", "--voting_threshold",
                        type=float,
                        help=u"期待値がこの値を超えた場合にbetする。1, 2など数字で指定。",
                        required=True
                        )
    args = parser.parse_args()

    return args



if __name__ == "__main__":

    ################inputs#################

    # simulationの試行回数
    simulation_time = 10000

    # argparser
    the_args = argparser()

    # betする期待値
    voting_threshold = the_args.voting_threshold

    # 指定した期日内で行われたレース全てをシミュレート
    the_date_from = "".join((the_args.start_date).split("/"))
    the_date_to = "".join((the_args.end_date).split("/"))

    # 読み込み先のファイルを指定
    the_race_results_file = summarizer_motorboat_data_filename.make_csv_race_results()
    the_boatrace_odds_file = summarizer_motorboat_data_filename.make_csv_odds()

    # 書きだし先のファイル指定
    the_simulation_result_file = summarizer_motorboat_data_filename.make_csv_simulation_results(the_date_from, the_date_to, voting_threshold)


    ###########

    # race noのリストを作成
    the_rno_list = [str(i + 1) + "R" for i in range(12)]
    # 会場のリスト作成
    the_jcd_dict = boatrace_crawler_conf.make_jcd_dict()
    the_jcd_list = list(the_jcd_dict.keys())
    # 日付のリスト作成
    the_hd_list = boatrace_crawler_conf.make_hd_list(the_date_from, the_date_to)
    # print(the_hd_list)

    # レース結果を読み込みdfとして保持
    the_race_results_df = raceResult_filter.load_data_into_df(the_race_results_file)
    # oddsに関してもdfにしておく
    the_odds_summary_df = pd.read_csv(the_boatrace_odds_file)

    # main
    simulation_result_list = []
    for the_hd in the_hd_list:
        for the_rno, the_jcd in itertools.product(the_rno_list, the_jcd_list):
            try:
                # 対象レースと同じ人・枠の過去データを抽出
                the_filtered_df_list_racer_frame = raceResult_filter.raceResult_filter(the_race_results_df,
                                                                                       the_rno, the_jcd, the_hd)
                # 組番tuple、その組番がくる確率tuple　を返す
                the_number_tuple, the_counts_tuple = simulate_race.simulate_a_race(the_filtered_df_list_racer_frame, simulation_time)

                # 期待値計算時に無駄なところを観に行く回数を少なくするため、ここでfilterをかけておく
                the_odds_summary_df_raceFiltered = raceResult_filter.filter_by_race(the_odds_summary_df, the_rno, the_jcd, the_hd)
                print(the_hd, the_jcd, the_rno)

                # 組番ごとの期待値を計算し、期待値1以上になるものはbet_listに追加する
                bet_dict = {}
                for i, the_number in enumerate(the_number_tuple):
                    # 期待値を計算
                    the_coming_rate = the_counts_tuple[i] / simulation_time
                    the_odds = the_odds_summary_df_raceFiltered[the_odds_summary_df_raceFiltered["組番"]==(" " + the_number)]["オッズ"].values[0]
                    if the_odds == "欠場":
                        print("欠場のためシミュレーションせず")
                        break

                    else:
                        the_odds = float(the_odds)
                        # print("組番 {0}: オッズ={1}".format(the_number, the_odds))
                        the_expected_value = the_coming_rate * the_odds

                        if the_expected_value > voting_threshold:
                            bet_dict[the_number] = the_odds

                # breakされなかった時の処理
                else:
                    # 実際のレース結果
                    result_number_series = raceResult_filter.filter_by_race(the_race_results_df, the_rno, the_jcd, the_hd)["枠"]
                    result_number_list = result_number_series.values.tolist()
                    result_number_triplicate = "-".join([str(result_number_list[i])[0] for i in range(3)])

                    # 実際のrefund rateを計算
                    cost = len(bet_dict)
                    return_ = bet_dict.get(result_number_triplicate, 0)
                    refund_rate = return_ - cost
                    print("収支={0}".format(refund_rate))

                    simulation_result_list.append([the_rno, the_jcd, the_hd, cost, return_, refund_rate])

            except IndexError:
                pass

    simulation_result_df = pd.DataFrame(simulation_result_list, columns=["レース", "レース場", "日付", "ベット数", "払い戻し", "収支"])
    simulation_result_df.to_csv(the_simulation_result_file, index=False)