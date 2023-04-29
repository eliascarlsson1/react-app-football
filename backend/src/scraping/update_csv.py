import os
import requests
from ..data_handling.database_con import get_current_year, get_all_league_ids

script_dir = os.path.dirname(__file__)
path_to_relevant = "../../data/historical_data/relevant_data"
path_to_all = "../../data/historical_data/all_data"
relevant_abs_path = os.path.join(script_dir, path_to_relevant)
all_abs_path = os.path.join(script_dir, path_to_all)

def update_leagues():
    leagues = get_all_league_ids()
    year = get_current_year()

    if "PL" in leagues:
        url = "https://www.football-data.co.uk/mmz4281/" + year + "/E0.csv"
        response = requests.get(url)
        with open(relevant_abs_path + "/PL2223.csv", "wb") as f:
            f.write(response.content)
        with open(all_abs_path + "/PL2223.csv", "wb") as f:
            f.write(response.content)

        print("Premier League updated")

    if "L1" in leagues:
        url = "https://www.football-data.co.uk/mmz4281/" + year + "/F1.csv"
        response = requests.get(url)
        with open(relevant_abs_path + "/L12223.csv", "wb") as f:
            f.write(response.content)
        with open(all_abs_path + "/L12223.csv", "wb") as f:
            f.write(response.content)
        print("Ligue 1 updated")

    if "BL" in leagues:
        url = "https://www.football-data.co.uk/mmz4281/" + year + "/D1.csv"
        response = requests.get(url)
        with open(relevant_abs_path + "/BL2223.csv", "wb") as f:
            f.write(response.content)
        with open(all_abs_path + "/BL2223.csv", "wb") as f:
            f.write(response.content)
        print("Bundesliga updated")

    if "SA" in leagues:
        url = "https://www.football-data.co.uk/mmz4281/" + year + "/I1.csv"
        response = requests.get(url)
        with open(relevant_abs_path + "/SA2223.csv", "wb") as f:
            f.write(response.content)
        with open(all_abs_path + "/SA2223.csv", "wb") as f:
            f.write(response.content)
        print("Serie A updated")

    if "LL" in leagues:
        url = "https://www.football-data.co.uk/mmz4281/" + year + "/SP1.csv"
        response = requests.get(url)
        with open(relevant_abs_path + "/LL2223.csv", "wb") as f:
            f.write(response.content)
        with open(all_abs_path + "/LL2223.csv", "wb") as f:
            f.write(response.content)
        print("La Liga updated")

    if "CS" in leagues:
        url = "https://www.football-data.co.uk/mmz4281/" + year + "/E1.csv"
        response = requests.get(url)
        with open(relevant_abs_path + "/CS2223.csv", "wb") as f:
            f.write(response.content)
        with open(all_abs_path + "/CS2223.csv", "wb") as f:
            f.write(response.content)
        print("Championship updated")

    if "E2" in leagues:
        url = "https://www.football-data.co.uk/mmz4281/" + year + "/E2.csv"
        response = requests.get(url)
        with open(relevant_abs_path + "/E22223.csv", "wb") as f:
            f.write(response.content)
        with open(all_abs_path + "/E22223.csv", "wb") as f:
            f.write(response.content)
        print("League-one updated")

    if "S2" in leagues:
        url = "https://www.football-data.co.uk/mmz4281/" + year + "/SP2.csv"
        response = requests.get(url)
        with open(relevant_abs_path + "/S22223.csv", "wb") as f:
            f.write(response.content)
        with open(all_abs_path + "/S22223.csv", "wb") as f:
            f.write(response.content)
        print("Laliga2 updated")

    if "SB" in leagues:
        url = "https://www.football-data.co.uk/mmz4281/" + year + "/I2.csv"
        response = requests.get(url)
        with open(relevant_abs_path + "/SB2223.csv", "wb") as f:
            f.write(response.content)
        with open(all_abs_path + "/SB2223.csv", "wb") as f:
            f.write(response.content)
        print("Serie B updated")

    if "D2" in leagues:
        url = "https://www.football-data.co.uk/mmz4281/" + year + "/D2.csv"
        response = requests.get(url)
        with open(relevant_abs_path + "/D22223.csv", "wb") as f:
            f.write(response.content)
        with open(all_abs_path + "/D22223.csv", "wb") as f:
            f.write(response.content)
        print("Bundesliga2 updated")

    if "NE" in leagues:
        url = "https://www.football-data.co.uk/mmz4281/" + year + "/N1.csv"
        response = requests.get(url)
        with open(relevant_abs_path + "/NE2223.csv", "wb") as f:
            f.write(response.content)
        with open(all_abs_path + "/NE2223.csv", "wb") as f:
            f.write(response.content)
        print("Eredivise updated")

    if "BE" in leagues:
        url = "https://www.football-data.co.uk/mmz4281/" + year + "/B1.csv"
        response = requests.get(url)
        with open(relevant_abs_path + "/BE2223.csv", "wb") as f:
            f.write(response.content)
        with open(all_abs_path + "/BE2223.csv", "wb") as f:
            f.write(response.content)
        print("Jupiler League updated")

    if "PO" in leagues:
        url = "https://www.football-data.co.uk/mmz4281/" + year + "/P1.csv"
        response = requests.get(url)
        with open(relevant_abs_path + "/PO2223.csv", "wb") as f:
            f.write(response.content)
        with open(all_abs_path + "/PO2223.csv", "wb") as f:
            f.write(response.content)
        print("Liga-Portugal updated")
