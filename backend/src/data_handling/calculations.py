import pandas as pd
import math

# Requirments on dataframes is that prediction, y_par and odds (for prediction) exist


# Returns ROI in percantage relative to 100, betting 1 on all games
def calculate_basic_roi(dataframe: pd.DataFrame, y_par: str) -> float | str:
    if len(dataframe) == 0:
        return "Empty dataframe"

    if "prediction" not in dataframe.columns:
        return "No prediction column found"

    if y_par not in dataframe.columns:
        return "No y parameter column found"

    if "odds_pred" not in dataframe.columns:
        return "No odds column found"

    roi_df: pd.DataFrame = dataframe[["prediction", y_par, "odds_pred"]]
    money_bet = 0
    money_returned = 0
    for index, row in roi_df.iterrows():  # type: ignore
        odds = float(row["odds_pred"])  # type: ignore
        if math.isnan(odds):
            continue
        money_bet += 1
        if row["prediction"] == row[y_par]:
            money_returned += odds

    return 100 * money_returned / money_bet - 100
