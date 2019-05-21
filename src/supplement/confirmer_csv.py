# -*- coding=utf8 =*-
import pandas as pd

import summarizer_motorboat_data_filename


if __name__ == "__main__":

    """
    RaceResultはcrawleしている
    """

    # レース結果のcsvファイルを読み込み
    the_raceResult_csv_file = summarizer_motorboat_data_filename.make_csv_race_results()
    the_raceResult_df = pd.read_csv(the_raceResult_csv_file)

    # odds csvも読み込む
    the_boatrace_odds_file = summarizer_motorboat_data_filename.make_csv_odds()
    the_odds_summary_df = pd.read_csv(the_boatrace_odds_file)

    # それぞれのdfの日付部分を取り出し、重複を削除
    crawled_days_raceResult_set = set(the_raceResult_df['日付'])
    crawled_days_odds_set = set(the_odds_summary_df['日付'])

    # raceResultはあるけど、oddsはない日付を書き出す
    intersection_days_set = crawled_days_raceResult_set & crawled_days_odds_set
    only_raceResult_days_set = crawled_days_raceResult_set - intersection_days_set
    only_odds_days_set = crawled_days_odds_set - intersection_days_set
    print("raceResultだけをcrawlしている日付は{0}".format(only_raceResult_days_set))
    print("oddsだけをcrawlしている日付は{0}".format(only_odds_days_set))