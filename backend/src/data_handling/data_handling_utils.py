import os
import pandas as pd
from typing import List, Dict


### Paths ###
relative_data_path = "../../data"
file_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(file_path, relative_data_path)
relevant_data_path = data_path + "/historical_data/relevant_data"
prepared_data_path = data_path + "/prepared_data"
prepared_scrape_data_csv = data_path + "/prepared_scrape.csv"
all_data_path = data_path + "/historical_data/all_data"


# Returns a list of all the historical csv files
def get_historical_data_list() -> List[str]:
    historical_data_list: List[str] = []
    for filename in os.listdir(relevant_data_path):
        if len(filename) == 10:
            league = filename[:2]
            year = filename[2:6]
            historical_data_list.append(league + year)

    return historical_data_list


#
def get_is_all_relevant_data_prepared() -> bool:
    relavant_data_files = os.listdir(relevant_data_path)
    prepared_data_files = os.listdir(prepared_data_path)
    for file in relavant_data_files:
        if file not in prepared_data_files:
            return False
    return True


# Loads all prepared data
def get_prepared_data_dict() -> dict[str, pd.DataFrame]:
    df_dict: dict[str, pd.DataFrame] = {}
    for filename in os.listdir(prepared_data_path):
        if len(filename) == 10:
            league = filename[:2]
            year = filename[2:6]
            path = prepared_data_path + "/" + filename
            df_dict[league + year] = pd.read_csv(path)  # type: ignore

    return df_dict


def get_all_historical_data_dict() -> dict[str, pd.DataFrame]:
    df_dict: dict[str, pd.DataFrame] = {}
    for filename in os.listdir(all_data_path):
        if len(filename) == 10:
            league = filename[:2]
            year = filename[2:6]
            path = all_data_path + "/" + filename
            df_dict[league + year] = pd.read_csv(path)  # type: ignore

    return df_dict


def load_prepared_scrape() -> pd.DataFrame:
    return pd.read_csv(prepared_scrape_data_csv)  # type: ignore


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
