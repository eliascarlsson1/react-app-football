# from src.model_handling.test_model import get_roi_for_model_and_test
# from src.data_handling.data_handling_utils import get_historical_data_list

# print(get_roi_for_model_and_test(get_historical_data_list(), "current_model"))

# from src.prepare_data.prepare_data import prepare_relevant_data
# from src.data_handling.data_handling_utils import get_all_historical_data_dict

# def function(status, total):
#     print(status, total)

# df_dict = get_all_historical_data_dict()
# prepare_relevant_data(df_dict, True, function)

# from src.model_handling.manage import save_model

# print(save_model("test_model"))

from src.model_handling.test_model import get_stats_for_model_and_test

print(get_stats_for_model_and_test(["PL2223", "BL2223"], "current_model", "hard test"))
