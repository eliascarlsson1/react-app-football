import os
import pandas as pd
import datetime
from typing import List, Dict, Any
import numpy as np
from src.scrape.scrape_utils import get_bookmaker_to_over_under_odds
from ..data_handling.database_con import (
    get_historical_data_name_from_oddsportal_name,
    get_my_bookmakers,
)
from ..data_handling.calculations import calculate_basic_roi


script_dir = os.path.dirname(__file__)
relative_path_scrape = "../../data/scrape.csv"
scrape_path = os.path.join(script_dir, relative_path_scrape)


def filter_predicted_scrapes_by_odds(
    predicted_games: pd.DataFrame,
    nof_odds_cutoff: int,
    perc_over_mean_cutoff: float,
    stds_over_mean_cutoff: float,
) -> pd.DataFrame:
    # Returns a dataframe with the same column + two more columns: best_bookmaker and odds
    columns = predicted_games.columns.tolist()
    columns.extend(["best_bookmaker", "odds"])

    filtered_games_list = []

    for index, row in predicted_games.iterrows():  # type: ignore
        scrape_game_id: str = row["ScrapeGameIndex"]  # type: ignore
        prediction = row["prediction"]  # type: ignore
        result = analyze_scrape_odds(
            scrape_game_id,  # type: ignore
            prediction,  # type: ignore
            nof_odds_cutoff,
            perc_over_mean_cutoff,
            stds_over_mean_cutoff,
        )
        row["best_bookmaker"] = result["best_bookmaker"]
        row["odds"] = result["odds"]
        if result["pass"]:
            filtered_games_list.append(row)  # type: ignore

    filtered_predicted_games = pd.DataFrame(filtered_games_list, columns=columns)

    return filtered_predicted_games


# Analyze the odds scraped from oddsportal, returns best bookmaker, odds and if it passes filter
def analyze_scrape_odds(
    scrape_game_id: str,
    prediction: int,
    nof_odds_cutoff: int,
    perc_over_mean_cutoff: float,
    stds_over_mean_cutoff: float,
) -> Dict[str, Any]:
    scrape_df = pd.read_csv(scrape_path)  # type: ignore
    scrape_game = scrape_df.loc[scrape_df["scrape_game_index"] == scrape_game_id]  # type: ignore
    if scrape_game.empty:  # type: ignore
        return {
            "best_bookmaker": "error",
            "odds": "error",
            "pass": False,
        }
    dict = get_bookmaker_to_over_under_odds(
        "Over/Under +2.5", scrape_game.iloc[0]["odds_over_under"]  # type: ignore
    )
    if dict == None:
        print("Did not find dict")
        return {
            "best_bookmaker": "error",
            "odds": "error",
            "pass": False,
        }

    predictionString = "Over" if prediction == 1 else "Under"
    best_odds_result = find_best_odds_with_statistics(dict, predictionString, False)
    if best_odds_result == None:
        return {
            "best_bookmaker": "error",
            "odds": "error",
            "pass": False,
        }
    (
        best_bookmaker,
        odds,
        num_available_odds,
        perc_over_mean,
        stds_over_mean,
    ) = best_odds_result
    game_pass = True
    if num_available_odds < nof_odds_cutoff:
        game_pass = False
    if perc_over_mean < perc_over_mean_cutoff:
        game_pass = False
    if stds_over_mean < stds_over_mean_cutoff:
        game_pass = False
    return {
        "best_bookmaker": best_bookmaker,
        "odds": odds,
        "pass": game_pass,
    }


