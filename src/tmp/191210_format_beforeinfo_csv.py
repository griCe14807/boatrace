# -*- coding=utf8 =*-

import pandas as pd
import glob

def main(filepath):
    """
    flying_i カラム名をexhibition_flying_flag_i　へと変換
    late_i カラム名をexhibition_late_flag_i　へと変換
    exhibition_late_flag_iをゼロ埋めする
    """

    df = pd.read_csv(filepath)

    for i in range(1, 7):
        df.rename(columns={'flying_{0}'.format(i): 'exhibition_flying_flag_{0}'.format(i),
                           'late_{0}'.format(i): 'exhibition_late_flag_{0}'.format(i)},
                  inplace=True)
        df.fillna(0, inplace=True)
    df.to_csv(filepath)


if __name__ == "__main__":

    mypath = r"/Users/grice/mywork/boatrace/data/beforeinfo/1*.csv"
    for filename in glob.glob(mypath):
        print(filename)
        main(filename)