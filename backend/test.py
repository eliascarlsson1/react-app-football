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


all_games_df = all_games_in_one_df
odds_type = "Over/Under +2.5"
bookmakers = ["bet365", "Pinnacle", "William Hill", "Unibet"]
nof_odds_cutoff = 8
perc_over_mean_cutoff = 2
stds_over_mean_cutoff = 1

print("--------------------")
print("Prediction: Under")
analyse_historical_odds(
    all_games_df = all_games_df,
    prediction = 0,
    bookmakers = bookmakers,
    nof_odds_cutoff = nof_odds_cutoff,
    perc_over_mean_cutoff = perc_over_mean_cutoff,
    stds_over_mean_cutoff = stds_over_mean_cutoff,
)

print("--------------------")
print("Prediction: Over")
analyse_historical_odds(
    all_games_df = all_games_df,
    prediction = 1,
    bookmakers = bookmakers,
    nof_odds_cutoff = nof_odds_cutoff,
    perc_over_mean_cutoff = perc_over_mean_cutoff,
    stds_over_mean_cutoff = stds_over_mean_cutoff,
)
