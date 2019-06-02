# -*- coding=utf8 =*-

import pandas as pd
import numpy as np
import scipy.stats as stats
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../conf/'))
sys.path.append(os.path.join(current_dir, '../../conf/'))

import summarizer_motorboat_data_filename


def standerdize_feature_values(input_df, column_list_label):
    """
    特徴量+labelのdfをインプットとし、特徴量部分の標準化をおこなう。
    :param input_df:
    :param column_list_label:
    :return:
    """
    df_std = input_df.drop(column_list_label, axis=1)
    df_std = (df_std - df_std.mean()) / df_std.std()
    df_std[column_list_label] = input_df[column_list_label]
    # print(for_analysis_df_std)

    return df_std

def make_label_boolean_ver1(for_analysis_df, column_list_label):
    """
    dfのラベルを下記のように変換する。
    1枠の選手に関しては、1着なら1, それ以外なら0, 2枠以降の選手に関しては、3着以内なら1, 3着以外なら0のboolean

    :param for_analysis_df:
    :param column_list_label:
    :return:
    """

    for column_name in column_list_label:
        if column_name == "着_1":
            # 1枠の着順のカラムに関しては、トップなら1, そうでなければ0のbooleanのカラムにする
            for_analysis_df.loc[for_analysis_df[column_name] != 1, column_name] = 0
        else:
            for_analysis_df.loc[for_analysis_df[column_name] < 3.5, column_name] = 1
            for_analysis_df.loc[for_analysis_df[column_name] > 3.5, column_name] = 0

    return for_analysis_df


def knn(k, train_data, test_data, label_size):
    """

    :param k:
    :param train_data:
    :param test_data:
    :param label_size:
    :return:
    """
    labels = []

    for test in test_data:
        # すべてのトレインデータとtest（このループステップでラベルを予測したいデータ）との距離を計算したリストを作る
        distances = np.sum((train_data[:, :-(label_size)] - test[:-(label_size)]) ** 2, axis=1)

        # 距離リストの値が小さい順に並べた、トレインデータのインデックスを持つリストを作る
        sorted_train_indexes = np.argsort(distances)

        # インデックスリストを元に、testから近いk個のトレインデータのラベルを取り出す
        sorted_k_labels = train_data[sorted_train_indexes, -(label_size):][:k]

        # sorted_k_labelsの中で最も数の多かったlabelを取り出す
        mode_result = stats.mode(sorted_k_labels)

        # 最も多かったラベルをnumpyx.ndarray形式で取得
        label = mode_result.mode[0]

        labels.append(label)

    # labelsをarrayに変換
    labels = np.array(labels)

    return labels


if __name__ == "__main__":

    ####### input #######
    # 解析に使う特徴量カラム
    column_list_fv = ["ave_starttime_{0}".format(i) for i in range(1, 7)] + ["ave_着_{0}".format(i) for i in range(1, 7)]
    # 解析に使うラベルカラム
    column_list_label = ["着_{0}".format(i) for i in range(1, 4)]
    print(column_list_label)

    # データのうち、教師データとして使う割合（残りをテストデータとして用いる）
    train_data_ratio = 0.7

    # k-NNのk (周囲何個までみるか）
    k = 100

    ####################

    # 解析用dfをload
    for_analysis_df = pd.read_csv(summarizer_motorboat_data_filename.make_csv_for_analysis())

    # knnのinput用にlabelのサイズの変数を作成しておく
    label_size = len(column_list_label)

    # 解析用dfから必要なカラムを抜き出す
    column_list = column_list_fv + column_list_label
    for_analysis_df = for_analysis_df[column_list]


    # ラベルをbooleanに変換
    for_analysis_df = make_label_boolean_ver1(for_analysis_df, column_list_label)

    # 標準化されたdfを作成
    for_analysis_df_std = standerdize_feature_values(for_analysis_df, column_list_label)

    # 教師データとテストデータに分ける (標準化なしのデータ)
    train_size = int(len(for_analysis_df) * train_data_ratio)

    train_data = for_analysis_df[:train_size].values
    test_data = for_analysis_df[train_size:].values

    # 教師データとテストデータに分ける (標準化したデータ)
    train_data_std = for_analysis_df_std[:train_size].values
    test_data_std = for_analysis_df_std[train_size:].values

    # ラベルの不均一性について確認
#    for column_name in column_list_label:
#        i = int(column_name[-1])
#        print("教師データのうち{0}枠でラベル==1の割合は{1}".format(i, np.sum(train_data[:, -(label_size + 1 - i)]) / len(train_data)))
#        print("テストデータのうち{0}枠でラベル==1の割合は{1}".format(i, np.sum(test_data[:, -(label_size + 1 - i)]) / len(test_data)))

    # k-NNの実行
    pred_labels = knn(k, train_data, test_data, label_size)
    pred_labels_std = knn(k, train_data_std, test_data_std, label_size)

    # 正答率を計算
    accuracy = np.sum(pred_labels == test_data[:, -(label_size):], axis=0) / len(test_data)
    accuracy_std = np.sum(pred_labels_std==test_data[:, -(label_size):], axis=0) / len(test_data_std)

    print(accuracy)
    print(accuracy_std)