# -*- coding=utf8 =*-

"""
object: スタートタイムが一号艇のイン逃げ成功率に寄与するのかを知る

"""

import matplotlib.pyplot as plt

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../conf/'))

# my module
import csv_loader

if __name__ == "__main__":
    the_raceresult_summary_df = csv_loader.load_all_raceResults_as_a_df()
    for i in range(2, 7):
        x = df_start_time = the_raceresult_summary_df["starttime_float_{0}".format(i)]
        y = the_raceresult_summary_df["starttime_float_1"]
        color_code = the_raceresult_summary_df["着_1"]
        plt.scatter(x, y, c=color_code)
        plt.show()