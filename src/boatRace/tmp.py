# -*- coding=utf8 =*-
import matplotlib.pyplot as plt
import itertools
import pandas as pd
import sys
sys.path.append("../.")
# my module
import summarizer_motorboat_data_filename
import boatrace_crawler_conf

if __name__ == "__main__":
    file = summarizer_motorboat_data_filename.make_csv_odds()
    df = pd.read_csv(file)
    df = df.replace(' 6-1-6', ' 6-1-5')
    df.to_csv(file, index=False)