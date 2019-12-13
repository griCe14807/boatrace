# -*- coding=utf8 =*-

import time
import pandas as pd
import re

# my module
import boatrace_crawler_conf


def scrape_racelist(soup, rno, jcd, hd):
    """
    racelistのページに書かれている情報をクロール
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


def scrape_beforeinfo(soup, rno, jcd, hd):
    """
    exhibitionの情報など、直前情報ページに書かれている情報をクロール
    :param soup:
    :param rno:
    :param jcd:
    :param hd:
    :return:

    # TODO: プロペラ
    # TODO: 部品交換
    # TODO: 前走成績
    # TODO: 調整重量 (adjustment weight) (kg)
    # TODO: 風向き

    """
    race_result_dict = {"date": "-".join([hd[0:4], hd[5:7], hd[8:10]]),
                        "venue": jcd,
                        "raceNumber": rno[:-1]
                        }
    table = soup.find(class_="contentsFrame1_inner").find_all(class_="table1")[1]
    rows = table.find_all("tbody", {"class": "is-fs12"})

    for i, row in enumerate(rows, 1):
        # 選手名。最後の[1:-1]は改行を削除するため
        racer_name = row.find(class_="is-fs18 is-fBold").text
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

        # racer weight (kg)
        # 書いていないことがあり、その場合エラーになる
        race_result_dict["weight_{0}".format(i)] = row.find("td", {"rowspan": "2"}).text[:-2]

        # 展示タイム
        race_result_dict["exhibitionTime_{0}".format(i)] = row.find_all("td", {"rowspan": "4"})[3].text

        # チルト角度
        race_result_dict["tilt_{0}".format(i)] = row.find_all("td", {"rowspan": "4"})[4].text

    table2 = soup.find(class_="contentsFrame1_inner").find_all(class_="table1")[2]
    rows2 = table2.find_all("tr")

    for i, row2 in enumerate(rows2[2:], 1):
        # 展示競争での進入コース
        race_result_dict["exhibition_cource_{0}".format(i)] = row2.find_all("span")[0].text
        # 展示start time (ST, flyng, late)
        ex_st_ = row2.find_all("span")[3].text
        if len(ex_st_) == 3:
            race_result_dict["exhibition_ST_{0}".format(i)] = ex_st_
            race_result_dict["flying_{0}".format(i)] = 0
            race_result_dict["late_{0}".format(i)] = 0

        elif len(ex_st_) == 4:
            race_result_dict["exhibition_ST_{0}".format(i)] = ex_st_[1:]
            if ex_st_[0] == "F":
                race_result_dict["flying_{0}".format(i)] = 1
                race_result_dict["late_{0}".format(i)] = 0
            # elif ex_st_[0] == "L":
            #     race_result_dict["late_{0}".format(i)] = 1
            else:
                raise Exception("{0}号艇ex_stが予定外（{1}）".format(i, ex_st_))
        elif len(ex_st_) == 1:
            if ex_st_[0] == "L":
                race_result_dict["exhibition_ST_{0}".format(i)] = None
                race_result_dict["late_{0}".format(i)] = 1
            else:
                raise Exception("{0}号艇ex_stが予定外（{1}）".format(i, ex_st_))

        else:
            raise Exception("{0}号艇ex_stが予定外（{1}）".format(i, ex_st_))

    # 水面気象情報
    table3 = soup.find(class_="contentsFrame1_inner").find(class_="weather1")
    weather_data = (table3.find_all(class_="weather1_bodyUnitLabelData"))
    weather_string = table3.find_all(class_="weather1_bodyUnitLabelTitle")

    race_result_dict["temperature"] = weather_data[0].text[:-1]
    race_result_dict["weather"] = weather_string[1].text
    race_result_dict["wind_speed"] = weather_data[1].text[:-1]
    race_result_dict["water_temperature"] = weather_data[2].text[:-1]
    race_result_dict["wave_height"] = weather_data[3].text[:-2]

    # dictの値でfloatにできるものはしておく
    float_key_list = ["weight_{0}".format(i), "exhibitionTime_{0}".format(i), "tilt_{0}".format(i),
                       "exhibition_cource_{0}".format(i), "exhibition_ST_{0}".format(i)]
    for i in range(1, 7):
        for key in float_key_list:
            try:
                race_result_dict[key] = float(race_result_dict[key])
            except ValueError:
                race_result_dict[key] = None
                print("{0}はfloatにできず".format(key))
            except TypeError:
                race_result_dict[key] = None
                print("{0}はfloatにできず".format(key))

    # dictをdfに変換
    beforeinfo_df = pd.io.json.json_normalize([race_result_dict])

    time.sleep(0.1)

    return beforeinfo_df


def scrape_odds_trifecta(soup, rno, jcd, hd):
    """
    3連単のオッズをクロール
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
    
    odds_dict = {"date": "-".join([hd[0:4], hd[5:7], hd[8:10]]),
                 "venue": jcd,
                 "raceNumber": rno[:-1]
                 }

    #place bed (勝式)
    odds_dict["placeBed"] = "trifecta"

    # make results_odds list
    contentsFrame1_inner = soup.find(class_="contentsFrame1_inner")
    odds_table = contentsFrame1_inner.find_all(class_="table1")[1].find(class_="is-p3-0")
    odds_list_soup = odds_table.find_all(class_="oddsPoint")
    for i, odds in enumerate(odds_list_soup):
        odds_dict[set_number_list[i]] = odds.text

    # dictをdfに変換
    odds_df = pd.io.json.json_normalize([odds_dict])

    return odds_df


