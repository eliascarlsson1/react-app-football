from src.prepare_data.prepare_data import prepare_relevant_data
from src.data_handling.data_handling_utils import (
    get_all_historical_data_dict,
)

all_historical_data_dict = get_all_historical_data_dict()


def setPrepareDataStatus(newStatus: int, newTotal: int):
    prepareDataStatus = newStatus
    prepareDataTotal = newTotal


prepare_relevant_data(all_historical_data_dict, True, setPrepareDataStatus)
