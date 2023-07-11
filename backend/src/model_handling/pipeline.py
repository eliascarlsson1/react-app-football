from ..model_handling.apply_model_utils import (
    apply_model_to_df,
    load_training_data_from_model,
    load_x_and_y_parameters_from_model,
)
from ..model_handling.test_model import apply_test_to_df, get_stats_for_model_and_test
from typing import List, Dict, Any
import pandas as pd
from ..data_handling.database_con import get_pipeline_parameters, get_current_year
from ..data_handling.data_handling_utils import load_prepared_scrape
from ..data_handling.dataframes_handling import filter_df_for_leagues


def apply_pipeline(pipeline_name: str) -> pd.DataFrame | None:
    ## Get pipeline parameters
    try:
        pipeline_parameters = get_pipeline_parameters(pipeline_name)
    except:
        print("pipeline not found:", pipeline_name)
        return None
    model: str = pipeline_parameters["model"]
    leagues: List[str] = pipeline_parameters["leagues"]
    test: str = pipeline_parameters["test"]
    print("pipeline_parameters: ", pipeline_parameters)

    ## Load df and create dict
    df = load_prepared_scrape()

    ## Filter df for leagues
    df = filter_df_for_leagues(df, leagues)

    if len(df) == 0:
        print("no games found for leagues:", leagues)
        return None

    ## Apply model
    predicted_games_df = apply_model_to_df(model, df)
    filtered_predicted_game_df = apply_test_to_df(predicted_games_df, test)
    print("filtered_predicted_game_df: ", filtered_predicted_game_df)
    return filtered_predicted_game_df


def get_game_bet_information(row: Any, pipeline_name: str) -> Dict[str, Any]:
    information_dict: Dict[str, Any] = {}
    ## Information from row
    information_dict["homeTeam"] = row["HomeTeam"]
    information_dict["awayTeam"] = row["AwayTeam"]
    information_dict["date"] = row["Date"]
    information_dict["prediction"] = row["prediction"]
    information_dict["oddsPrediction"] = row["odds_pred"]
    information_dict["oddsportalLink"] = row["oddsportal_link"]

    ## Pipeline, model and test parameters
    pipeline_parameters = get_pipeline_parameters(pipeline_name)
    test = pipeline_parameters["test"]

    # Model
    model = pipeline_parameters["model"]
    x_y_parameters = load_x_and_y_parameters_from_model(model)
    training_data = load_training_data_from_model(model)
    model_information = {
        "xParameters": x_y_parameters[0],
        "yParameter": x_y_parameters[1],
        "trainingData": training_data,
    }

    # Stats for model and test
    league = row["league"] + get_current_year()
    stats = get_stats_for_model_and_test([league], model, test)
    stats_league = stats[league]
    information_dict["testDataForLeague"] = stats_league

    information_dict["model"] = model_information
    information_dict["test"] = test
    information_dict["pipelineName"] = pipeline_name

    ## FIXME: Messing stats for scraped games

    ## FIXME: Odds information, refine!
    information_dict["odds"] = {}
    return information_dict


if __name__ == "__main__":
    apply_pipeline("test_pipeline")
