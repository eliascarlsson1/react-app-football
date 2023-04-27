import os
from typing import List

# Returns a list of all the historical csv files
def get_historical_data_list() -> List[str]:
    path = "./data/historical_data/relevant_data"
    return os.listdir(path)

