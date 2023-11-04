import sqlite3
import os
import json
from typing import List, Any, Dict

script_dir = os.path.dirname(__file__)
path_to_db = "../../data/db.sqlite"
database_abs_path = os.path.join(script_dir, path_to_db)


def get_all_X_parameters() -> List[str]:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM parameters WHERE xnoty = 1")
    results = cursor.fetchall()
    names: List[str] = [result[0] for result in results]
    return names


def get_all_Y_parameters() -> List[str]:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM parameters WHERE xnoty = 0")
    results = cursor.fetchall()
    names: List[str] = [result[0] for result in results]
    return names


def get_all_league_ids() -> List[str]:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute("SELECT id FROM leagues")
    results = cursor.fetchall()
    ids: List[str] = [result[0] for result in results]
    return ids


def get_all_league_ids_to_names() -> Dict[str, str]:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute("SELECT id, name FROM leagues")
    results = cursor.fetchall()
    ids_to_names: Dict[str, str] = {result[0]: result[1] for result in results}
    return ids_to_names


def get_current_year() -> str:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM current_year")
    results = cursor.fetchall()
    year = results[0][0]
    return year


def get_model_names() -> List[str]:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM models")
    results = cursor.fetchall()
    names: List[str] = [result[0] for result in results]
    return names


def add_delete_model(add: bool, name: str) -> None:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    if add:
        if name in get_model_names():
            raise ValueError("Model name already exists")
        cursor.execute("INSERT INTO models (name) VALUES (?)", (name,))
    else:
        if name not in get_model_names():
            raise ValueError("Model name does not exist")
        cursor.execute("DELETE FROM models WHERE name = ?", (name,))
    con.commit()
    con.close()


def get_my_bookmakers() -> List[str]:
    # FIXME: Add to database
    return ["bet365", "Pinnacle", "William Hill", "Unibet"]


def get_test_names() -> List[str]:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM tests")
    results = cursor.fetchall()
    names: List[str] = [result[0] for result in results]
    return names


def delete_test(name: str) -> str:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    if name not in get_test_names():
        return "Test name does not exist"
    cursor.execute("DELETE FROM tests WHERE name = ?", (name,))
    con.commit()
    con.close()
    return "success"


def add_test(
    name: str,
    odds_high: float,
    odds_low: float,
    confidence_over_odds_high: float,
    confidence_over_odds_low: float,
    probability_low: float,
    probability_high: float,
    outcome: str,
) -> None:
    if name in get_test_names():
        if name == "current":
            delete_test("current")
        else:
            raise ValueError("Test name already exists")

    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute(
        """INSERT INTO tests (name, odds_high, odds_low, confidence_over_odds_high,
                   confidence_over_odds_low, probability_low, probability_high, outcome)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            name,
            odds_high,
            odds_low,
            confidence_over_odds_high,
            confidence_over_odds_low,
            probability_low,
            probability_high,
            outcome,
        ),
    )
    con.commit()
    con.close()


def get_test_parameters(test_name: str) -> Dict[str, Any]:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tests WHERE name = ?", (test_name,))
    results = cursor.fetchall()
    if len(results) == 0:
        raise ValueError("Test name does not exist")
    return_dict: Dict[str, Any] = {}
    return_dict["name"] = results[0][0]
    return_dict["odds_high"] = results[0][1]
    return_dict["odds_low"] = results[0][2]
    return_dict["confidence_over_odds_high"] = results[0][3]
    return_dict["confidence_over_odds_low"] = results[0][4]
    return_dict["probability_low"] = results[0][6]
    return_dict["probability_high"] = results[0][5]
    return_dict["outcome"] = results[0][7]
    return return_dict


def get_league_id_from_country_tournament(country: str, tournament: str) -> str | None:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute(
        "SELECT id FROM leagues WHERE oddsportal_country = ? AND oddsportal_tournament = ?",
        (country, tournament),
    )
    results = cursor.fetchall()
    if len(results) == 0:
        print("Can not find league", country, tournament)
        return
    return results[0][0]


def get_country_and_tournament_from_league_id(league: str) -> List[str] | None:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute(
        "SELECT oddsportal_country, oddsportal_tournament FROM leagues WHERE id = ?",
        (league,),
    )
    results = cursor.fetchall()
    if len(results) == 0:
        print("Can not find league", league)
        return
    return [results[0][0], results[0][1]]


def get_historical_data_name_from_oddsportal_name(team_name: str) -> str:
    # I have a table called team_name with historica_data_name and oddsportal_name

    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute(
        "SELECT historical_data_name FROM team_name WHERE oddsportal_name = ?",
        (team_name,),
    )
    results = cursor.fetchall()
    if len(results) == 0:
        return team_name
    return results[0][0]


def get_pipeline_names():
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM pipelines")
    results = cursor.fetchall()
    names: List[str] = [result[0] for result in results]
    return names


def get_pipeline_parameters(pipelineName: str) -> Dict[str, Any]:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM pipelines WHERE name = ?", (pipelineName,))
    results = cursor.fetchall()
    if len(results) == 0:
        raise ValueError("Pipeline name does not exist")
    return_dict: Dict[str, Any] = {}
    return_dict["name"] = results[0][0]
    return_dict["model"] = results[0][1]
    return_dict["test"] = results[0][2]
    leagues = results[0][3]
    try:
        leagues = json.loads(leagues)
    except:
        leagues = []
    return_dict["leagues"] = leagues
    return return_dict


def add_pipeline(
    name: str,
    model: str,
    test: str,
    leagues: List[str],
) -> str:
    if name in get_pipeline_names():
        return "Pipeline name already exists"

    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute(
        """INSERT INTO pipelines (name, model, test, leagues)
                   VALUES (?, ?, ?, ?)""",
        (
            name,
            model,
            test,
            json.dumps(leagues),
        ),
    )
    con.commit()
    con.close()
    return "success"


def delete_pipeline(name: str) -> str:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    if name not in get_pipeline_names():
        return "Pipeline name does not exist"
    cursor.execute("DELETE FROM pipelines WHERE name = ?", (name,))
    con.commit()
    con.close()
    return "success"


if __name__ == "__main__":
    print(
        get_pipeline_names()
    )  # print(get_league_id_from_country_tournament("england", "premier-league"))
    print(get_pipeline_parameters("my pipeline"))
    # print(get_country_and_tournament_from_league_id("BL"))
    # print(get_historical_data_name_from_oddsportal_name("Manchester City"))
    # print(get_historical_data_name_from_oddsportal_name("Sheffield United"))
    # print(get_all_league_ids_to_names())
