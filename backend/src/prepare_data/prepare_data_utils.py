import pandas as pd
import os
from typing import Any, Dict
from ..create_tables.create_table import create_tables_for_every_date  # type: ignore

script_dir = os.path.dirname(__file__)
relative_path_all_data = "../../data/historical_data/all_data"
all_data_path = os.path.join(script_dir, relative_path_all_data)


def add_simple_features(raw_data: pd.DataFrame) -> pd.DataFrame:
    ## Add simple features, y parameters for example.
    raw_data["TG"] = raw_data["FTHG"] + raw_data["FTAG"]
    raw_data["GameIndex"] = (
        raw_data["Date"] + raw_data["HomeTeam"] + raw_data["AwayTeam"]
    )
    raw_data = raw_data.assign(OvUn25=[1 if TG > 2.5 else 0 for TG in raw_data["TG"]])  # type: ignore

    if not ("Avg>2.5" in raw_data.columns):
        raw_data["AvgO25"] = raw_data["BbAv>2.5"]
        raw_data["AvgU25"] = raw_data["BbAv<2.5"]
    else:
        raw_data["AvgO25"] = raw_data["Avg>2.5"]
        raw_data["AvgU25"] = raw_data["Avg<2.5"]

    if not ("AvgA" in raw_data.columns):
        raw_data["AvgA"] = raw_data["BbAvA"]
        raw_data["AvgH"] = raw_data["BbAvH"]
        raw_data["AvgD"] = raw_data["BbAvD"]

    return raw_data


