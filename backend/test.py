from src.create_tables.create_table import create_tables_for_every_date  # type: ignore
from src.prepare_data.prepare_data_utils import load_one_season_test  # type: ignore
from src.train_model.train_model import train_model  # type: ignore
import pandas as pd

raw_data: pd.DataFrame = pd.read_csv("./backend/data/historical_data/relevant_data/PL2021.csv")  # type: ignore

# print(create_tables_for_every_date(raw_data)) # type: ignore

print(load_one_season_test(raw_data, "PL", "2021"))