def scrape_odds_exacta(soup, rno, jcd, hd):
    """

    TODO: 2連複のデータもcrawlする

    :param soup:
    :return place_bed: 勝式：三連単
    :return odds_list: [投票番号, 最終オッズ]のリストを全組み合わせについて格納したリスト
    
    """
    
    odds_dict = {"date": "-".join([hd[0:4], hd[5:7], hd[8:10]]),
             "venue": jcd,
             "raceNumber": rno[:-1]
             }

    set_number_list = [" 1-2", " 2-1", " 3-1", " 4-1", " 5-1", " 6-1",
                       " 1-3", " 2-3", " 3-2", " 4-2", " 5-2", " 6-2",
                       " 1-4", " 2-4", " 3-4", " 4-3", " 5-3", " 6-3",
                       " 1-5", " 2-5", " 3-5", " 4-5", " 5-4", " 6-4",
                       " 1-6", " 2-6", " 3-6", " 4-6", " 5-6", " 6-5",
                       ]

    #place bed (勝式)
    odds_dict["placeBed"] = "exacta"

    # make results_odds list
    contentsFrame1_inner = soup.find(class_="contentsFrame1_inner")
    odds_table = contentsFrame1_inner.find_all(class_="table1")[1].find(class_="is-p3-0")
    odds_list_soup = odds_table.find_all(class_="oddsPoint")
    for i, odds in enumerate(odds_list_soup):
        odds_dict[set_number_list[i]] = odds.text

    # dictをdfに変換
    odds_df = pd.io.json.json_normalize([odds_dict])

    return odds_df


def get_extractor(crawl_key):
    
    """
    クロール先に応じたcrawlerを用意
    
    """
    
    extractor_dict = {"racelist": scrape_racelist,
                      "beforeinfo": scrape_beforeinfo,
                      "odds3t": scrape_odds_trifecta,
                      "odds2tf": scrape_odds_exacta
                      }
    
    return extractor_dict[crawl_key]



def main(rno, jcd, hd, crawl_key):
    """
    :param rno:
    :param jcd:
    :param hd:
    :param hd:
    :return:
    """
    # クロール対象サイトのurl作成
    raceResult_url = boatrace_crawler_conf.make_url(crawl_key, rno, jcd, hd)
    print(raceResult_url)

    # パース
    soup = boatrace_crawler_conf.html_parser(raceResult_url)
    
    # extractorの指定
    the_extractor = get_extractor(crawl_key)

    # 存在しないraceをinputしてしまった時のためのtry-except
    try:
        # 対象サイトをcrawl
        race_information_df = the_extractor(soup, rno, jcd, hd)
        race_information_df = race_information_df.set_index(["date", "venue", "raceNumber"])
        return race_information_df

    except IndexError:
        return None

    # connectionResetErrorとかが起った場合、soupでNoneが返されてここでAttributeError
    except AttributeError:
        return None


if __name__ == "__main__":

    # pandas print時に省略しない設定
    pd.set_option('display.max_columns', 40)

    the_rno = "11R"
    the_jcd = "住之江"
    the_hd = "2019/10/06"
    crawl_key = "beforeinfo"
    """
    crawle_key: "racelist", "beforeinfo", "odds3t", "odds2tf"
    
    """

    the_beforeinfo_df = main(the_rno, the_jcd, the_hd, crawl_key)

    print(the_beforeinfo_df)
