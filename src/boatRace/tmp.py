# -*- coding=utf8 =*-
import matplotlib.pyplot as plt
import itertools
import pandas as pd
import sys
sys.path.append("../.")
# my module
import summarizer_motorboat_data_filename


def _1904XX_():

    file = summarizer_motorboat_data_filename.make_csv_odds()
    df = pd.read_csv(file)
    df = df.replace(' 6-1-6', ' 6-1-5')
    df.to_csv(file, index=False)

def _190505_support(str):
    return " " + str

def _190505_add_space_to_simulation_result_kumibann():
    simulation_result_file = r"/Users/grice/mywork/Gambling/data/boatRace/analyze/simulation_results_csv/3t/20190503_3t_simulationResult.csv"
    simulation_result_df = pd.read_csv(simulation_result_file)
    simulation_result_df["組番"] = simulation_result_df["組番"].map(_190505_support)
    simulation_result_df.to_csv(simulation_result_file, index=False)

def _delete_a_column():
    simulation_result_file = r"/Users/grice/mywork/Gambling/data/boatRace/analyze/simulation_results_csv/3t/20190502_3t_simulationResult.csv"
    simulation_result_df = pd.read_csv(simulation_result_file)
    simulation_result_df = simulation_result_df.drop("Unnamed: 0", axis=1)
    print(simulation_result_df)
    simulation_result_df.to_csv(simulation_result_file, index=False)


if __name__ == "__main__":
    _190505_add_space_to_simulation_result_kumibann()
