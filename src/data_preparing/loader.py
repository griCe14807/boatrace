"""How to use this script
(1) Download race result files by RaceResults.download()
(2) Manually extract text files from lzh files
(3) Move the text files to ./data directory
(4) RaceResults.load() will parse the text files
"""

import pandas as pd
import glob
import re
from datetime import datetime


def load():

    # loadした結果を格納するための辞書を作成（最後はpandas.DataFrameにします）
    race_result_dict = {"date": [],
                        "venue": [],
                        "raceNumber": [],
                        "weather": [],
                        "windDir": [],
                        "windPow": [],
                        "waveHight": [],
                        "ruler": [],
                        "win": [],
                        "winOdds": [],
                        "place_1": [],
                        "placeOdds_1": [],
                        "place_2": [],
                        "placeOdds_2": [],
                        "exacta": [],
                        "exactaOdds": [],
                        "quinella": [],
                        "quinellaOdds": [],
                        "wide_1": [],
                        "wideOdds_1": [],
                        "wide_2": [],
                        "wideOdds_2": [],
                        "wide_3": [],
                        "wideOdds_3": [],
                        "trifecta": [],
                        "trifectaOdds": [],
                        "trio": [],
                        "trioOdds": []
                        }
    for i in range(1, 7):
        race_result_dict["rank_{0}".format(i)] = []
        race_result_dict["racerId_{0}".format(i)] = []
        race_result_dict["racerName_{0}".format(i)] = []
        race_result_dict["motor_{0}".format(i)] = []
        race_result_dict["boat_{0}".format(i)] = []
        race_result_dict["exhibitionTime_{0}".format(i)] = []
        race_result_dict["exhibitionRank_{0}".format(i)] = []
        race_result_dict["startTime_{0}".format(i)] = []
        race_result_dict["raceTime_{0}".format(i)] = []

    # レース結果のテキストファイルを読み込み、辞書に格納していく
    for filename in glob.glob("/Users/grice/mywork/boatrace/data/results_race/K16*.TXT"):
        with open(filename, "r", encoding="shift_jis") as f:
            result_ = f.read()

            # 会場ごとの塊に分割
            result_ = re.split(r"[0-9][0-9]KBGN\n", result_)

            # 中身一つ一つを改行で分割
            result_ = [result_element.splitlines() for result_element in result_]

            # ファイル全体のhead（start）を削除
            result_ = result_[1:]

            for result_jcd in result_:
                # ヘッダ部分（会場名や払戻金のまとめなど）
                jcd_head = result_jcd[0:26]
                # 会場ごとに、parseしたい要素が集まったbody部分
                jcd_body = result_jcd[26:-2]

                # 会場ごとに取得
                jcd = jcd_head[0][0:3]  # 会場名
                hd = datetime.strptime(jcd_head[6][17:27].replace(" ", "0"), '%Y/%m/%d') # 日付 datetime型に

                # bodyをレースごとに分割
                for i in range(1, 13):
                    race_body = jcd_body[21 * (i-1): 21 * i]

                    # レースごとに取得その1: レースごとのヘッダ部分から取得
                    race_head = race_body[0]

                    race = int(race_head[2:4].replace(" ", ""))  # レース番号
                    ruler = race_body[1][50:53].replace(" ", "") # 決まり手

                    # 進入固定の場合位置が変わる
                    if race_head[20:24] == "進入固定":
                        weather = race_head[39]  # 天候
                        wind_dir = race_head[46:48]  # 風向
                        wind_power = int(race_head[50])  # 風速 (m)
                        wave = int(race_head[58])  # 波高 (cm)

                    else:
                        weather = race_head[43] # 天候
                        wind_dir = race_head[50:52] # 風向
                        wind_power = int(race_head[54])   # 風速
                        wave = int(race_head[62]) # 波高

                    # 選手情報を取得
                    racers_result = race_body[3:9]
                    for racer_result in racers_result:

                        # スタートタイム。flying, lateがあった場合はnoneを格納. これで多分転覆もexcept側に入ってる
                        # TODO 本当はそもそも解析用のdfに加えないようにしたい
                        try:
                            start_time = float(racer_result[43: 47])
                            rank = int(racer_result[2:4])  # 順位

                        except ValueError:
                            start_time = None
                            rank = 0

                        frame = racer_result[6] # 枠番
                        racer_id = racer_result[8:12]   # 選手登録番号
                        racer_name = racer_result[13:21]    # 名前
                        motor = racer_result[22:24] # モーター番号
                        boat = racer_result[27:29]  # ボート番号
                        exhibition_time = float(racer_result[31:35])   # 展示タイム
                        exhibition_rank = int(racer_result[38])  # 展示順位
                        # レースタイム
                        race_time = racer_result[52: 58].split(".")
                        if race_time[0] == " ": # 5着5着のタイムはない
                            race_time = None
                        else:
                            race_time = int(race_time[0]) * 60 + int(race_time[1]) + int(race_time[2]) / 100



                        # print(rank, frame, racer_id, racer_name, motor, boat, exhibition_time, exhibition_rank, start_time, race_time)

                        # 辞書に格納
                        race_result_dict["rank_{0}".format(frame)].append(rank)
                        race_result_dict["racerId_{0}".format(frame)].append(racer_id)
                        race_result_dict["racerName_{0}".format(frame)].append(racer_name)
                        race_result_dict["motor_{0}".format(frame)].append(motor)
                        race_result_dict["boat_{0}".format(frame)].append(boat)
                        race_result_dict["exhibitionTime_{0}".format(frame)].append(exhibition_time)
                        race_result_dict["exhibitionRank_{0}".format(frame)].append(exhibition_rank)
                        race_result_dict["startTime_{0}".format(frame)].append(start_time)
                        race_result_dict["raceTime_{0}".format(frame)].append(race_time)

                    # 払い戻し結果を取得
                    payoff_result = race_body[10:19]
                    win_number = payoff_result[0][15]   # 単勝勝ち艇
                    win_payoff = int(payoff_result[0][25:29])    # 単勝払い戻し
                    place_number_1 = payoff_result[1][15]
                    place_payoff_1 = int(payoff_result[1][25:29])
                    try:
                        place_number_2 = payoff_result[1][31]
                        place_payoff_2 = int(payoff_result[1][41:45])
                    except IndexError:  # なぜか書いてないことがある
                        place_number_2 = ""
                        place_payoff_2 = ""

                    exacta_number = payoff_result[2][14:17]
                    exacta_payoff = int(payoff_result[2][24:28])
                    quinella_number = payoff_result[3][14:17]
                    quinella_payoff = int(payoff_result[3][23:28])
                    wide_1_number = payoff_result[4][14:17]
                    wide_1_payoff = int(payoff_result[4][24:28])
                    wide_2_number = payoff_result[5][17:20]
                    wide_2_payoff = int(payoff_result[5][27:31])
                    wide_3_number = payoff_result[6][17:20]
                    wide_3_payoff = int(payoff_result[6][27:31])
                    trifecta_number = payoff_result[7][14:19]   # 3連単
                    trifecta_payoff = int(payoff_result[7][22:28])
                    trio_number = payoff_result[8][14:19]   # ３連複
                    trio_payoff = int(payoff_result[8][23:28])


                    # print(hd, jcd, race, weather, wind_dir, wind_power, wave, ruler)

                    """
                    print(win_number, win_payoff, place_number_1, place_payoff_1, place_number_2, place_payoff_2,
                          exacta_number, exacta_payoff, quinella_number, quinella_payoff,
                          wide_1_number, wide_1_payoff, wide_2_number, wide_2_payoff, wide_3_number, wide_3_payoff,
                          trifecta_number, trifecta_payoff, trio_number, trio_payoff
                          )
                    """

                    # 辞書に格納
                    race_result_dict["date"].append(hd)
                    race_result_dict["venue"].append(jcd)
                    race_result_dict["raceNumber"].append(race)
                    race_result_dict["weather"].append(weather)
                    race_result_dict["windDir"].append(wind_dir)
                    race_result_dict["windPow"].append(wind_power)
                    race_result_dict["waveHight"].append(wave)
                    race_result_dict["ruler"].append(ruler)
                    race_result_dict["win"].append(win_number)
                    race_result_dict["winOdds"].append(win_payoff)
                    race_result_dict["place_1"].append(place_number_1)
                    race_result_dict["placeOdds_1"].append(place_payoff_1)
                    race_result_dict["place_2"].append(place_number_2)
                    race_result_dict["placeOdds_2"].append(place_payoff_2)
                    race_result_dict["exacta"].append(exacta_number)
                    race_result_dict["exactaOdds"].append(exacta_payoff)
                    race_result_dict["quinella"].append(quinella_number)
                    race_result_dict["quinellaOdds"].append(quinella_payoff)
                    race_result_dict["wide_1"].append(wide_1_number)
                    race_result_dict["wideOdds_1"].append(wide_1_payoff)
                    race_result_dict["wide_2"].append(wide_2_number)
                    race_result_dict["wideOdds_2"].append(wide_2_payoff)
                    race_result_dict["wide_3"].append(wide_3_number)
                    race_result_dict["wideOdds_3"].append(wide_3_payoff)
                    race_result_dict["trifecta"].append(trifecta_number)
                    race_result_dict["trifectaOdds"].append(trifecta_payoff)
                    race_result_dict["trio"].append(trio_number)
                    race_result_dict["trioOdds"].append(trio_payoff)

    race_result_df = pd.DataFrame(race_result_dict)

    return race_result_df


if __name__ == "__main__":

    race_result_df = load()
    print(race_result_df.dtypes)