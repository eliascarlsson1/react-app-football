import os
import sqlite3
import pandas as pd
from typing import List, Dict

script_dir = os.path.dirname(__file__)
path_to_db = "../../data/db.sqlite"
database_abs_path = os.path.join(script_dir, "../../data/db.sqlite")
con = sqlite3.connect(database_abs_path)


# Returns a list of all the historical csv files
def get_historical_data_list() -> List[str]:
    path = "./data/historical_data/relevant_data"
    historical_data_list: List[str] = []
    for filename in os.listdir(path):
        if len(filename) == 10:
            league = filename[:2]
            year = filename[2:6]
            historical_data_list.append(league + year)

    return historical_data_list


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


# Selects and concatenates dataframes from a df_dict
def concatenate_df_dict(
    dataframes_dict: Dict[str, pd.DataFrame], to_concatenate: List[str]
) -> pd.DataFrame:
    # Creating a list of all dataframes
    dataframes_names = [key for key in dataframes_dict]
    dataframes = [dataframes_dict[key] for key in to_concatenate]

    # Preparing test and train data
    for i, df in enumerate(dataframes):
        df["n_df"] = dataframes_names[i]

    data = pd.concat(dataframes).reset_index()  # type: ignore

    return data

def get_all_X_parameters():
    print(con.execute("SELECT * FROM parameters"))