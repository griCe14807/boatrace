import pickle
import sys
import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../../conf/'))
sys.path.append(os.path.join(current_dir, '../../crawl/'))
sys.path.append(os.path.join(current_dir, '../../data_preparing/'))
sys.path.append(os.path.join(current_dir, '../../analyze/'))

# my module
import loader
import exhibition_crawler
import race_list_crawler

# 定数定義
DRIVER_WIN = "chromedriver.exe"
DRIVER_MAC = '/Users/grice/Desktop/Selenium/chromedriver'

# 各動作間の待ち時間（秒）
INTERVAL = 3


def convert_class_into_int(input_df):
    """
    クラスカラムを，A1 =0, A2 = 1のように数字に変換する

    :param input_df:
    :return:
    """

    class_dict = {"A1": 0, "A2": 1, "B1": 2, "B2": 3}

    for key, value in class_dict.items():
        input_df.replace(key, value, inplace=True)

    return input_df


def main(rno, jcd, hd, threshold_1, threshold_2, threshold_3):
    voting_number_list = []
    exclude_jcd_list = ["蒲　郡", "平和島", "鳴　門", "下　関", "　津　"]

    if jcd in exclude_jcd_list:
        return voting_number_list
    else:
        # clf_list (各ラベルについて学習ずみのclfを要素とするリスト) をロード
        output_file = os.path.join(current_dir, '../../../data/analysis/LR_dump')
        clf_list = pickle.load(open(output_file, 'rb'))

        # exhibition timeをcrawlして取得
        the_exhibition_time_list = exhibition_crawler.main(jcd, INTERVAL)

        # race_listから取れるデータを取得
        the_motor_and_boat_df = race_list_crawler.main(rno, jcd, hd)
        # racer dfをload
        racer_df = loader.load_racer_data()

        # 解析用dfへ変換する元のjsonを作成
        for_analysis_dict = {}
        for i in range(1, 7):
            racer_row = pd.merge(the_motor_and_boat_df, racer_df, how="left",
                                 left_on=["racer_{0}".format(i), "racer_id_{0}".format(i)],
                                 right_on=["racerName_ch", "racerId"]
                                 )
            for_analysis_dict["class_{0}".format(i)] = [racer_row["class"].values[0]]
            for_analysis_dict["aveST_frame{0}".format(i)] = [racer_row["aveST_frame{0}".format(i)].values[0]]
            for_analysis_dict["placeRate_frame{0}".format(i)] = [racer_row["placeRate_frame{0}".format(i)].values[0]]
            for_analysis_dict["exhibitionTime_{0}".format(i)] = [the_exhibition_time_list[i - 1]]
            for_analysis_dict["motor_place2Ratio_{0}".format(i)] = float(the_motor_and_boat_df["motor_place2Ratio_{0}".format(i)][0][1:])
            for_analysis_dict["motor_place3Ratio_{0}".format(i)] = float(the_motor_and_boat_df["motor_place3Ratio_{0}".format(i)][0][1:])
            for_analysis_dict["boat_place2Ratio_{0}".format(i)] = float(the_motor_and_boat_df["boat_place2Ratio_{0}".format(i)][0][1:])
            for_analysis_dict["boat_place3Ratio_{0}".format(i)] = float(the_motor_and_boat_df["boat_place3Ratio_{0}".format(i)][0][1:])

        # dfに格納
        for_analysis_df = pd.DataFrame(for_analysis_dict)

        # クラスカラムを，A1 =0, A2 = 1のように数字に変換する
        for_analysis_df = convert_class_into_int(for_analysis_df)

        # inputに用いることができるarrayに直す
        x = for_analysis_df.values

        # ラベルが1になる確率を1号艇から6号艇の順に並べたリスト
        predict_proba_all = []
        for i, clf in enumerate(clf_list):
            predict_proba_all.append(clf.predict_proba(x)[0][1])
        print(predict_proba_all)

        # 投票するリストを作成
        if predict_proba_all[0] > threshold_1:
            for j in range(2, 7):
                if predict_proba_all[j - 1] > threshold_2:
                    for k in range(2, 7):
                        if k is not j and predict_proba_all[k - 1] > threshold_3:
                            bet_num_1 = "1-{0}-{1}".format(j, k)
                            bet_num_2 = "1-{0}-{1}".format(k, j)
                            voting_number_list.append(bet_num_1)
                            voting_number_list.append(bet_num_2)

        voting_number_set = set(voting_number_list)
        voting_number_list = list(voting_number_set)
        print(voting_number_list)

        return voting_number_list


if __name__ == "__main__":

    #### 下記inputを指定して実行 ###
    """
    注意点
    1. その場でcrawlするため、開始直前のレースに対してしか適用できない
    2. 以下のレース場に関しては、boatraceBBのサイトが無いため利用不可
    (inputしても自動的にpassになる）
        ["蒲　郡", "平和島", "鳴　門", "下　関", "　津　"]
    
    """
    # ----------input------------
    the_rno = "12R"
    the_jcd = "桐　生"
    the_hd = "2019/08/15"

    threshold_1 = 0.75
    threshold_2 = 0.6
    threshold_3 = 0.4

    # ---------------------------

    the_voting_number_list = main(the_rno, the_jcd, the_hd, threshold_1, threshold_2, threshold_3)