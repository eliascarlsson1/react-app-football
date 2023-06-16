from src.prepare_data.prepare_data import prepare_scraped_game, prepare_relevant_data
from src.data_handling.data_handling_utils import get_all_historical_data_dict


### Variables ###
all_historical_data_dict = get_all_historical_data_dict()

# prepare_scraped_game(
#     "Chelsea",
#     "Brentford",
#     "27/04/2023",
#     "OddsOver",
#     "OddsUnder",
#     "OddsH",
#     "OddsA",
#     "OddsD",
#     "2223",
#     "PL",
#     all_df_dict=all_historical_data_dict,
# )


prepare_relevant_data(all_df_dict=all_historical_data_dict, only_current_year=True, setStatus=print)