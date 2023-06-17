from src.prepare_data.prepare_data import prepare_scraped_game, prepared_scraped_games
from src.data_handling.data_handling_utils import get_all_historical_data_dict
from src.prepare_data import elo_tilt as et


### Variables ###
all_historical_data_dict = get_all_historical_data_dict()
elo_tilt_handler = et.Elo_Tilt_Handler(all_historical_data_dict)

prepared_scraped_games(
    elo_tilt_handler=elo_tilt_handler, all_df_dict=all_historical_data_dict
)
