

def make_label_boolean_ver1(for_analysis_df, column_list_label):
    """
    dfのラベルを下記のように変換する。
    1枠の選手に関しては、1着なら1, それ以外なら0, 2枠以降の選手に関しては、3着以内なら1, 3着以外なら0のboolean

    :param for_analysis_df:
    :param column_list_label:
    :return:
    """

    for column_name in column_list_label:
        if column_name == "rank_1":
            # 1枠の着順のカラムに関しては、トップなら1, そうでなければ0のbooleanのカラムにする
            for_analysis_df.loc[for_analysis_df[column_name] != 1, column_name] = 0
        else:
            # 2枠以降の選手に関しては，3着以内なら1, そうでなければ0のboolean
            for_analysis_df.loc[for_analysis_df[column_name] < 3.5, column_name] = 1
            for_analysis_df.loc[for_analysis_df[column_name] > 3.5, column_name] = 0

    return for_analysis_df


def make_label_boolean_ver2(for_analysis_df, column_list_label):
    """
    dfのラベルを下記のように変換する。
    1枠-6枠それぞれの選手に対して、1着～3着それぞれになるか否かのboolean 18個

    :param for_analysis_df:
    :param column_list_label:
    :return:
    """

    for column_name in column_list_label:
        for r in range(1, 4):
            for_analysis_df.loc[for_analysis_df[column_name]==r, "{0}_{1}".format(column_name, r)] = 1
            for_analysis_df.loc[for_analysis_df[column_name]!=r, "{0}_{1}".format(column_name, r)] = 0
        for_analysis_df.drop(column_name, axis=1, inplace=True)
        print(column_name)
        print(for_analysis_df.columns)

    return for_analysis_df



def standerdize_feature_values(input_df, column_list_label):
    """
    特徴量+labelのdfをインプットとし、特徴量部分の標準化をおこなう。
    :param input_df:
    :param column_list_label:
    :return:
    """
    df_std = input_df.drop(column_list_label, axis=1)
    print(df_std)
    df_std = (df_std - df_std.mean()) / df_std.std()
    df_std[column_list_label] = input_df[column_list_label]
    # print(for_analysis_df_std)

    return df_std


if __name__ == '__main__':
    for_analysis_df = pd.DataFrame({"age": [1, 2, 3], "hight": [10, 20, 30]})
    for_analysis_df = make_label_boolean_ver2(for_analysis_df, ["age", "hight"])