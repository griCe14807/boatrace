# -*- coding=utf8 =*-

import time
import pandas as pd

# my module
import boatrace_crawler_conf

def crawl_beforeinfo(soup, rno, jcd, hd):
    """
    モーターおよびボートのデータをcrawl
    :return:
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

        # TODO: プロペラ
        # TODO: 部品交換
        # TODO: 前走成績
        # TODO: 調整重量 (adjustment weight) (kg)
        # TODO: 水面気象情報

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


def main(rno, jcd, hd):
    """
    :param rno:
    :param jcd:
    :param hd:
    :return:
    """
    # クロール対象サイトのurl作成
    raceResult_url = boatrace_crawler_conf.make_url("beforeinfo", rno, jcd, hd)
    print(raceResult_url)

    # パース
    soup = boatrace_crawler_conf.html_parser(raceResult_url)

    # 存在しないraceをinputしてしまった時のためのtry-except
    try:
        # 対象サイトをパースしてcrawl
        race_information_df = crawl_beforeinfo(soup, rno, jcd, hd)
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

    the_beforeinfo_df = main(the_rno, the_jcd, the_hd)

    print(the_beforeinfo_df)
