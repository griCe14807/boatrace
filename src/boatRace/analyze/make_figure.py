# -*- coding=utf8 =*-
import sys
import matplotlib.pyplot as plt

sys.path.append("../.")
# my module
import summarizer_motorboat_data_filename
import boatrace_crawler_conf


"""
TODO 色分けがうまくできないのであれだけど、これは作りたい
枠番で色分けして、これまでのtimeを日付ごとにplotした散布図を作成
frame_cmap = ListedColormap(["grey", "black", "red", "blue", "yellow", "green"])

# plt.plot(the_filtered_df_1["日付"],the_filtered_df_1["レースタイム"])
# plt.plot(the_filtered_df_2["日付"],the_filtered_df_2["レースタイム"])
# plt.plot(the_filtered_df_3["日付"],the_filtered_df_3["レースタイム"])
# plt.plot(the_filtered_df_4["日付"],the_filtered_df_4["レースタイム"])
# plt.plot(the_filtered_df_6["日付"],the_filtered_df_6["レースタイム"])

x = the_filtered_df_5["日付"]
y = the_filtered_df_5["racetime_float"]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot_date(x, y, c=the_filtered_df_5["枠"], cmap=cm.Accent, marker="o")

plt.show()
"""


def plot_result_on_single_figure(filtered_df_list):
    """
    一号艇から六号艇までのこれまでのレースタイムをプロット
    :param filtered_df_list:
    :return:
    """

    x_1 = filtered_df_list[0]["日付"]
    y_1 = filtered_df_list[0]["racetime_float"]
    x_2 = filtered_df_list[1]["日付"]
    y_2 = filtered_df_list[1]["racetime_float"]
    x_3 = filtered_df_list[2]["日付"]
    y_3 = filtered_df_list[2]["racetime_float"]
    x_4 = filtered_df_list[3]["日付"]
    y_4 = filtered_df_list[3]["racetime_float"]
    x_5 = filtered_df_list[4]["日付"]
    y_5 = filtered_df_list[4]["racetime_float"]
    x_6 = filtered_df_list[5]["日付"]
    y_6 = filtered_df_list[5]["racetime_float"]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot_date(x_1, y_1, label="1号艇")
    ax.plot_date(x_2, y_2, label="2号艇")
    ax.plot_date(x_3, y_3, label="3号艇")
    ax.plot_date(x_4, y_4, label="4号艇")
    ax.plot_date(x_5, y_5, label="5号艇")
    ax.plot_date(x_6, y_6, label="6号艇")

    plt.legend()


if __name__ == "__main__":
    # figure書きだし
    plot_result_on_single_figure(the_filtered_df_list_racer_frame)

    plt.show()