# -*- coding=utf8 =*-

import time
import pandas as pd

# my module
import boatrace_crawler_conf

def crawl_motor_data(soup, rno, jcd, hd):
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
        motor_column = row.find_all("td", {"class": " is-lineH2"})[0].text.split("\n")
        race_result_dict["motorNo_{0}".format(i)] = motor_column[1][-4:-1]
        race_result_dict["motor_place2Ratio_{0}".format(i)] = motor_column[2][-7:-1]
        race_result_dict["motor_place3Ratio_{0}".format(i)] = motor_column[3][-7:-1]

        boat_column = row.find_all("td", {"class": " is-lineH2"})[1].text.split("\n")
        race_result_dict["boatNo_{0}".format(i)] = boat_column[1][-4:-1]
        race_result_dict["boat_place2Ratio_{0}".format(i)] = boat_column[2][-7:-1]
        race_result_dict["boat_place3Ratio_{0}".format(i)] = boat_column[3][-7:-1]

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
        race_result_df = crawl_motor_data(soup, rno, jcd, hd)
        return race_result_df

    except AttributeError:
        return None



if __name__ == "__main__":

    the_rno = "1R"
    the_jcd = "浜名湖"
    the_hd = "2019/01/01"

    the_motor_and_boat_data_df = main(the_rno, the_jcd, the_hd)
    print(the_motor_and_boat_data_df)