def calculate_features_from_table(
    raw_data: pd.DataFrame, league: str, year: str, all_df_dict: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    tables: Any = create_tables_for_every_date(raw_data)
    # fmt: off
    raw_data["Played"] = raw_data.apply(played_avg, tables=tables, axis=1)  # type: ignore
    raw_data["HtPos"] = raw_data.apply(position, team="HomeTeam", tables=tables, axis=1)  # type: ignore
    raw_data["AtPos"] = raw_data.apply(position, team="AwayTeam", tables=tables, axis=1)  # type: ignore
    raw_data["HtSGLG"] = raw_data.apply(glg, team="HomeTeam", s_or_c="Goals_Scored", data=raw_data, axis=1)  # type: ignore
    raw_data["AtSGLG"] = raw_data.apply(glg, team="AwayTeam", s_or_c="Goals_Scored", data=raw_data, axis=1)  # type: ignore
    raw_data["HtCGLG"] = raw_data.apply(glg, team="HomeTeam", s_or_c="Goals_Conceded", data=raw_data, axis=1)  # type: ignore
    raw_data["AtCGLG"] = raw_data.apply(glg, team="AwayTeam", s_or_c="Goals_Conceded", data=raw_data, axis=1)  # type: ignore
    raw_data["HtASGPG"] = raw_data.apply(average_scored_gpg, team="HomeTeam", tables=tables, axis=1)  # type: ignore
    raw_data["AtASGPG"] = raw_data.apply(average_scored_gpg, team="AwayTeam", tables=tables, axis=1)  # type: ignore
    raw_data["HtACGPG"] = raw_data.apply(average_conceded_gpg, team="HomeTeam", tables=tables, axis=1) # type: ignore
    raw_data["AtACGPG"] = raw_data.apply(average_conceded_gpg, team="AwayTeam", tables=tables, axis=1) # type: ignore
    raw_data["HtASGP5G"] = raw_data.apply(average_scored_gp5g, team="HomeTeam", tables=tables, data=raw_data, axis=1) # type: ignore
    raw_data["AtASGP5G"] = raw_data.apply(average_scored_gp5g, team="AwayTeam", tables=tables, data=raw_data, axis=1) # type: ignore
    raw_data["HtACGP5G"] = raw_data.apply(average_conceded_gp5g, team="HomeTeam", tables=tables, data=raw_data, axis=1) # type: ignore
    raw_data["AtACGP5G"] = raw_data.apply(average_conceded_gp5g, team="AwayTeam", tables=tables, data=raw_data, axis=1) # type: ignore
    raw_data["HtASGP3G"] = raw_data.apply(average_gp3g, team="HomeTeam", s_or_c="Goals_Scored", tables=tables, data=raw_data, axis=1) # type: ignore
    raw_data["AtASGP3G"] = raw_data.apply(average_gp3g, team="AwayTeam", s_or_c="Goals_Scored", tables=tables, data=raw_data, axis=1) # type: ignore
    raw_data["HtACGP3G"] = raw_data.apply(average_gp3g, team="HomeTeam", s_or_c="Goals_Conceded", tables=tables, data=raw_data, axis=1) # type: ignore
    raw_data["AtACGP3G"] = raw_data.apply(average_gp3g, team="AwayTeam", s_or_c="Goals_Conceded", tables=tables, data=raw_data, axis=1) # type: ignore
    raw_data["HtpercentGO"] = raw_data.apply(percent_games_over, team="HomeTeam", data=raw_data, axis=1) # type: ignore
    raw_data["AtpercentGO"] = raw_data.apply(percent_games_over, team="AwayTeam", data=raw_data, axis=1) # type: ignore
    # fmt: on
    dict_keys = []
    for filename in os.listdir(all_data_path):  # type: ignore
        if filename[0:2] == league:
            if int(year) >= int(filename[2:6]):  # type: ignore
                dict_keys.append(filename[0:6])  # type: ignore
    raw_data["AGTM"] = raw_data.apply(  # type: ignore
        average_goals_this_matchup,
        dict_keys=dict_keys,
        year=year,
        axis=1,
        all_df_dict=all_df_dict,
    )

    return raw_data


# Calculate from table
def position(row: Any, team: str, tables: Any, option: bool = False) -> int:
    # Position of HT or AT
    # team = "HomeTeam" or "AwayTeam"
    if option:
        return (tables["last_date"])[row[team]]["Position"]

    return (tables[row.Date])[row[team]]["Position"]


def played_avg(row: Any, tables: Any):
    return (
        tables[row.Date][row.HomeTeam]["Played"]
        + tables[row.Date][row.AwayTeam]["Played"]
    ) / 2


def glg(row: Any, team: str, data: pd.DataFrame, s_or_c: str):  # type: ignore
    # How many goals did the team score last game

    # Slicing the data to only include games up until this game
    dataslice = data.iloc[0 : (list(data.Date).index(row.Date))]  # type: ignore

    # Return 0 if no previous game
    if (row[team] not in list(dataslice["HomeTeam"])) and (  # type: ignore
        row[team] not in list(dataslice["AwayTeam"])  # type: ignore
    ):
        return 0

    filtered = dataslice[  # type: ignore
        (dataslice["HomeTeam"] == row[team]) | (dataslice["AwayTeam"] == row[team])
    ]
    newrow = filtered.iloc[-1]  # type: ignore

    if row[team] == newrow["HomeTeam"]:
        if s_or_c == "Goals_Conceded":
            return newrow["FTAG"]  # type: ignore
        if s_or_c == "Goals_Scored":
            return newrow["FTHG"]  # type: ignore
    elif row[team] == newrow["AwayTeam"]:
        if s_or_c == "Goals_Conceded":
            return newrow["FTHG"]  # type: ignore
        if s_or_c == "Goals_Scored":
            return newrow["FTAG"]  # type: ignore


def average_scored_gpg(row: Any, team: str, tables: Any):
    # Average goals scored this season
    if tables[row.Date][row[team]]["Played"] == 0:
        return 0
    else:
        return (
            tables[row.Date][row[team]]["Goals_Scored"]
            / tables[row.Date][row[team]]["Played"]
        )


def average_conceded_gpg(row: Any, team: str, tables: Any):
    # Average goals scored this season
    if tables[row.Date][row[team]]["Played"] == 0:
        return 0
    else:
        return (
            tables[row.Date][row[team]]["Goals_Conceded"]
            / tables[row.Date][row[team]]["Played"]
        )


def average_scored_gp5g(row: Any, team: str, tables: Any, data: pd.DataFrame):
    # Average goals scoared last five games

    dataslice = data.iloc[0 : (list(data.Date).index(row.Date))]  # type: ignore

    # Games played in table
    played = tables[row.Date][row[team]]["Played"]
    if played == 0:
        return 0
    games_back = 5 if played > 5 else (played)

    for date in dataslice.Date:  # type: ignore
        if tables[date][row[team]]["Played"] == played - games_back:
            return (
                tables[row.Date][row[team]]["Goals_Scored"]
                - tables[date][row[team]]["Goals_Scored"]
            ) / (games_back)

    return 0


def average_conceded_gp5g(row: Any, team: str, tables: Any, data: pd.DataFrame):
    # Average goals scoared last five games

    dataslice = data.iloc[0 : (list(data.Date).index(row.Date))]  # type: ignore

    # Games played in table
    played = tables[row.Date][row[team]]["Played"]
    if played == 0:
        return 0
    games_back = 5 if played > 5 else (played)

    for date in dataslice.Date:  # type: ignore
        if tables[date][row[team]]["Played"] == played - games_back:
            return (
                tables[row.Date][row[team]]["Goals_Conceded"]
                - tables[date][row[team]]["Goals_Conceded"]
            ) / (games_back)

    return 0


def average_gp3g(row: Any, team: str, s_or_c: str, tables: Any, data: pd.DataFrame):
    # Average goals scoared last five games

    dataslice = data.iloc[0 : (list(data.Date).index(row.Date))]  # type: ignore

    # Games played in table
    played = tables[row.Date][row[team]]["Played"]
    if played == 0:
        return 0
    games_back = 3 if played > 3 else (played)

    for date in dataslice.Date:  # type: ignore
        if tables[date][row[team]]["Played"] == played - games_back:
            return (
                tables[row.Date][row[team]][s_or_c] - tables[date][row[team]][s_or_c]
            ) / (games_back)

    return 0


def average_goals_this_matchup(
    row: Any, dict_keys: list[str], year: str, all_df_dict: Dict[str, pd.DataFrame]
):
    # Problem... returns 0 if never met before and dates...

    teams = [row["HomeTeam"], row["AwayTeam"]]
    total_goals = []
    for key in dict_keys:  # type: ignore
        season = all_df_dict[key]  # type: ignore
        if key[2:6] == year:
            season = season[0 : season[season.Date == row["Date"]].index[0]]
            results = season.loc[  # type: ignore
                ((teams[0] == season["HomeTeam"]) | (teams[0] == season["AwayTeam"]))
                & ((teams[1] == season["HomeTeam"]) | (teams[1] == season["AwayTeam"]))
            ]
            TG = results["FTHG"] + results["FTAG"]  # type: ignore
            total_goals.extend(TG)  # type: ignore
        else:
            results = season.loc[  # type: ignore
                ((teams[0] == season["HomeTeam"]) | (teams[0] == season["AwayTeam"]))
                & ((teams[1] == season["HomeTeam"]) | (teams[1] == season["AwayTeam"]))
            ]
            TG = results["FTHG"] + results["FTAG"]  # type: ignore
            total_goals.extend(TG)  # type: ignore

    if not len(total_goals) == 0:
        return sum(total_goals) / len(total_goals)
    else:
        return 0


def percent_games_over(row: Any, team: str, data: pd.DataFrame):  # type: ignore
    dataslice = data.iloc[0 : (list(data.Date).index(row.Date))]  # type: ignore

    # Return 0 if no previous game
    if (row[team] not in list(dataslice["HomeTeam"])) and (  # type: ignore
        row[team] not in list(dataslice["AwayTeam"])  # type: ignore
    ):
        return 0.5

    filtered = dataslice[  # type: ignore
        (dataslice["HomeTeam"] == row[team]) | (dataslice["AwayTeam"] == row[team])
    ]
    perc = filtered.apply(lambda x: 1 if x["TG"] > 2.5 else 0, axis=1).sum() / len(  # type: ignore
        filtered  # type: ignore
    )
    return perc  # type: ignore
