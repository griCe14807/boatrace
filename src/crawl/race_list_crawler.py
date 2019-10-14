# -*- coding=utf8 =*-

import time
import pandas as pd
import re

# my module
import boatrace_crawler_conf

def crawl_race_information(soup, rno, jcd, hd):
    """
    モーターおよびボートのデータをcrawlし、csvとして保存
    :return:
    """
    race_result_dict = {"date": "-".join([hd[0:4], hd[5:7], hd[8:10]]),
                        "venue": jcd,
                        "raceNumber": rno[:-1]
                        }
    table = soup.find(class_="contentsFrame1_inner").find_all(class_="table1")[1]
    rows = table.find_all("tbody", {"class": "is-fs12"})

    for i, row in enumerate(rows, 1):
        # racer id
        race_result_dict["racer_id_{0}".format(i)] = row.find(class_="is-fs11").text.split("\n")[1][-6:-2]

        # 選手名。最後の[1:-1]は改行を削除するため
        racer_name = row.find(class_="is-fs18 is-fBold").text[1:-1]
        # racerの書式をダウンロードファイルに合わせる
        racer_ = racer_name.split("\u3000")

        # 苗字3文字名前3文字の場合
        if len(racer_[0])==6:
            racer = racer_[0][0:3] + "\u3000\u3000" + racer_[0][3:6]

        # 苗字の文字数を整える
        elif len(racer_[0]) == 1:
            racer_[0] = racer_[0] + "\u3000\u3000"
        elif len(racer_[0]) == 2:
            racer_[0] = racer_[0][0] + "\u3000" + racer_[0][1]

        # 名前の文字数を整える
        if len(racer_[-1]) == 1:
            racer_[-1] == "\u3000\u3000" + racer_[-1]
            racer = racer_[0] + "\u3000\u3000\u3000\u3000" + racer_[-1]
        elif len(racer_[-1]) == 2:
            racer_[-1] = racer_[-1][0] + "\u3000" + racer_[-1][1]
            racer = racer_[0] + "\u3000\u3000" + racer_[-1]
        elif len(racer_[-1]) == 3:
            racer = racer_[0] + "\u3000\u3000" + racer_[-1]

        # race_result_listの要素としてクロールした結果のリストを追加
        race_result_dict["racer_{0}".format(i)] = racer

        # racer data
        racer_column_3 = row.find_all("td", {"class": "is-lineH2"})[0].text.split("\n")
        race_result_dict["num_false_start_{0}".format(i)] = racer_column_3[1][-3:-1]
        race_result_dict["num_late_start_{0}".format(i)] = racer_column_3[2][-3:-1]
        race_result_dict["ave_start_time_{0}".format(i)] = racer_column_3[3][-5:-1]

        # racer data: win rate national
        national_win_rate_column = row.find_all("td", {"class": "is-lineH2"})[1].text.split("\n")
        race_result_dict["win_rate_national_{0}".format(i)] = national_win_rate_column[1][-6:-1]
        race_result_dict["place2Ratio_national_{0}".format(i)] = national_win_rate_column[2][-6:-1]
        race_result_dict["place3Ratio_national_{0}".format(i)] = national_win_rate_column[3][-6:-1]

        # racer data: win rate local
        local_win_rate_column = row.find_all("td", {"class": "is-lineH2"})[2].text.split("\n")
        race_result_dict["win_rate_local_{0}".format(i)] = local_win_rate_column[1][-6:-1]
        race_result_dict["place2Ratio_local_{0}".format(i)] = local_win_rate_column[2][-6:-1]
        race_result_dict["place3Ratio_local_{0}".format(i)] = local_win_rate_column[3][-6:-1]

        # crawl motor data
        motor_column = row.find_all("td", {"class": " is-lineH2"})[0].text.split("\n")
        race_result_dict["motorNo_{0}".format(i)] = motor_column[1][-4:-1]
        race_result_dict["motor_place2Ratio_{0}".format(i)] = motor_column[2][-7:-1]
        race_result_dict["motor_place3Ratio_{0}".format(i)] = motor_column[3][-7:-1]

        # crawl boat data
        boat_column = row.find_all("td", {"class": " is-lineH2"})[1].text.split("\n")
        race_result_dict["boatNo_{0}".format(i)] = boat_column[1][-4:-1]
        race_result_dict["boat_place2Ratio_{0}".format(i)] = boat_column[2][-7:-1]
        race_result_dict["boat_place3Ratio_{0}".format(i)] = boat_column[3][-7:-1]

        # crawl this championship results
        # x号艇, 初日1レースの着順...CS_rank_x_1, y号艇、3日目2レース目の着順...CS_rank_y_6 のように表記
        divided_rows = row.find_all("tr")
        CS_result_column_1 = divided_rows[0].find_all("td", {"class": re.compile("null")})
        CS_result_column_2 = divided_rows[1].find_all("td", {"class": re.compile("null")})
        CS_result_column_3 = divided_rows[2].find_all("td", {"class": re.compile("null")})
        CS_result_column_4 = divided_rows[3].find_all("td", {"class": re.compile("null")})

        for j, CS_result in enumerate(CS_result_column_1, 1):
            CS_result_class_name_ = CS_result.get("class")
            if len(CS_result_class_name_)==2:
                if CS_result_class_name_[1][-1] is not "l":
                    # frame
                    race_result_dict["CS_frame_{0}_{1}".format(i, j)] = CS_result.get("class")[1][-1]
                    # レース番号
                    race_result_dict["CS_race_{0}_{1}".format(i, j)] = CS_result.text
                    # cource
                    race_result_dict["CS_cource_{0}_{1}".format(i, j)] = CS_result_column_2[j-1].text
                    # start time
                    race_result_dict["CS_ST_{0}_{1}".format(i, j)] = CS_result_column_3[j-1].text
                    # 順位
                    race_result_dict["CS_rank_{0}_{1}".format(i, j)] = CS_result_column_4[j-1].text
                    """
                    print(race_result_dict["CS_frame_{0}_{1}".format(i, j)],
                          race_result_dict["CS_race_{0}_{1}".format(i, j)],
                          race_result_dict["CS_cource_{0}_{1}".format(i, j)],
                          race_result_dict["CS_ST_{0}_{1}".format(i, j)],
                          race_result_dict["CS_rank_{0}_{1}".format(i, j)]
                          )
                    """

                else:
                    pass
            else:
                pass


    # dictをdfに変換
    race_result_df = pd.io.json.json_normalize([race_result_dict])
    # print(race_result_df[["boatNo_1", "boat_place2Ratio_4", "motor_place3Ratio_5"]])

    time.sleep(0.1)

    return race_result_df


def main(rno, jcd, hd):
    """
    :param rno:
    :param jcd:
    :param hd:
    :return:
    """
    # クロール対象サイトのurl作成
    raceResult_url = boatrace_crawler_conf.make_url("racelist", rno, jcd, hd)
    print(raceResult_url)
    soup = boatrace_crawler_conf.html_parser(raceResult_url)

    # 存在しないraceをinputしてしまった時のためのtry-except
    try:
        # 対象サイトをパースしてcrawl
        race_information_df = crawl_race_information(soup, rno, jcd, hd)
        race_information_df = race_information_df.set_index(["date", "venue", "raceNumber"])
        return race_information_df

    except IndexError:
        return None

    # connectionResetErrorとかが起った場合、soupでNoneが返されてここでAttributeError
    except AttributeError:
        return None




if __name__ == "__main__":

    the_rno = "1R"
    the_jcd = "浜名湖"
    the_hd = "2019/01/01"

    the_race_information_df = main(the_rno, the_jcd, the_hd)
    print(the_race_information_df)
