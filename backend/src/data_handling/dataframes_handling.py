import pandas as pd
from typing import List


# Assumes prediction column
# FIXME: y_par
def add_odds_pred(dataframe: pd.DataFrame, odds0: str, odds1: str) -> pd.DataFrame:
    if len(dataframe) == 0:
        raise Exception("Empty dataframe")
    if (odds0 not in dataframe.columns) or (odds1 not in dataframe.columns):
        raise Exception("Odds column not found")
    if "prediction" not in dataframe.columns:
        raise Exception("Prediction column not found")
    if "odds_pred" in dataframe.columns:
        raise Exception("Odds prediction column already exists")

    odds: List[str] = []
    for index, row in dataframe.iterrows():  # type: ignore
        if row["prediction"] == 0:
            odds.append(row[odds0])  # type: ignore
        else:
            odds.append(row[odds1])  # type: ignore

    dataframe["odds_pred"] = odds

    return dataframe