## FIXME: Assumes Over Under +2.5
def analyse_historical_odds(
    all_games_df: pd.DataFrame,
    prediction: int,
    bookmakers: List[str] | None,
    nof_odds_cutoff: int,
    perc_over_mean_cutoff: float,
    stds_over_mean_cutoff: float,
    odds_type: str = "Over/Under +2.5",
):
    scrape_df: pd.DataFrame = pd.read_csv(scrape_path)  # type: ignore
    tg_and_odds: List[tuple[str, Dict[str, List[float]]]] = []
    for index, row in scrape_df.iterrows():  # type: ignore
        historical_game = get_historical_game(all_games_df, row["home_team"], row["away_team"], row["date"])  # type: ignore
        if historical_game.empty:
            continue
        total_goals = historical_game["FTHG"].iloc[0] + historical_game["FTAG"].iloc[0]  # type: ignore
        dict = get_bookmaker_to_over_under_odds(odds_type, row["odds_over_under"])  # type: ignore
        if dict == None:
            continue
        tg_and_odds.append((total_goals, dict))  # type: ignore

    if len(tg_and_odds) / len(scrape_df) < 0.3:
        print("Not enough data to analyse odds")
        return

    y_par = "OvUn25" if odds_type == "Over/Under +2.5" else "OvUn35"
    roi_dataframe = pd.DataFrame(columns=["prediction", y_par, "odds_pred"])

    best_bookmakers = []
    for total_goals, dict in tg_and_odds:
        # Find best odds
        predictionString = "Over" if prediction == 1 else "Under"
        best_odds_result = find_best_odds_with_statistics(dict, predictionString, False)
        if best_odds_result == None:
            continue
        (
            best_bookmaker,
            odds,
            num_available_odds,
            perc_over_mean,
            stds_over_mean,
        ) = best_odds_result
        # print (best_bookmaker, odds, num_available_odds, perc_over_mean, stds_over_mean)
        best_bookmakers.append(best_bookmaker)  # type: ignore
        if num_available_odds < nof_odds_cutoff:
            continue
        if perc_over_mean < perc_over_mean_cutoff:
            continue
        if stds_over_mean < stds_over_mean_cutoff:
            continue

        if bookmakers != None and best_bookmaker not in bookmakers:
            continue

        result = 1 if float(total_goals) > 2.5 else 0
        # Add row to dataframe
        datframe_row = pd.DataFrame(
            [[prediction, result, odds]],
            columns=["prediction", y_par, "odds_pred"],
        )
        roi_dataframe = pd.concat([roi_dataframe, datframe_row])  # type: ignore

    # Print histogram of best bookmakers
    print("Histogram of best bookmakers")
    print(len(pd.Series(best_bookmakers)))
    print(pd.Series(best_bookmakers).value_counts())

    # Round to 2 decimals
    percentage_game_bet_on = len(roi_dataframe) / len(tg_and_odds) * 100
    print(
        "Percentage of games bet on",
        round(percentage_game_bet_on, 2),
        "% (",
        len(roi_dataframe),
        "/",
        len(tg_and_odds),
        ")",
    )
    print("ROI: ", calculate_basic_roi(roi_dataframe, y_par))  # type: ignore


def find_best_odds_with_statistics(
    odds_dict: dict[str, List[float]],
    over_under: str,
    only_ony_my_bookmakers: bool = True,
) -> tuple[str, float, float, float, float] | None:
    # Returns bookmaker, odds, number of available odds, percentage over mean, stds over mean

    bookmakers_to_include = get_my_bookmakers()
    best_odds = 0
    best_bookmaker = ""
    all_odds = []

    for bookmaker, odds in odds_dict.items():
        if over_under == "Under":
            all_odds.append(float(odds[0]))  # type: ignore
            if float(odds[0]) > best_odds:
                if only_ony_my_bookmakers and bookmaker not in bookmakers_to_include:
                    continue
                best_odds = float(odds[0])
                best_bookmaker = bookmaker
        elif over_under == "Over":
            all_odds.append(float(odds[1]))  # type: ignore
            if float(odds[1]) > best_odds:
                if only_ony_my_bookmakers and bookmaker not in bookmakers_to_include:
                    continue
                best_odds = float(odds[1])
                best_bookmaker = bookmaker

    if best_odds == 0:
        return None

    ## Number of available odds
    num_available_odds = len(all_odds)

    ## Calculating mean
    mean = sum(all_odds) / len(all_odds)
    perc_over_mean = (best_odds - mean) / mean * 100

    ## Calculating stds
    std: float = np.std(all_odds)  # type: ignore
    stds_over_mean = (best_odds - mean) / std

    return (
        best_bookmaker,
        best_odds,
        num_available_odds,
        perc_over_mean,
        stds_over_mean,
    )


def get_historical_game(
    all_games_df: pd.DataFrame, home_team: str, away_team: str, date: str
) -> pd.DataFrame:
    historical_ht = get_historical_data_name_from_oddsportal_name(home_team)
    historical_at = get_historical_data_name_from_oddsportal_name(away_team)
    # Get the day of the game formatted yyyy-mm-dd
    date = date.split(",")[0]
    # Format date to match 13/08/2022
    date = datetime.datetime.strptime(date, "%d %b %Y").strftime("%d/%m/%Y")

    # Get the game from the dataframe
    game = all_games_df.loc[
        (all_games_df["HomeTeam"] == historical_ht)
        & (all_games_df["AwayTeam"] == historical_at)
        & (all_games_df["Date"] == date)
    ]

    if len(game) == 1:
        return game
    else:
        return pd.DataFrame()
