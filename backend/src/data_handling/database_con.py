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