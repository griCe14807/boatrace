# -*- coding=utf8 =*-
import pandas as pd
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))
sys.path.append(os.path.join(current_dir, '../crawl/'))

# my module
import summarizer_motorboat_data_filename


def make_df_of_all_days(the_boatrace_odds_path, the_sumulation_result_path):
    """
    読み込み先フォルダ内のファイルを全てまとめる場合

    :param the_boatrace_odds_path:
    :param the_sumulation_result_path:
    :return:
    """
    the_boatrace_odds_files = os.listdir(the_boatrace_odds_path)
    the_simulation_result_files = os.listdir(the_sumulation_result_path)

    # レース結果, odds, シミュレーション結果をそれぞれdfに変換
    the_odds_summary_df = pd.concat([pd.read_csv(os.path.join(the_boatrace_odds_path, the_boatrace_odds_file))
                                     for the_boatrace_odds_file in the_boatrace_odds_files
                                     if not os.path.isdir(the_boatrace_odds_file) and the_boatrace_odds_file[
                                                                                      -4:] == ".csv"])
    the_simulation_result_df = pd.concat(
        [pd.read_csv(os.path.join(the_sumulation_result_path, the_simulation_result_file))
         for the_simulation_result_file in the_simulation_result_files
         if not os.path.isdir(the_simulation_result_file) and the_simulation_result_file[-4:] == ".csv"])

    return the_odds_summary_df, the_simulation_result_df


def make_df_of_a_day_odds(input_date, how_to_bet):

    """
    日付を指定し、その日付のファイルに対してdfを作成
    :param input_date: 20190506のようなstr型で入力
    :return:

    """
    odds_summary_filename = input_date + "_odds" + how_to_bet + ".csv"
    boatrace_odds_path = summarizer_motorboat_data_filename.return_directory_path("odds") + how_to_bet + "/"
    odds_summary_file = os.path.join(boatrace_odds_path + odds_summary_filename)
    odds_summary_df = pd.read_csv(odds_summary_file)

    return odds_summary_df


def make_df_of_a_day_simulation_result(input_date, how_to_bet):
    # 3tは3tのまま、2tfがinputの時は2tという文字列に直したい
    how_to_bet = how_to_bet[:2]
    simulation_result_filename = input_date + "_" + how_to_bet + "_simulationResult.csv"
    simulation_result_path = summarizer_motorboat_data_filename.return_directory_path("simulationResults") + how_to_bet +"/"
    simulation_result_file = os.path.join(simulation_result_path + simulation_result_filename)
    simulation_result_df = pd.read_csv(simulation_result_file)

    return simulation_result_df


def main(input_date, how_to_bet):   # inputをoption化すること。
    """
    oddsのファイル、race resultのファイル、シミュレーション結果のファイルから、それらを統合した下記のcolumnを持つdfを作成。
    [レース番号など、組み番、オッズ、シミュレーションから求まった確率、実際のあたりor外れ]
    これが実際に解析するさいに用いるdfになる。このdfは日付ごとにcsvとして保存する

    """
    # 読み込み先のファイルを指定
    the_boatrace_odds_path = r"/Users/grice/mywork/boatrace/data/boatRace/results_odds/odds3t/"
    the_simulation_result_path = r"/Users/grice/mywork/boatrace/data/boatRace/simulation/simulation_results_csv/3t/"

    # TODO: ここはoptionで選択できるようにする
    the_odds_summary_df = make_df_of_a_day_odds(input_date, how_to_bet)
    the_simulation_result_df = make_df_of_a_day_simulation_result(input_date, how_to_bet)

    # oddsとシミュレーション結果のdfを結合
    for_analysis_df = pd.merge(the_odds_summary_df, the_simulation_result_df, on=["日付", "レース場", "レース", "組番"], how="left")

    # TODO: ここも現状では欠場がある時だけコメントアウトを外すようになっている
    # for_analysis_df["オッズ"][for_analysis_df["オッズ"] == "欠場"] = 0
    for_analysis_df["オッズ"] = for_analysis_df["オッズ"].astype(float)

    # 期待値カラムを作成
    for_analysis_df["期待値"] = for_analysis_df["オッズ"] * for_analysis_df["くる率"]

    return for_analysis_df

if __name__ == "__main__":
    the_input_date = "20190501"

    the_for_analysis_df = main(the_input_date)
    print(the_for_analysis_df)
