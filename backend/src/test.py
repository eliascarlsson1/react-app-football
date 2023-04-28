from create_tables.create_table import create_tables_for_every_date  # type: ignore
import pandas as pd

raw_data: pd.DataFrame = pd.read_csv("./backend/data/historical_data/relevant_data/PL2021.csv")  # type: ignore

print(create_tables_for_every_date(raw_data))
