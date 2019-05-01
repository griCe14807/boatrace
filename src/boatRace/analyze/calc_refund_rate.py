# -*- coding=utf8 =*-

def calc_refund_rate(bet_result, odds):
    """

    :param bet_result: 的中返還。pandas.Series
    :param odds: それぞれのオッズ。pandas.Series
    :return:
    """
    # betを計算。とりあえず、全部に一律100円だった場合
    bet_total_bool = ~bet_result.isnull()
    bet_result_bool = bet_result.isin(["的中"])

    # refundを計算
    refunds = odds * bet_result_bool

    refund_rate = refunds.sum() / bet_total_bool.sum()
    return refund_rate


def calc_filtered_refund_rate(for_analysis_df, bin_size):
    """
    オッズでbinを区切って回収率を計算
    :param bin_size:
    :return:
    """
    odds_vs_refund_rate_list = []
    for i in range (200 // bin_size):
        filtered_df = for_analysis_df[(for_analysis_df["オッズ"] > (bin_size * i))
                                          & (for_analysis_df["オッズ"] < (bin_size * (i+1)))]
        filtered_refund_rate = calc_refund_rate(filtered_df["的中返還_katagiri"], filtered_df["オッズ"])

        odds_vs_refund_rate_list.append([i * bin_size, filtered_refund_rate])

    return odds_vs_refund_rate_list


def calc_expect_value_of_each_number(number_tuple, counts_tuple, odds_df, num_simulation, odds_threshold):
    # 組番ごとの期待値を計算
    expected_value_list = []
    bet_list = []
    for i, number in enumerate(number_tuple):
        # 期待値を計算
        the_coming_rate = counts_tuple[i] / num_simulation
        odds = odds_df[odds_df["組番"] == (" " + number)]["オッズ"].values[0]
        if odds == "欠場":
            print("欠場のためシミュレーションせず")
            break

        else:
            odds = float(odds)
            # print("組番 {0}: オッズ={1}".format(the_number, the_odds))
            expected_value = the_coming_rate * odds
            expected_value_list.append(expected_value)

            if expected_value > odds_threshold:
                bet_list.append(number)

    return expected_value_list, bet_list
