import os
import pandas as pd
from prepare_data_utils import load_one_season


def prepare_relevant_data() -> None:
    directory = "./data/relevant_data"
    for filename in os.listdir(directory):
        if len(filename) == 10:
            league = filename[:2]
            year = filename[2:6]
            raw_data = pd.read_csv(directory + "/" + filename)  # type: ignore
            dataframe = load_one_season(raw_data, league, year)
            ## FIXME: Do something, maybe return status... and how many files, percent loaded
