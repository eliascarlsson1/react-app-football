from src.prepare_data.elo import EloHandler
from src.data_handling.data_handling_utils import get_all_historical_data_dict

all_df_dict = get_all_historical_data_dict()
elo_handler = EloHandler(all_df_dict)
print(elo_handler.get_all_dict_keys())
