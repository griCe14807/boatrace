# -*- coding=utf8 =*-
import pandas as pd
import itertools
import time
import sys
import os
current_dir = os.getcwd()
sys.path.append(os.path.join(current_dir, '../crawl/'))

# my module
import motor_and_boat_data_crawler
import boatrace_crawler_conf

if __name__ == "__main__":

    #################### inputs ########################

    # crawl開始日付、終了日付の指定
    the_date_from = '20190517'
    the_date_to = '20190601'

    ####################################################

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

            # クロール対象サイトのurl作成
            the_raceResult_url = boatrace_crawler_conf.make_url("racelist", the_rno, the_jcd, the_hd)
            print(the_raceResult_url)

            # 対象サイトをパース
            the_soup = boatrace_crawler_conf.html_parser(the_raceResult_url)

            try:    # 存在しないraceをinputしてしまった時のためのtry-except
                # crawl
                this_race_result_df = motor_and_boat_data_crawler.crawl_motor_data(the_soup, the_rno, the_jcd, the_hd)
                this_race_result_df_list.append(this_race_result_df)
                # print(this_race_result_df)

            except IndexError:
                pass

            time.sleep(1)

        # その日のraceResultを一つのdfにまとめる
        the_race_result_df = pd.concat(this_race_result_df_list)

        # output csvファイルの指定
        output_path = "/Users/grice/mywork/boatrace/data/motor_and_boat"
        the_output_filename = os.path.join(output_path, the_hd[2:4] + the_hd[5:7] + the_hd[8:10] + ".csv")
        print(the_output_filename)
        # 書きだし
        the_race_result_df.to_csv(the_output_filename, index=False)