import pandas as pd
from typing import List, Dict, Any
import json


def filter_scrape_for_upcoming_games(scrape: pd.DataFrame) -> pd.DataFrame:
    time_now = pd.Timestamp.now()
    scrape["datetime"] = pd.to_datetime(scrape["date"] + " " + scrape["time"])  # type: ignore

    # Filter for games that are upcoming
    scrape = scrape[scrape["datetime"] > time_now]
    scrape = scrape.drop(columns=["datetime"])
    return scrape


def filter_scrape_for_last_scraped(scrape: pd.DataFrame) -> pd.DataFrame:
    # Filter scrape to only have one of each id, with the latest scrape_time
    scrape = scrape.sort_values(by=["scrape_time"], ascending=False)  # type: ignore
    scrape = scrape.drop_duplicates(subset=["scrape_game_index"], keep="first")
    return scrape


def get_average_over_under_odds(type: str, encodedJsonObj: str) -> List[float] | None:
    # Returns odds [0, 1]

    try:
        jsonObj = json.loads(encodedJsonObj)
    except:
        print("Could not decode json object")
        return None

    odds = jsonObj.get(type)
    if jsonObj.get(type) == None:
        print("Type not found in json object")
        return None

    list1 = [float(odds[i][0]) for i in odds]
    list2 = [float(odds[i][1]) for i in odds]

    average1 = sum(list1) / len(list1)
    average2 = sum(list2) / len(list2)

    return [average1, average2]


def get_over_under_odds_for_bookmaker(
    type: str, encodedJsonObj: str, bookmaker: str
) -> List[float] | None:
    # Returns odds [0, 1]
    try:
        jsonObj = json.loads(encodedJsonObj)
    except:
        print("Could not decode json object")
        return None

    odds = jsonObj.get(type)
    if jsonObj.get(type) == None:
        print("Type not found in json object")
        return None

    bookmaker_odds = odds.get(bookmaker)
    if bookmaker_odds == None:
        print("Bookmaker not found in json object")
        return None

    return [bookmaker_odds[0], bookmaker_odds[1]]


def get_average_one_x_two_odds(encodedJsonObj: str) -> List[float] | None:
    # Returns odds [0, 1, 2]

    try:
        jsonObj = json.loads(encodedJsonObj)
    except:
        print("Could not decode json object")
        return None

    list1 = [float(jsonObj[i][0]) for i in jsonObj]
    list2 = [float(jsonObj[i][1]) for i in jsonObj]
    list3 = [float(jsonObj[i][2]) for i in jsonObj]

    average1 = sum(list1) / len(list1)
    average2 = sum(list2) / len(list2)
    average3 = sum(list3) / len(list3)

    return [average1, average2, average3]


def get_one_x_two_odds_for_bookmaker(
    encodedJsonObj: str, bookmaker: str
) -> List[float] | None:
    # Returns odds [0, 1, 2]
    try:
        jsonObj = json.loads(encodedJsonObj)
    except:
        print("Could not decode json object")
        return None

    bookmaker_odds = jsonObj.get(bookmaker)
    if bookmaker_odds == None:
        print("Bookmaker not found in json object")
        return None

    return [bookmaker_odds[0], bookmaker_odds[1], bookmaker_odds[2]]


# if __name__ == "__main__":
#     df = pd.read_csv("./data/scrape.csv")  # type: ignore
#     filtered_df = filter_scrape_for_upcoming_games(df)
#     print(filtered_df)
#     filtered_df = filter_scrape_for_last_scraped(filtered_df)
#     print(filtered_df)

#     jsonStr = filtered_df["odds_over_under"].iloc[0]  # type: ignore
#     if type(jsonStr) == str:  # type: ignore
#         b = get_over_under_odds_for_bookmaker("Over/Under +2.5", "test", "Pinnacle")
#         print(b)

#         a = get_average_over_under_odds("Over/Under +2.5", jsonStr)
#         print(a)

#     jsonStr2 = filtered_df["odds_one_x_two"].iloc[0]  # type: ignore
#     if type(jsonStr2) == str:  # type: ignore
#         c = get_average_one_x_two_odds(jsonStr2)
#         print(c)

#         d = get_one_x_two_odds_for_bookmaker(jsonStr2, "Pinnacle")
#         print(d)


# Apply functions to dataframe
def add_average_odds(df: pd.DataFrame, col_names: List[str], odds: str):
    add_to_df_dict: Dict[str, List[float]] = {}
    for col_name in col_names:
        add_to_df_dict[col_name] = []

    for index, row in df.iterrows():  # type: ignore
        avgs = get_avg_odds_for_odds(row, odds)
        if avgs == None:
            print("Could not get average odds for: ", odds)
            return

        for i in range(len(col_names)):
            avg = avgs[i]
            add_to_df_dict[col_names[i]].append(avg)

    for col_name in col_names:
        values = add_to_df_dict[col_name]
        df[col_name] = values


def get_avg_odds_for_odds(row: Any, odds: str) -> List[float] | None:
    if odds.startswith("Over/Under"):
        jsonStr: str = row["odds_over_under"]  # type: ignore
        if type(jsonStr) != str:  # type: ignore
            print("Could not read json object from dataframe: ", jsonStr)  # type: ignore
            return None
        avgs = get_average_over_under_odds(odds, jsonStr)
        return avgs

    if odds == "one_x_two":
        jsonStr = row["odds_one_x_two"]  # type: ignore
        if type(jsonStr) != str:  # type: ignore
            print("Could not read json object from dataframe: ", jsonStr)  # type: ignore
            return None
        avgs = get_average_one_x_two_odds(jsonStr)
        return avgs
