# -*- coding=utf8 =*-

import pandas as pd
import time
import itertools
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../conf/'))

# my module
import boatrace_crawler_conf
import summarizer_motorboat_data_filename


def extract_from_trifecta(soup):
    """

    :param soup:
    :return place_bed: 勝式：三連単
    :return odds_list: [投票番号, 最終オッズ]のリストを全組み合わせについて格納したリスト
    """

    set_number_list = [" 1-2-3", " 2-1-3", " 3-1-2", " 4-1-2", " 5-1-2", " 6-1-2",
                       " 1-2-4", " 2-1-4", " 3-1-4", " 4-1-3", " 5-1-3", " 6-1-3",
                       " 1-2-5", " 2-1-5", " 3-1-5", " 4-1-5", " 5-1-4", " 6-1-4",
                       " 1-2-6", " 2-1-6", " 3-1-6", " 4-1-6", " 5-1-6", " 6-1-5",
                       " 1-3-2", " 2-3-1", " 3-2-1", " 4-2-1", " 5-2-1", " 6-2-1",
                       " 1-3-4", " 2-3-4", " 3-2-4", " 4-2-3", " 5-2-3", " 6-2-3",
                       " 1-3-5", " 2-3-5", " 3-2-5", " 4-2-5", " 5-2-4", " 6-2-4",
                       " 1-3-6", " 2-3-6", " 3-2-6", " 4-2-6", " 5-2-6", " 6-2-5",
                       " 1-4-2", " 2-4-1", " 3-4-1", " 4-3-1", " 5-3-1", " 6-3-1",
                       " 1-4-3", " 2-4-3", " 3-4-2", " 4-3-2", " 5-3-2", " 6-3-2",
                       " 1-4-5", " 2-4-5", " 3-4-5", " 4-3-5", " 5-3-4", " 6-3-4",
                       " 1-4-6", " 2-4-6", " 3-4-6", " 4-3-6", " 5-3-6", " 6-3-5",
                       " 1-5-2", " 2-5-1", " 3-5-1", " 4-5-1", " 5-4-1", " 6-4-1",
                       " 1-5-3", " 2-5-3", " 3-5-2", " 4-5-2", " 5-4-2", " 6-4-2",
                       " 1-5-4", " 2-5-4", " 3-5-4", " 4-5-3", " 5-4-3", " 6-4-3",
                       " 1-5-6", " 2-5-6", " 3-5-6", " 4-5-6", " 5-4-6", " 6-4-5",
                       " 1-6-2", " 2-6-1", " 3-6-1", " 4-6-1", " 5-6-1", " 6-5-1",
                       " 1-6-3", " 2-6-3", " 3-6-2", " 4-6-2", " 5-6-2", " 6-5-2",
                       " 1-6-4", " 2-6-4", " 3-6-4", " 4-6-3", " 5-6-3", " 6-5-3",
                       " 1-6-5", " 2-6-5", " 3-6-5", " 4-6-5", " 5-6-4", " 6-5-4",
                       ]

    #place bed (勝式)
    place_bed = "３連単"

    # make results_odds list
    odds_list = []
    contentsFrame1_inner = soup.find(class_="contentsFrame1_inner")
    odds_table = contentsFrame1_inner.find_all(class_="table1")[1].find(class_="is-p3-0")
    odds_list_soup = odds_table.find_all(class_="oddsPoint")
    for i, odds in enumerate(odds_list_soup):
        odds_list.append([set_number_list[i], odds.text])

    return place_bed, odds_list



def extract_from_exacta(soup):
    """

    :param soup:
    :return place_bed: 勝式：三連単
    :return odds_list: [投票番号, 最終オッズ]のリストを全組み合わせについて格納したリスト
    """

    set_number_list = [" 1-2", " 2-1", " 3-1", " 4-1", " 5-1", " 6-1",
                       " 1-3", " 2-3", " 3-2", " 4-2", " 5-2", " 6-2",
                       " 1-4", " 2-4", " 3-4", " 4-3", " 5-3", " 6-3",
                       " 1-5", " 2-5", " 3-5", " 4-5", " 5-4", " 6-4",
                       " 1-6", " 2-6", " 3-6", " 4-6", " 5-6", " 6-5",
                       ]

    #place bed (勝式)
    place_bed = "2連単"

    # make results_odds list
    odds_list = []
    contentsFrame1_inner = soup.find(class_="contentsFrame1_inner")
    odds_table = contentsFrame1_inner.find_all(class_="table1")[1].find(class_="is-p3-0")
    odds_list_soup = odds_table.find_all(class_="oddsPoint")
    for i, odds in enumerate(odds_list_soup):
        odds_list.append([set_number_list[i], odds.text])

    return place_bed, odds_list


