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


def voting_algolithm_1(predict_proba_all, threshold_1, threshold_2, threshold_3):
    """
    1を頭に、x_2以上+x_3以上の組み合わせBOX買い（x_2v > x_3)
    :param predict_proba_all:
    :param threshold_1:
    :param threshold_2:
    :param threshold_3:
    :return:
    """

    voting_number_list = []

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

    return voting_number_list


def voting_algolithm_2(predict_proba_all, threshold_1, threshold_2, threshold_3):
    """
    2-1-iの組み合わせを買い
    :param predict_proba_all:
    :param threshold_1:
    :param threshold_2:
    :param threshold_3:
    :return:
    """

    voting_number_list = []

    if predict_proba_all[0] > threshold_1:
        if predict_proba_all[1] > threshold_2:
            for k in range(3, 7):
                if predict_proba_all[k - 1] > threshold_3:
                    voting_number_list.append("2-1-{0}".format(k))

    return voting_number_list



def main(rno, jcd, hd):

    venue_list = ["　津　", "三　国", "下　関", "丸　亀", "住之江",
                  "児　島", "唐　津", "多摩川", "大　村", "宮　島",
                  "尼　崎", "常　滑", "平和島", "徳　山", "戸　田",
                  "桐　生", "江戸川", "浜名湖", "琵琶湖", "福　岡",
                  "芦　屋", "若　松", "蒲　郡", "鳴　門"]


    # clf_list (各ラベルについて学習ずみのclfを要素とするリスト) をロード
    output_file = os.path.join(current_dir, 'LR_dump')
    clf_list = pickle.load(open(output_file, 'rb'))

    # 直前情報をcrawlして取得
    the_beforeinfo_df = exhibition_crawler.main(rno, jcd, hd)

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
        # 全国勝率・二連・三連率
        for_analysis_dict["win_rate_national_{0}".format(i)] = the_motor_and_boat_df["win_rate_national_{0}".format(i)]
        for_analysis_dict["place2Ratio_national_{0}".format(i)] = the_motor_and_boat_df["place2Ratio_national_{0}".format(i)]
        for_analysis_dict["place3Ratio_national_{0}".format(i)] = the_motor_and_boat_df["place3Ratio_national_{0}".format(i)]
        # 勝率・二連率・三連率（当地）
        for_analysis_dict["win_rate_local_{0}".format(i)] = the_motor_and_boat_df["win_rate_local_{0}".format(i)]
        for_analysis_dict["place2Ratio_local_{0}".format(i)] = the_motor_and_boat_df["place2Ratio_local_{0}".format(i)]
        for_analysis_dict["place3Ratio_local_{0}".format(i)] = the_motor_and_boat_df["place3Ratio_local_{0}".format(i)]
        # 展示タイム
        for_analysis_dict["exhibitionTime_{0}".format(i)] = the_beforeinfo_df["exhibitionTime_{0}".format(i)]
        # 展示競争の進入コース
        for_analysis_dict["exhibition_cource_{0}".format(i)] = the_beforeinfo_df["exhibition_cource_{0}".format(i)]

        # モーターおよびボートの成績
        for_analysis_dict["motor_place2Ratio_{0}".format(i)] = float(the_motor_and_boat_df["motor_place2Ratio_{0}".format(i)][0][1:])
        for_analysis_dict["motor_place3Ratio_{0}".format(i)] = float(the_motor_and_boat_df["motor_place3Ratio_{0}".format(i)][0][1:])
        for_analysis_dict["boat_place2Ratio_{0}".format(i)] = float(the_motor_and_boat_df["boat_place2Ratio_{0}".format(i)][0][1:])
        for_analysis_dict["boat_place3Ratio_{0}".format(i)] = float(the_motor_and_boat_df["boat_place3Ratio_{0}".format(i)][0][1:])

    for venue in venue_list:
        if venue == jcd:
            for_analysis_dict["{0}".format(venue)] = 1
        else:
            for_analysis_dict["{0}".format(venue)] = 0

    # dfに格納
    for_analysis_df = pd.DataFrame(for_analysis_dict)
    pd.set_option("display.max_columns", 500)
    # クラスカラムを，A1 =0, A2 = 1のように数字に変換する
    for_analysis_df = convert_class_into_int(for_analysis_df)

    # dfをfloatに変換
    for_analysis_df = for_analysis_df.astype(float)

    # inputに用いることができるarrayに直す
    x = for_analysis_df.values

    # ラベルが1になる確率を1号艇から6号艇の順に並べたリスト
    predict_proba_all = []
    for i, clf in enumerate(clf_list):
        predict_proba_all.append(clf.predict_proba(x)[0][1])

    print(predict_proba_all)

    # 投票するリストを作成 (1頭でx_2を超えたやつとx_3を超えたやつの組み合わせbox
    voting_number_list_1 = voting_algolithm_1(predict_proba_all, 0.6, 0.8, 0.7)
    voting_number_list_2 = voting_algolithm_2(predict_proba_all, 0.5, 0.8, 0.6)
    voting_number_list = voting_number_list_1 + voting_number_list_2
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
    the_rno = "11R"
    the_jcd = "桐　生"
    the_hd = "2019/10/21"

    # ---------------------------

    the_voting_number_list = main(the_rno, the_jcd, the_hd)