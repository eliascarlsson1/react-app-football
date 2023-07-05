# import pandas as pd
# from typing import List, Dict, Any
# from scrape_utils import filter_scrape_for_upcoming_games, filter_scrape_for_last_scraped, get_over_under_odds


# def get_odds_stats(oddsDict: Dict[]): Dict[str, float]

# if __name__ == "__main__":
#     df = pd.read_csv("./data/scrape.csv")  # type: ignore
#     filtered_df = filter_scrape_for_upcoming_games(df)
#     filtered_df = filter_scrape_for_last_scraped(filtered_df)

#     jsonStr = filtered_df["odds_over_under"].iloc[0]  # type: ignore
#     if type(jsonStr) == str:  # type: ignore
#         b = get_over_under_odds("Over/Under +2.5", jsonStr)
#         print(b)
