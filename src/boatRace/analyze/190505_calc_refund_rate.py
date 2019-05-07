# -*- coding=utf8 =*-
import pandas as pd
import matplotlib.pyplot as plt
import os

# my module
import analysis_df_maker

if __name__ == "__main__":
    ### input
    voting_threshold = 2
    occurrence_rate = 0.03
    the_input_date = "20190503"

    for_analysis_df = analysis_df_maker.main(the_input_date)

    # 条件に応じてbetする組番を残したdfを作成（filtering)
    betted_df = for_analysis_df[for_analysis_df["期待値"] > voting_threshold]
    # 必要に応じて以下さらにfilteringをおこなう
    betted_df = betted_df[betted_df["くる率"] > occurrence_rate]

    # 収支カラムを作成
    betted_df.loc[betted_df["的中"]==1, "収支"] = betted_df["オッズ"] - 1
    betted_df.loc[betted_df["的中"] == 0, "収支"] = - 1

    output_filename = the_input_date + "_vt" + str(voting_threshold) + "_or" + str(occurrence_rate) + ".csv"
    betted_df.to_csv(os.path.join("/Users/grice/mywork/Gambling/data/boatRace/analyze/for_analysis/", output_filename))

    """
    # 累計収支カラムを作成
    betted_df["累計収支"] = betted_df["収支"]
    print(betted_df.iloc[0:2, 5:11])
    for i in range(1, len(betted_df)):
        # 10列目が累計収支、9列目がその行の収支
        betted_df.iloc[i, 10] = betted_df.iloc[i, 9] + betted_df.iloc[i-1, 10]

    print(betted_df)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(hit_rate, odds)

    plt.legend()
    plt.show()
    """


