import os
import pandas as pd
from typing import Dict, Any, List
from . import prepare_data_utils as pdu
from . import elo_tilt as et
from ..data_handling.database_con import (
    get_all_X_parameters,
    get_all_Y_parameters,
    get_current_year,
)
from ..create_tables.create_table import create_tables_for_every_date  # type: ignore
from ..scrape.scrape_utils import (
    filter_scrape_for_last_scraped,
    filter_scrape_for_upcoming_games,
    add_average_odds,
)


all_x_par = get_all_X_parameters()
all_y_par = get_all_Y_parameters()

relative_data_path = "../../data"
file_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(file_path, relative_data_path)
relevant_data_path = data_path + "/historical_data/relevant_data"
prepared_data_path = data_path + "/prepared_data"


def prepare_relevant_data(
    all_df_dict: Dict[str, pd.DataFrame], only_current_year: bool, setStatus: Any
) -> str:
    elo_tilt_handler = et.Elo_Tilt_Handler(all_df_dict)
    current_year = get_current_year()

    filenames = os.listdir(relevant_data_path)
    ## Filter filenames to include current year
    if only_current_year:
        filenames = [
            filename for filename in filenames if filename[2:6] == current_year
        ]
    status = 0

    for filename in filenames:
        if len(filename) == 10:
            league = filename[:2]
            year = filename[2:6]
            raw_data = pd.read_csv(relevant_data_path + "/" + filename)  # type: ignore
            dataframe = load_one_season(
                raw_data, league, year, all_df_dict, elo_tilt_handler
            )
            dataframe.to_csv(prepared_data_path + "/" + filename, index=False)
            print("Prepared", filename)
            status += 1
            setStatus(status, len(filenames))

    return "success"


