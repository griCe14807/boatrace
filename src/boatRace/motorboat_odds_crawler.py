# -*- coding=utf8 =*-

import pandas as pd
import glob
import time
import itertools
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


def convert_into_dataframe(hd, jcd, rno, place_bed, odds_list):
    """
    pandas dataframeとしてすでにあるデータを読み込み、マージして重複を削除
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


def main(rno, jcd, hd):
    # クロール対象サイトのurl作成
    odds_url = boatrace_crawler_conf.make_url("odds3t", rno, jcd, hd)
    print(odds_url)
    try:
        # 対象サイトをパースしてcrawl
        soup = boatrace_crawler_conf.html_parser(odds_url)
        place_bed, odds_list = extract_from_trifecta(soup)

        # dataframeとして格納
        new_odds_summary_df = convert_into_dataframe(hd, jcd, rno, place_bed, odds_list)

    except IndexError:
        new_odds_summary_df = pd.DataFrame()

    time.sleep(0.1)

    return new_odds_summary_df



if __name__ == "__main__":

    # input option 以下から選ぶ
    ##### input option 1: 自分がこれまで投票したレースについてcrawle #######
    """
    # 投票結果のcsvファイルから、どのレース結果が必要かを読み取る
    the_voting_csv_file_list = glob.glob(r"/Users/grice/mywork/Gambling/data/boatRace/results_voting/myDownload/not_yet/*")
    the_voting_df_list = [pd.read_csv(date_of_data, encoding="shift-jis") for date_of_data in the_voting_csv_file_list]
    the_voting_df = pd.concat(the_voting_df_list)

    for_input_df = the_voting_df.drop_duplicates(subset=['レース', 'レース場', '日付'])

    the_rno_list = []
    the_jcd_list = []
    the_hd_list = []

    for index, row in for_input_df.iterrows():
        rno = row['レース']
        jcd = row['レース場']
        hd = row['日付']

        the_rno_list.append(rno)
        the_jcd_list.append(jcd)
        the_hd_list.append(hd)
    """

    #### input option 2: 指定した期日内で行われたレースをcrawle ######

    the_date_from = '20190502'
    the_date_to = '20190503'
    # race noのリスト
    the_rno_list = [str(i + 1) + "R" for i in range(12)]
    # 会場のリスト
    the_jcd_dict = boatrace_crawler_conf.make_jcd_dict()
    the_jcd_list = list(the_jcd_dict.keys())
    # 日付のリスト
    the_hd_list = boatrace_crawler_conf.make_hd_list(the_date_from, the_date_to)
    # print(the_hd_list)

    ###########

    print(the_rno_list, the_jcd_list, the_hd_list)

    # 出力先のファイルを指定
    the_boatrace_odds_file = summarizer_motorboat_data_filename.make_csv_odds()
    # すでにあるデータをdataframeとして読み込み
    the_odds_summary_df = pd.read_csv(the_boatrace_odds_file)

    # main
    for the_hd in the_hd_list:
        for the_rno, the_jcd in itertools.product(the_rno_list, the_jcd_list):
            the_new_odds_summary_df = main(the_rno, the_jcd, the_hd)
            # 二つのdataframeをmerge
            the_odds_summary_df = the_odds_summary_df.append(the_new_odds_summary_df)

        # csv書きだし
        the_odds_summary_df.to_csv(the_boatrace_odds_file, index=False)

        # 再度csv読み込みし、重複行を削除（一気にやろうとするとなぜか2こだけ重複が残る）
        the_new_odds_summary_df = pd.read_csv(the_boatrace_odds_file)
        the_new_odds_summary_df = the_new_odds_summary_df[~the_new_odds_summary_df.duplicated()]
        print(the_new_odds_summary_df)

        # csv書きだし
        the_new_odds_summary_df.to_csv(the_boatrace_odds_file, index=False)