from ..model_handling.apply_model_utils import apply_model_to_df
from ..model_handling.test_model import apply_test_to_df
from typing import Dict, List
import pandas as pd
from ..data_handling.database_con import get_pipeline_parameters
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


if __name__ == "__main__":
    apply_pipeline("test_pipeline")