def extract_raceresults(rno, jcd, hd):
    raceResult_url = boatrace_crawler_conf.make_url("raceresult", rno, jcd, hd)

    # 対象サイトをパースしてcrawl
    the_soup = boatrace_crawler_conf.html_parser(raceResult_url)
    tr = the_soup.find("tr", {"class": "is-p6-0"}).find(class_="numberSet1_row")
    result_trrifecta = " " + "".join([element.text for element in tr.find_all("span")])

    return result_trrifecta


def convert_into_dataframe(hd, jcd, rno, place_bed, odds_list):
    """
    :param hd: 開催日
    :param jcd: 開催場所
    :param rno: レースNo
    :param place_bed: 勝式
    :param odds_list: 番号と最終オッズのリスト
    :param output_csv_file: 書きだし先csvファイル

    """

    # crawlしたデータをformat
    new_odds_list = []
    head_list = [hd, jcd, rno, place_bed]
    for odds in odds_list:
        odds[0:0] = head_list
        new_odds_list.append(odds)

    # 新しく取得したデータをdfに変換
    culumn_list = ["日付", "レース場", "レース", "勝式", "組番", "オッズ"]
    new_odds_df = pd.DataFrame(new_odds_list, columns=culumn_list)

    return new_odds_df

def get_extractor():

    return {"odds3t": {"extractor": extract_from_trifecta},
            "odds2tf": {"extractor": extract_from_exacta}
            }


def main(rno, jcd, hd, how_to_bet):
    # クロール対象サイトのurl作成
    odds_url = boatrace_crawler_conf.make_url(how_to_bet, rno, jcd, hd)
    print(odds_url)

    # 対象サイトをパースしてcrawl
    soup = boatrace_crawler_conf.html_parser(odds_url)
    the_extractor = get_extractor()[how_to_bet]["extractor"]
    place_bed, odds_list = the_extractor(soup)

    # dataframeとして格納
    new_odds_summary_df = convert_into_dataframe(hd, jcd, rno, place_bed, odds_list)
    print(new_odds_summary_df)

    return new_odds_summary_df



if __name__ == "__main__":

    #### input 指定した期日に行われたレースをcrawle ######


    the_hd = '2019/05/16'
    # how_to_betは "odds3t" もしくは　"odds2tf"
    how_to_bet = "odds3t"

    # race noのリスト
    the_rno_list = [str(i + 1) + "R" for i in range(12)]
    # 会場のリスト
    the_jcd_dict = boatrace_crawler_conf.make_jcd_dict()
    the_jcd_list = list(the_jcd_dict.keys())
    # print(the_hd_list)

    ###########


    # main
    the_odds_summary_df_list = []
    for the_rno, the_jcd in itertools.product(the_rno_list, the_jcd_list):
        try:
            this_odds_summary_df = main(the_rno, the_jcd, the_hd, how_to_bet)

            # 3連単的中番号
            the_result_number = extract_raceresults(the_rno, the_jcd, the_hd)
            # 2連単的中番号
            if how_to_bet == "odds2tf":
                the_result_number = the_result_number[:-2]
            print("的中番号は{0}".format(the_result_number))

            # 的中カラムを作成。的中は1, 外れは0
            this_odds_summary_df["的中"] = this_odds_summary_df["組番"] == the_result_number

            the_odds_summary_df_list.append(this_odds_summary_df)

        except IndexError:
            pass

        time.sleep(0.1)

    the_odds_summary_df = pd.concat(the_odds_summary_df_list)

    # 出力先のファイルを指定
    the_output_file = summarizer_motorboat_data_filename.make_csv_odds(the_hd, how_to_bet)

    # csv書きだし
    the_odds_summary_df.to_csv(the_output_file, index=False)
