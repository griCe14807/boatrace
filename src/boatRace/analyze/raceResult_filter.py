# -*- coding=utf8 =*-
import sys
import pandas as pd

sys.path.append("../.")
# my module
import summarizer_motorboat_data_filename
import boatrace_crawler_conf


def raceResult_filter(race_results_df, rno, jcd, hd):
    """

    :param race_results_file:
    :param rno:
    :param jcd:
    :param hd:
    :return: 　要素数６のリスト。一つ一つの要素は、レース結果のうち、　[要素番号]+1の枠番の選手の、該当枠におけるレース結果を抽出したpandas.df

    """

    #  Filteringを行うためのレーサーネームをcrawle
    raceList_url = boatrace_crawler_conf.make_url("racelist", rno, jcd, hd)
    soup = boatrace_crawler_conf.html_parser(raceList_url)
    racer_list = crawle_race_list(soup)

    # plot用データを作成: racernameでfiltering
    filtered_df_list_racer = [filter_by_racername(race_results_df, racer) for racer in racer_list]

    # 枠番でのfilteringを追加
    filtered_df_list_racer_frame = []
    for i, filtered_df_racer in enumerate(filtered_df_list_racer, 1):
        filtered_df_racer_frame = filter_by_frame(filtered_df_racer, i)
        filtered_df_list_racer_frame.append(filtered_df_racer_frame)

    return filtered_df_list_racer_frame


def filter_by_race(input_df, rno, jcd, hd):
    """
    input dataframeのうち、rno, jcd, hdで指定した部分を返す。
    :param input_df:
    :param rno:
    :param jcd:
    :param hd:
    :return:
    """
    input_df_raceFiltered = input_df[(input_df["レース"]==rno) &
                              (input_df["レース場"]==jcd) & (input_df["日付"]==hd)]

    return input_df_raceFiltered


def crawle_race_list(soup):
    """
    soupから選手名をリストとして取得
    :return racer_list: 出場選手名を枠順に並べたリスト

    """

    racer_list = []
    table = soup.find(class_="contentsFrame1_inner").find_all(class_="table1")[1]
    rows = table.find_all("tbody", {"class": "is-fs12"})

    for row in rows:
        # 選手名を取得。最後の[1:-1]は改行を削除するため
        racer_name = row.find(class_="is-fs18 is-fBold").text[1:-1]
        # race_result_listの要素としてクロールした結果のリストを追加
        racer_list.append(racer_name)
    print(racer_list)

    return racer_list


def filter_by_racername(race_results_df, racername):
    filtered_df_racername = race_results_df[race_results_df["ボートレーサー"]==racername]

    return filtered_df_racername


def filter_by_frame(race_results_df, frame):
    filtered_df_frame = race_results_df[race_results_df["枠"]==frame]

    return filtered_df_frame



if __name__ == "__main__":

    """
    解析対象のレースに出場するracerおよびその枠ごとでこれまでのレース結果をfilteringし、結果を散布図にして表示
        
    """
    ################inputs#################

    the_rno = "12R"
    the_jcd = "下　関"
    the_hd = "2019/04/17"

    # 読み込み先のファイルを指定
    the_race_results_file = summarizer_motorboat_data_filename.make_csv_race_results()

    #######################################

    the_filtered_df_list_racer_frame = raceResult_filter(the_race_results_file,
                                                         the_rno, the_jcd, the_hd)