def prepared_scraped_games(
    elo_tilt_handler: et.Elo_Tilt_Handler, all_df_dict: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    # Writes to data/prepared_scrape.csv

    # col_name_to_odds = Dictionary from odds to colname,
    # e.g. Dict["Over/Under +2.5", ["AvgU25", "AvgO25"]] - in the correct order
    odds_to_colname: Dict[str, List[str]] = {}
    odds_to_colname["Over/Under +2.5"] = ["AvgU25", "AvgO25"]
    odds_to_colname["one_x_two"] = ["AvgH", "AvgD", "AvgA"]

    df = pd.read_csv("./data/scrape.csv")  # type: ignore
    df = filter_scrape_for_last_scraped(df)
    df = filter_scrape_for_upcoming_games(df)

    # Adds average odds to df
    for odds, col_names in odds_to_colname.items():
        add_average_odds(df, col_names, odds)

    print(df)

    prepare_scrape_df_rows = []
    for index, row in df.iterrows():  # type: ignore
        row = prepare_scraped_game(
            row["home_team"],  # type: ignore
            row["away_team"],  # type: ignore
            row["game_date"],  # type: ignore
            row["scrape_time"],  # type: ignore
            row["scrape_game_index"],  # type: ignore
            row["AvgO25"],  # type: ignore
            row["AvgU25"],  # type: ignore
            row["AvgH"],  # type: ignore
            row["AvgA"],  # type: ignore
            row["AvgD"],  # type: ignore
            row["Year"],  # type: ignore
            row["League"],  # type: ignore
            all_df_dict,
            elo_tilt_handler,
        )
        prepare_scrape_df_rows.append(row)  # type: ignore

    ## FIXME: WIP
    # Collect all scraped games
    # - Odds over under 2.5, average
    # Change team name to a name that i recognize
    # Return scrape df/ save to file

    print("Not implemented yet")


def prepare_scraped_game(
    HomeTeam: str,
    AwayTeam: str,
    game_date: str,
    scrape_time: str,
    scrape_game_index: str,
    OddsOver: str,
    OddsUnder: str,
    OddsH: str,
    OddsA: str,
    OddsD: str,
    year: str,
    league: str,
    all_df_dict: Dict[str, pd.DataFrame],
    elo_tilt_handler: et.Elo_Tilt_Handler,
) -> pd.DataFrame:
    current_data = pd.read_csv(relevant_data_path + "/" + league + year + ".csv")  # type: ignore
    current_data = pdu.add_simple_features(current_data)

    ## FIXME: Heavy to create table only for this..
    ## FIXME: Assuming the teams to predict did not play this date...
    tables: Any = create_tables_for_every_date(current_data)
    date = list(tables.keys())[-2]

    row_data = pd.DataFrame(
        {
            "HomeTeam": [HomeTeam],
            "AwayTeam": [AwayTeam],
            "AvgO25": [OddsOver],
            "AvgU25": [OddsUnder],
            "AvgA": [OddsA],
            "AvgH": [OddsH],
            "AvgD": [OddsD],
            "Date": [date],
            "GameIndex": ["Predicted_game"],
            "TG": "unknown",
            "FTR": "unknown",
        }
    )

    row_data = pdu.calculate_features_from_table(
        row_data, current_data, league, year, all_df_dict
    )

    # Add elo and tild
    row_data = add_tilt_and_elo(row_data, elo_tilt_handler, league, year)

    # Tidy up the dataframe
    # FIXME: Somehow include bookmaker odds or a game id so i can find bookmaker odds
    row_data["Date"] = game_date
    row_data["ScrapeTime"] = scrape_time

    row_data.to_csv("row_data.csv")
    print(row_data)
    return row_data


def load_one_season(
    raw_data: pd.DataFrame,
    league: str,
    year: str,
    all_df_dict: Dict[str, pd.DataFrame],
    elo_tilt_handler: et.Elo_Tilt_Handler,
) -> pd.DataFrame:
    # Prepare the data
    raw_data = pdu.add_simple_features(raw_data)

    # Calculating features
    raw_data = pd.DataFrame = pdu.calculate_features_from_table(
        raw_data, raw_data, league, year, all_df_dict
    )
    raw_data = add_tilt_and_elo(raw_data, elo_tilt_handler, league, year)

    # Ensure all parameters are in the dataframe
    parameters_to_include = ["GameIndex", "HomeTeam", "AwayTeam", "Date"]
    all_parameters = parameters_to_include + all_x_par + all_y_par
    for par in all_parameters:
        if par not in raw_data.columns:
            raise Exception("{} not in raw_data.columns".format(par))

    prepared_data = raw_data[all_parameters]
    prepared_data = prepared_data.iloc[10:, :]  # removes first games of each season
    return prepared_data


def add_tilt_and_elo(
    raw_data: pd.DataFrame,
    elo_tilt_handler: et.Elo_Tilt_Handler,
    league: str,
    year: str,
) -> pd.DataFrame:
    # fmt: off
    raw_data["tilt_ht"] = raw_data.apply(applyTiltElo, team="HomeTeam", league=league, elo_tilt="tilt", elo_tilt_handler=elo_tilt_handler, axis=1) # type: ignore
    raw_data["tilt_at"] = raw_data.apply(applyTiltElo, team="AwayTeam", league=league, elo_tilt="tilt", elo_tilt_handler=elo_tilt_handler, axis=1) # type: ignore
    raw_data["elo_ht"] = raw_data.apply(applyTiltElo, team="HomeTeam", league=league, elo_tilt="elo", elo_tilt_handler=elo_tilt_handler, axis=1) # type: ignore
    raw_data["elo_at"] = raw_data.apply(applyTiltElo, team="AwayTeam", league=league, elo_tilt="elo", elo_tilt_handler=elo_tilt_handler, axis=1) # type: ignore
    raw_data["win_e_ht"] = raw_data.apply(calculate_win_e, axis=1) # type: ignore
    # fmt: on

    return raw_data


def applyTiltElo(
    row: Any,
    team: str,
    league: str,
    elo_tilt: str,
    elo_tilt_handler: et.Elo_Tilt_Handler,
):
    if elo_tilt == "elo":
        return elo_tilt_handler.get_elo(league, row["Date"], row[team])
    if elo_tilt == "tilt":
        return elo_tilt_handler.get_tilt(league, row["Date"], row[team])


def calculate_win_e(row: Any):
    elo_at = float(row["elo_at"])
    elo_ht = float(row["elo_ht"])
    we_ht = 1 / (1 + 10 ** ((elo_at - (elo_ht + 70)) / 400))
    return we_ht
