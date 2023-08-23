import pandas as pd
import numpy as np
import copy


def create_empty_table(teams):
    """Creates an empty football league table

    Args:
        teams (ndarray): Array of teams in league

    Outputs:
        table0 (dictionary): Empty table
    """
    table0 = dict()
    emptyteam = {
        "Position": 0,
        "Points": 0,
        "Wins": 0,
        "Played": 0,
        "Draws": 0,
        "Losses": 0,
        "Goals_Scored": 0,
        "Goals_Conceded": 0,
        "Goal_Difference": 0,
    }
    for team in teams:
        table0[team] = dict(emptyteam)

    return table0


def update_positions(table0):
    """Updates the positions in the table

    Args:
        table0 (dict): League table

    Output:
        table0 (dict): Table with updated positions
    """

    team_order = sorted(
        table0.keys(),
        key=lambda x: (table0[x]["Points"], table0[x]["Goal_Difference"]),
        reverse=True,
    )

    for pos, team in enumerate(team_order):
        table0[team]["Position"] = pos + 1

    return table0


def fill_game(game, table0):
    """Fills the table dictionary with the results of one game

    Args:
        game (series): A named series (one row from dataframe) containing a game
        table0 (dict): The league table

    Returns:
        table0 (dict): The league table with game added
    """

    homet = game["HomeTeam"]
    awayt = game["AwayTeam"]

    table0[homet]["Played"] += 1
    table0[awayt]["Played"] += 1
    table0[homet]["Goals_Scored"] += game["FTHG"]
    table0[awayt]["Goals_Scored"] += game["FTAG"]
    table0[homet]["Goals_Conceded"] += game["FTAG"]
    table0[awayt]["Goals_Conceded"] += game["FTHG"]
    table0[homet]["Goal_Difference"] = (
        table0[homet]["Goals_Scored"] - table0[homet]["Goals_Conceded"]
    )
    table0[awayt]["Goal_Difference"] = (
        table0[awayt]["Goals_Scored"] - table0[awayt]["Goals_Conceded"]
    )
    if game["FTHG"] > game["FTAG"]:
        table0[homet]["Points"] += 3
        table0[homet]["Wins"] += 1
        table0[awayt]["Losses"] += 1
    elif game["FTHG"] == game["FTAG"]:
        table0[homet]["Points"] += 1
        table0[awayt]["Points"] += 1
        table0[homet]["Draws"] += 1
        table0[awayt]["Draws"] += 1
    elif game["FTHG"] < game["FTAG"]:
        table0[awayt]["Points"] += 3
        table0[awayt]["Wins"] += 1
        table0[homet]["Losses"] += 1

    return table0


def fill_date(data, date, table0):
    """Fills table for one whole date

    Args:
        data (dataframe): Dataframe containig all matches
        date (string): String containinng date
        table0 (dict): League table

    Output:
        table0 (dict): Update league table
    """

    for index, game in data[data["Date"] == date].iterrows():
        table0 = fill_game(game, table0)

    table0 = update_positions(table0)

    return table0


def create_tables_for_every_date(data):
    """Create tables for every date (table in the morning, before games)
    OBS: It assumes that rows are ordered correctly by dates

    Args:
        data (dataframe): Raw datafile with dates

    Output:
        dateTable (nested nested dict): Dictionay with dates as keys, containing a
                                        for every date
    """

    dates = pd.unique(np.array(data["Date"]))
    dates = np.append(dates, "last_date")

    # Create tables for every date
    dateTables = dict()
    all_home_teams = np.unique(np.array(data["HomeTeam"]))
    all_away_teams = np.unique(np.array(data["AwayTeam"]))
    all_teams = np.unique(np.concatenate([all_home_teams, all_away_teams]))
    table0 = create_empty_table(all_teams)

    for index, date in enumerate(dates):
        if index == 0:
            dateTables[date] = dict(table0)
        else:
            dateTables[date] = fill_date(
                data, dates[index - 1], copy.deepcopy(dateTables[dates[index - 1]])
            )

    return dateTables
