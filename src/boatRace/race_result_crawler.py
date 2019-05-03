# -*- coding=utf8 =*-
import re
import pandas as pd
import itertools
import time
import boatrace_crawler_conf
import summarizer_motorboat_data_filename


def crawle_race_result(soup, cols, rno, jcd, hd):
    """
    soupをパースし, 順位、選手登録番号、枠番、線署名といった情報scrapeする
    cols, rno, jcd, hdというinputは、そのままoutputに入れるために入力値にしている（内部で計算なし）
    :param soup:
    :return race_result_list: [日付、レース場、レース、順位、枠番、登録番号、選手名、タイム]のリストを一位から6位までネストしたリスト
    """

    race_result_list = []
    table = soup.find(class_="grid_unit").find(class_="table1")
    rows = table.find_all("tbody")

    for i, row in enumerate(rows, 1):
        rank = i  # 順位
        frame = row.find("td", {"class": re.compile("is-fs14 is-fBold")}).text  # 枠番
        registration_number = row.find("span", {"class": "is-fs12"}).text  # 選手登録番号
        racer_name = row.find("span", {"class": "is-fs18 is-fBold"}).text  # 選手名
        race_time = row.find_all("td")[3].text
        # race_result_listの要素としてクロールした結果のリストを追加
        race_result_list.append([hd, jcd, rno, rank, frame, registration_number, racer_name, race_time])
    race_result_df = pd.DataFrame(race_result_list, columns=cols)

    return race_result_df


if __name__ == "__main__":

    #################### inputs ########################

    # もともとcsvファイルが存在する状態で回す必要があることに注意

    # crawl開始日付、終了日付の指定
    the_date_from = '20190428'
    the_date_to = '20190501'

    # output csvファイルの指定
    the_boatrace_results_file = summarizer_motorboat_data_filename.make_csv_race_results()
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

    # csvファイル内で定義されているcolumn名を書きだしておく
    the_cols = ["日付", "レース場", "レース", "着", "枠", "登録番号", "ボートレーサー", "レースタイム"]

    # 結果をまとめたcsvファイル（すでにある）をdfとして読み込み。
    the_race_result_df = pd.read_csv(the_boatrace_results_file)

    for the_hd in the_hd_list:
        for the_rno, the_jcd in itertools.product(the_rno_list, the_jcd_list):

            # 以下、crawl実行部分
            # クロール対象サイトのurl作成
            the_raceResult_url = boatrace_crawler_conf.make_url("raceresult", the_rno, the_jcd, the_hd)
            print(the_raceResult_url)

            # 存在しないraceをinputしてしまった時のためのtry-except
            try:
                # 対象サイトをパースしてcrawl
                the_soup = boatrace_crawler_conf.html_parser(the_raceResult_url)
                the_new_race_result_df = crawle_race_result(the_soup, the_cols, the_rno, the_jcd, the_hd)
                # dataframeをconcut
                the_race_result_df = pd.concat([the_race_result_df, the_new_race_result_df])

            except AttributeError:
                pass

            time.sleep(0.1)

        # 重複が残ったまま書きだし
        the_race_result_df.to_csv(the_boatrace_results_file, index=False)

        # 重複行を削除
        the_race_result_df = pd.read_csv(the_boatrace_results_file)
        the_race_result_df = the_race_result_df[~the_race_result_df.duplicated()]
        print(the_race_result_df)

        # 再度書きだし
        the_race_result_df.to_csv(the_boatrace_results_file, index=False)

