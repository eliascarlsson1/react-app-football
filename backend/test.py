from src.data_handling.database_con import get_model_names
from src.model_handling.evaluate_model import generate_model_statistics
from src.data_handling.data_handling_utils import (
    get_all_historical_data_dict,
)

print(get_model_names())
all_historical_data_dict = get_all_historical_data_dict()
generate_model_statistics("Serie A", ["BE2122"])
