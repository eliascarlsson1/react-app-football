import os
import pandas as pd
from typing import Dict
from . import prepare_data_utils as pdu
from ..data_handling.database_con import get_all_X_parameters

all_x_par = get_all_X_parameters()

relative_data_path = "../../data"
file_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(file_path, relative_data_path)
relevant_data_path = data_path + "/historical_data/relevant_data"
prepared_data_path = data_path + "/prepared_data"


def prepare_relevant_data(all_df_dict: Dict[str, pd.DataFrame]) -> str:
    for filename in os.listdir(relevant_data_path):
        if len(filename) == 10:
            league = filename[:2]
            year = filename[2:6]
            raw_data = pd.read_csv(relevant_data_path + "/" + filename)  # type: ignore
            dataframe = load_one_season(raw_data, league, year, all_df_dict)
            dataframe.to_csv(prepared_data_path + "/" + filename, index=False)
    return "success"


def load_one_season(
    raw_data: pd.DataFrame, league: str, year: str, all_df_dict: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    # Prepare the data
    raw_data = pdu.add_simple_features(raw_data)

    # Calculating features
    raw_data = pd.DataFrame = pdu.calculate_features_from_table(
        raw_data, league, year, all_df_dict
    )

    # Creating the return dataframe
    prepared_data = raw_data[all_x_par]

    ##FIXME: Is this good?
    prepared_data = prepared_data.iloc[10:, :]  # removes first games of each season

    return prepared_data
