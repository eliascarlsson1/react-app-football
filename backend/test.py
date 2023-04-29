# from src.prepare_data.prepare_data import prepare_relevant_data
# from src.data_handling.data_handling_utils import get_all_historical_data_dict


# all_df_dict = get_all_historical_data_dict()
# prepare_relevant_data(all_df_dict)


# from src.data_handling.database_con import get_current_year
# print(get_current_year())

# from src.scraping.update_csv import update_leagues

# update_leagues()

from src.model_handling.train_model import save_model
# from src.data_handling.database_con import add_delete_model, get_model_names

print(save_model("test1"))
