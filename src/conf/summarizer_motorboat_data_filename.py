# -*- coding=utf8 =*-
import os

"""
windows-macのそれぞれでいじる際、ファイルごとにパスを変えるのはめんどいので、このファイル内で変更するべし

"""

def return_directory_path(key):
    directory_path_dict = {"odds": r"/Users/grice/mywork/boatrace/data/results_odds/",
                           "simulationResults": r"/Users/grice/mywork/boatrace/data/simulation/simulation_results_csv/",
                           "raceResults": r"/Users/grice/mywork/boatrace/data/results_race/crawled"
                           }

    return directory_path_dict[key]


# oddsまとめファイルのパスとファイル名
def make_csv_odds(hd, how_to_bet):
    boatrace_odds_csv_path = return_directory_path("odds") + how_to_bet[4:]
    boatrace_odds_csv_filename = hd[0:4] + hd[5:7] + hd[8:10] + "_odds" + how_to_bet[4:] + ".csv"
    boatrace_odds_csv_file = os.path.join(boatrace_odds_csv_path, boatrace_odds_csv_filename)

    return boatrace_odds_csv_file


def make_csv_voting_result():
    whose_data = ["katagiri", "SHKamPo"]
    voting_csv_file_list = []
    for whose in whose_data:
        voting_result_csv_path = r"/Users/grice/mywork/boatrace/data/boatRace/results_voting/"
        voting_csv_filename = "voting_resut_" + whose + ".csv"
        voting_csv_file = os.path.join(voting_result_csv_path + voting_csv_filename)
        voting_csv_file_list.append((voting_csv_file))

    return voting_csv_file_list


def make_csv_for_analysis():
    for_analysis_csv_path = r"/Users/grice/mywork/boatrace/data/analysis/"
    for_analysis_csv_filename = "race_result_summary.csv"
    for_analysis_csv_file = os.path.join(for_analysis_csv_path, for_analysis_csv_filename)

    return for_analysis_csv_file


def make_csv_race_results(hd):
    boatrace_race_csv_path = return_directory_path("raceResults")
    boatrace_race_csv_filename = hd[0:4] + hd[5:7] + hd[8:10] + "_raceResults.csv"
    boatrace_raceResults_csv_file = os.path.join(boatrace_race_csv_path, boatrace_race_csv_filename)

    return boatrace_raceResults_csv_file

def make_csv_simulation_results(the_date_from, the_date_to, voting_threshold):
    path = r"/Users/grice/mywork/boatrace/data/boatRace/simulation/simulation_results"
    filename = the_date_from + "-" + the_date_to + "over" + str(voting_threshold) + ".csv"
    csv_file = os.path.join(path, filename)

    return csv_file


def make_csv_closing_time(hd):
    path = r"/Users/grice/mywork/boatrace/data/boatRace"
    filename = "".join(hd.split("/")) + ".csv"
    csv_file = os.path.join(path, filename)
    return csv_file


def make_csv_simulation_results2(hd, how_to_bet):
    path = return_directory_path("simulationResults") + how_to_bet
    filename = hd[0:4] + hd[5:7] + hd[8:10] + "_" + how_to_bet + "_simulationResult.csv"
    csv_file = os.path.join(path, filename)

    return csv_file


# テスト用
if __name__ == "__main__":
    csv_file = make_csv_odds("2019/05/01", "3t")
    print(csv_file)
