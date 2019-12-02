# -*- coding=utf8 =*-
import pandas as pd
import itertools
import time
import sys
import os
import argparse

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../crawl/'))

# my module
import boatrace_crawler
import boatrace_crawler_conf


def argparser():

    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--crawl_key",
                        help=u"何をcrawlするか. 'racelist' or 'beforeinfo'で指定",
                        required=True
                        )
    parser.add_argument("-s", "--start_date",
                        help=u"'20190102'のように6桁の数字で指定",
                        required=True
                        )
    parser.add_argument("-e", "--end_date",
                        help=u"'20190102'のように6桁の数字で指定. 指定した日付の前日までがクロール対象",
                        required=True
                        )
    args = parser.parse_args()

    return args


if __name__ == "__main__":

    # crawl開始日付、終了日付, クロール先、出力先の指定
    the_args = argparser()
    crawl_key = the_args.crawl_key
    the_date_from = the_args.start_date
    the_date_to = the_args.end_date
    the_output_path = output_path = os.path.join('../../data', crawl_key)

    # 以下で定義する全てのリストの要素の組み合わせについてcrawlを行う.
    # race noのリスト
    the_rno_list = [str(i + 1) + "R" for i in range(12)]
    # 会場のリスト
    the_jcd_dict = boatrace_crawler_conf.make_jcd_dict()
    the_jcd_list = list(the_jcd_dict.keys())
    # 日付のリスト
    the_hd_list = boatrace_crawler_conf.make_hd_list(the_date_from, the_date_to)
    print(the_hd_list)

    for the_hd in the_hd_list:
        this_race_result_df_list = []
        for the_rno, the_jcd in itertools.product(the_rno_list, the_jcd_list):

            # crawl
            this_race_result_df = boatrace_crawler.main(the_rno, the_jcd, the_hd, crawl_key)
            this_race_result_df_list.append(this_race_result_df)

            time.sleep(1)

        # その日のraceResultを一つのdfにまとめる
        the_race_result_df = pd.concat(this_race_result_df_list)

        # output csvファイルの指定
        output_path = os.path.join(current_dir, the_output_path)
        the_output_filename = os.path.join(output_path, the_hd[2:4] + the_hd[5:7] + the_hd[8:10] + ".csv")
        print(the_output_filename)
        # 書きだし
        the_race_result_df.to_csv(the_output_filename, index=True)