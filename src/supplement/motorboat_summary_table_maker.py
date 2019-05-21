# -*- coding=utf8 =*-
import pandas as pd
import summarizer_motorboat_data_filename

if __name__ == "__main__":
    # voterace_oddsのcsv file name作成
    the_boatrace_odds_file = motorboat_parameter.make_csv_odds()

    # voting resultのリスト（中は一つ一つcsv file name）
    the_voting_csv_file_list = summarizer_motorboat_data_filename.make_csv_voting_result()

    # output csv指定
    the_for_analysis_csv_file = summarizer_motorboat_data_filename.make_csv_for_analysis()

    # dataframeに格納し、マージ
    odds_summary_df = pd.read_csv(the_boatrace_odds_file)
    summary_df = odds_summary_df
    for whose_data in the_voting_csv_file_list:
        voting_result_df = pd.read_csv(whose_data, encoding="shift-jis")
        summary_df = pd.merge(summary_df, voting_result_df, how="left", on=["日付", "レース場", "レース", "勝式", "組番"])

    print(summary_df)

    # csv書きだし
    summary_df.to_csv(the_for_analysis_csv_file, index=False)