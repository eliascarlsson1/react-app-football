import os
import pandas as pd
from src.scrape.scrape_utils import get_bookmaker_to_over_under_odds


script_dir = os.path.dirname(__file__)
relative_path_scrape = "../../data/scrape.csv"
scrape_path = os.path.join(script_dir, relative_path_scrape)


def analyse_historical_odds():
    scrape_df: pd.DataFrame = pd.read_csv(scrape_path)  # type: ignore
    over_under_25_dics = []
    for index, row in scrape_df.iterrows():  # type: ignore
        print(index)
        dict = get_bookmaker_to_over_under_odds("Over/Under +2.5", row["odds_over_under"])  # type: ignore
        over_under_25_dics.append(dict)  # type: ignore

    print(over_under_25_dics)
