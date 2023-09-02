from typing import List, Dict, Any
import pandas as pd
from ..model_handling.apply_model_utils import (
    apply_model,
    load_x_and_y_parameters_from_model,
    load_training_data_from_model,
)
from ..data_handling.database_con import get_test_parameters
from ..data_handling.calculations import calculate_basic_roi
from ..data_handling.data_handling_utils import (
    concatenate_df_dict,
    get_historical_data_list,
)


def get_roi_for_model(test_data: List[str], model: str) -> Dict[str, str | float]:
    all_data = get_historical_data_list()
    df_dict = apply_model(model, all_data)
    train_data = load_training_data_from_model(model)
    filtered_all_data = [
        x for x in all_data if x not in test_data and x not in train_data
    ]
    df_dict["all other data"] = concatenate_df_dict(df_dict, filtered_all_data)
    y_par = load_x_and_y_parameters_from_model(model)[1]
    roi_dict: Dict[str, str | float] = {}
    for key in df_dict:
        if key not in test_data and key != "all other data":
            continue
        roi_dict[key] = calculate_basic_roi(df_dict[key], y_par)
    return roi_dict


def get_stats_for_model_and_test(
    test_data: List[str], model: str, test: str
) -> Dict[str, Any]:
    all_data = get_historical_data_list()
    train_data = load_training_data_from_model(model)
    filtered_all_data = [
        x for x in all_data if x not in test_data and x not in train_data
    ]
    df_dict_before_filter = apply_model(model, all_data)
    df_dict_before_filter["all other data"] = concatenate_df_dict(
        df_dict_before_filter, filtered_all_data
    )
    df_dict = apply_test_to_df_dict(df_dict_before_filter, test)
    df_dict["all other data"] = concatenate_df_dict(df_dict, filtered_all_data)

    return_dict: Dict[str, Any] = {}
    y_par = load_x_and_y_parameters_from_model(model)[1]
    for key in df_dict:
        if key not in test_data and key != "all other data":
            continue
        this_df_dict = get_stats_for_dataframe(
            key, df_dict, df_dict_before_filter, y_par
        )
        return_dict[key] = this_df_dict

    return return_dict


def get_stats_for_dataframe(
    key: str,
    df_dict: Dict[str, pd.DataFrame],
    df_dict_before_filter: Dict[str, pd.DataFrame],
    y_par: str,
) -> Dict[str, str]:
    this_df_dict: Dict[str, Any] = {}
    this_df_dict["id"] = key
    this_df_dict["gamesBeforeFilter"] = len(df_dict_before_filter[key])
    this_df_dict["gamesAfterFilter"] = len(df_dict[key])
    this_df_dict["zeroBeforeFilter"] = len(
        df_dict_before_filter[key][df_dict_before_filter[key]["prediction"] == 0]
    )
    this_df_dict["oneBeforeFilter"] = len(
        df_dict_before_filter[key][df_dict_before_filter[key]["prediction"] == 1]
    )
    this_df_dict["zeroAfterFilter"] = len(df_dict[key][df_dict[key]["prediction"] == 0])
    this_df_dict["oneAfterFilter"] = len(df_dict[key][df_dict[key]["prediction"] == 1])
    this_df_dict["roi"] = calculate_basic_roi(df_dict[key], y_par)

    return this_df_dict


def apply_test_to_df_dict(
    df_dict: Dict[str, pd.DataFrame], test: str
) -> Dict[str, pd.DataFrame]:
    new_df_dict = df_dict.copy()
    for key in new_df_dict:
        new_df_dict[key] = apply_test_to_df(df_dict[key], test)
    return new_df_dict


def apply_test_to_df(dataframe_in: pd.DataFrame, test: str) -> pd.DataFrame:
    dataframe = dataframe_in.copy()
    parameters = get_test_parameters(test)

    odds_high = float(parameters["odds_high"])
    odds_low = float(parameters["odds_low"])
    dataframe = dataframe[dataframe["odds_pred"] > odds_low]  # type: ignore
    dataframe = dataframe[dataframe["odds_pred"] < odds_high]  # type: ignore

    confidence_over_odds_high = float(parameters["confidence_over_odds_high"])
    confidence_over_odds_low = float(parameters["confidence_over_odds_low"])
    dataframe = dataframe[dataframe["prob_over_odds"] > confidence_over_odds_low]  # type: ignore
    dataframe = dataframe[dataframe["prob_over_odds"] < confidence_over_odds_high]  # type: ignore

    probability_high = float(int(parameters["probability_high"]) / 100)
    probability_low = float(int(parameters["probability_low"]) / 100)
    dataframe = dataframe[dataframe["prob_pred"] > probability_low]  # type: ignore
    dataframe = dataframe[dataframe["prob_pred"] < probability_high]  # type: ignore

    outcome: List[Any] = parameters["outcome"].split(",")
    outcome = [int(x) for x in outcome]
    dataframe = dataframe[dataframe["prediction"].isin(outcome)]  # type: ignore

    return dataframe  # type: ignore
