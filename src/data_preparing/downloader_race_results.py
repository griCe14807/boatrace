"""How to use this script
(1) Download race result files by RaceResults.download()
(2) Manually extract text files from lzh files
(3) Move the text files to ./data directory
(4) RaceResults.load() will parse the text files
"""

import pandas as pd
import urllib
import os
import time
# import patoolib


current_dir = os.path.dirname(os.path.abspath(__file__))



class RaceResults:
    def __init__(self):
        self.baseuri = "http://www1.mbrace.or.jp/od2/K/%s/k%s.lzh" # http://www1.mbrace.or.jp/od2/K/201612/k161201.lzh
        self.id2index = None

    def download(self, start, end):
        period = pd.date_range(start, end)

        for date in period:
            # Get file from the website
            dirname = date.strftime("%Y%m")
            lzhname = date.strftime("%y%m%d")
            uri = self.baseuri % (dirname, lzhname)
            savename = os.path.join(current_dir, "../../data/results_race/lzh/%s.lzh") % lzhname
            if not os.path.exists(savename):
                print("Send request to", uri)
                urllib.request.urlretrieve(uri, savename)
                time.sleep(3)

            # The following unpack part didn't work my Windows environment...
            # Unpack lzh files
            # unpackedname = "./data/results/K%s.TXT" % lzhname
            # if not os.path.exists(unpackedname):
            #     print("Unpacking", savename)
            #     patoolib.extract_archive(savename, outdir="./data/results")

if __name__ == "__main__":
    r = RaceResults()
    r.download("2019-08-18", "2019-08-22")

