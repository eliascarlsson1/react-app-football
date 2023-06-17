from src.prepare_data.prepare_data import prepare_scraped_game, prepared_scraped_games
from src.data_handling.data_handling_utils import get_all_historical_data_dict


### Variables ###
all_historical_data_dict = get_all_historical_data_dict()

prepared_scraped_games(all_df_dict=all_historical_data_dict)
