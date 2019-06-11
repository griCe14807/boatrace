# -*- coding=utf8 =*-
import matplotlib.pyplot as plt
import sys
sys.path.append("../.")
# my module
import summarizer_motorboat_data_filename
import raceResult_filter
import make_figure



if __name__ == "__main__":
    ################inputs#################

    the_rno = "12R"
    the_jcd = "下　関"
    the_hd = "2019/04/17"

    # 読み込み先のファイルを指定
    the_race_results_file = summarizer_motorboat_data_filename.make_csv_race_results()

    #######################################

    the_filtered_df_list_racer_frame = raceResult_filter.raceResult_filter(the_race_results_file,
                                                         the_rno, the_jcd, the_hd)

    make_figure.plot_result_on_single_figure(the_filtered_df_list_racer_frame)
    plt.show()