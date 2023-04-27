import os
import pandas as pd
from typing import List


# Returns a list of all the historical csv files
def get_historical_data_list() -> List[str]:
    path = "./data/historical_data/relevant_data"
    return os.listdir(path)


#
def get_is_all_relevant_data_prepared() -> bool:
    relevant_data_path = "./data/historical_data/relevant_data"
    relavant_data_files = os.listdir(relevant_data_path)
    prepared_data_path = "./data/prepared_data"
    prepared_data_files = os.listdir(prepared_data_path)
    for file in relavant_data_files:
        if file not in prepared_data_files:
            return False
    return True


# Loads all prepared data
def get_prepared_data() -> dict[str, pd.DataFrame]:
    directory = "./data/prepared_data"
    df_dict: dict[str, pd.DataFrame] = {}
    for filename in os.listdir(directory):
        if len(filename) == 10:
            league = filename[:2]
            year = filename[2:6]
            path = directory + "/" + filename
            df_dict[league + year] = pd.read_csv(path)  # type: ignore

    return df_dict
