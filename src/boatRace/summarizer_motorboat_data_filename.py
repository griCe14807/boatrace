# -*- coding=utf8 =*-
import os

"""
windows-macのそれぞれでいじる際、ファイルごとにパスを変えるのはめんどいので、このファイル内で変更するべし

"""


# oddsまとめファイルのパスとファイル名
def make_csv_odds():
    boatrace_odds_csv_path = r"/Users/grice/mywork/Gambling/data/boatRace/results_odds"
    boatrace_odds_csv_filename = "boatRace_odds.csv"
    boatrace_odds_csv_file = os.path.join(boatrace_odds_csv_path, boatrace_odds_csv_filename)

    return boatrace_odds_csv_file


def make_csv_voting_result():
    whose_data = ["katagiri", "SHKamPo"]
    voting_csv_file_list = []
    for whose in whose_data:
        voting_result_csv_path = r"/Users/grice/mywork/Gambling/data/boatRace/results_voting/"
        voting_csv_filename = "voting_resut_" + whose + ".csv"
        voting_csv_file = os.path.join(voting_result_csv_path + voting_csv_filename)
        voting_csv_file_list.append((voting_csv_file))

    return voting_csv_file_list


def make_csv_for_analysis():
    for_analysis_csv_path = r"/Users/grice/mywork/Gambling/data/boatRace/analyze/"
    for_analysis_csv_filename = "boatrace_summary.csv"
    for_analysis_csv_file = os.path.join(for_analysis_csv_path, for_analysis_csv_filename)

    return for_analysis_csv_file


def make_csv_race_results():
    boatrace_race_csv_path = r"/Users/grice/mywork/Gambling/data/boatRace/results_race"
    boatrace_race_csv_filename = "boatRace_raceResults.csv"
    boatrace_raceResults_csv_file = os.path.join(boatrace_race_csv_path, boatrace_race_csv_filename)

    return boatrace_raceResults_csv_file

def make_csv_simulation_results():
    path = r"/Users/grice/mywork/Gambling/data/boatRace/analyze/simulation_results"
    filename = "simulationResults.csv"
    csv_file = os.path.join(path, filename)

    return csv_file

def make_csv_closing_time(hd):
    path = r"/Users/grice/mywork/Gambling/data/boatRace"
    filename = "".join(hd.split("/")) + ".csv"
    csv_file = os.path.join(path, filename)

    return csv_file