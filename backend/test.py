from src.scrape.odds_analysis import analyse_historical_odds
from src.data_handling.data_handling_utils import (
    get_all_historical_data_dict,
    concatenate_df_dict,
    get_historical_data_list,
)

all_historical_data_dict = get_all_historical_data_dict()
historical_data_list = get_historical_data_list()
all_games_in_one_df = concatenate_df_dict(
    all_historical_data_dict, historical_data_list
)
## print names of headers and number of rows
# get first row and date


analyse_historical_odds(
    all_games_df=all_games_in_one_df,
    odds_type="Over/Under +2.5",
    prediction=1,
    # bookmakers=["bet365", "Pinnacle", "William Hill"],
    bookmakers=["Pinnacle"],
    nof_odds_cutoff=0,
    perc_over_mean_cutoff=0,
    stds_over_mean_cutoff=0,
)
