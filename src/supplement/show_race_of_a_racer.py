# -*- coding=utf8 =*-

"""
新しい特徴量を生み出すことはせず、

"""

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../analyze/conf/'))
sys.path.append(os.path.join(current_dir, '../crawl/'))


# my module
import csv_loader
import boatrace_crawler_conf


if __name__ == "__main__":
    racer = "吉川\u3000\u3000元浩"
    # 過去のレース結果をdfとして取得
    the_raceresult_summary_df = csv_loader.load_all_raceResults_as_a_df()
    # plot用データを作成: racername+枠番でfiltering
    filtered_df = the_raceresult_summary_df[the_raceresult_summary_df["ボートレーサー_{0}".format(1)] == racer].sort_values("日付")
    print(filtered_df[["ボートレーサー_{0}".format(1), "日付", "レース場", "レース", "着_1", "スタートタイム_{0}".format(1), "着_2", "着_3"]])

