import sqlite3
import os
from typing import List

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


def get_test_names() -> List[str]:
    con = sqlite3.connect(database_abs_path)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM tests")
    results = cursor.fetchall()
    names: List[str] = [result[0] for result in results]
    return names


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
