# -*- coding=utf8 =*-

# my module
import loader

if __name__ == "__main__":

    # これまでのレース結果をロード
    race_result_df = loader.load_race_results()

    # 出場履歴のある選手の登録番号のリストを作成
    racer_id_list = []
    for i in range(1, 7):
        racer_id_list_ = race_result_df["racerId_{0}".format(i)]

        racer_id_list.extend(racer_id_list_.unique())
    racer_id_set = set(racer_id_list)

    # 選手ごとに統計量を作成
    for racer_id in racer_id_set:
        # 枠番ごとの平均ST


    # TODO: classはレースごとに取得することに変更
    # TODO: 本当はこうやって作ったやつをinputにする方がいい。そうしないとレーサーの強さが過去のデータになる。

    """
    for_merge_df = racer_df[["racerName_ch",
                             "class",
                             "aveST_frame{0}".format(i),
                             "placeRate_frame{0}".format(i)
                             ]]
    """