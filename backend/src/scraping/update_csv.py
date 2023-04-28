import pandas as pd
import requests
from python_scripts.functions.prepare_ML_data import write_return_csv


def update_leagues(leagues, year):
    if "PL" in leagues:
        URL = "https://www.football-data.co.uk/mmz4281/" + year + "/E0.csv"
        response = requests.get(URL)
        with open("./data/relevant_data/PL2223.csv", "wb") as f:
            f.write(response.content)
        with open("./data/all_data/PL2223.csv", "wb") as f:
            f.write(response.content)

        print("Premier League updated")

    if "L1" in leagues:
        URL = "https://www.football-data.co.uk/mmz4281/" + year + "/F1.csv"
        response = requests.get(URL)
        with open("./data/relevant_data/L12223.csv", "wb") as f:
            f.write(response.content)
        with open("./data/all_data/L12223.csv", "wb") as f:
            f.write(response.content)
        print("Ligue 1 updated")

    if "BL" in leagues:
        URL = "https://www.football-data.co.uk/mmz4281/" + year + "/D1.csv"
        response = requests.get(URL)
        with open("./data/relevant_data/BL2223.csv", "wb") as f:
            f.write(response.content)
        with open("./data/all_data/BL2223.csv", "wb") as f:
            f.write(response.content)
        print("Bundesliga updated")

    if "SA" in leagues:
        URL = "https://www.football-data.co.uk/mmz4281/" + year + "/I1.csv"
        response = requests.get(URL)
        with open("./data/relevant_data/SA2223.csv", "wb") as f:
            f.write(response.content)
        with open("./data/all_data/SA2223.csv", "wb") as f:
            f.write(response.content)
        print("Serie A updated")

    if "LL" in leagues:
        URL = "https://www.football-data.co.uk/mmz4281/" + year + "/SP1.csv"
        response = requests.get(URL)
        with open("./data/relevant_data/LL2223.csv", "wb") as f:
            f.write(response.content)
        with open("./data/all_data/LL2223.csv", "wb") as f:
            f.write(response.content)
        print("La Liga updated")

    if "CS" in leagues:
        URL = "https://www.football-data.co.uk/mmz4281/" + year + "/E1.csv"
        response = requests.get(URL)
        with open("./data/relevant_data/CS2223.csv", "wb") as f:
            f.write(response.content)
        with open("./data/all_data/CS2223.csv", "wb") as f:
            f.write(response.content)
        print("Championship updated")

    if "E2" in leagues:
        URL = "https://www.football-data.co.uk/mmz4281/" + year + "/E2.csv"
        response = requests.get(URL)
        with open("./data/relevant_data/E22223.csv", "wb") as f:
            f.write(response.content)
        with open("./data/all_data/E22223.csv", "wb") as f:
            f.write(response.content)
        print("League-one updated")

    if "S2" in leagues:
        URL = "https://www.football-data.co.uk/mmz4281/" + year + "/SP2.csv"
        response = requests.get(URL)
        with open("./data/relevant_data/S22223.csv", "wb") as f:
            f.write(response.content)
        with open("./data/all_data/S22223.csv", "wb") as f:
            f.write(response.content)
        print("Laliga2 updated")

    if "SB" in leagues:
        URL = "https://www.football-data.co.uk/mmz4281/" + year + "/I2.csv"
        response = requests.get(URL)
        with open("./data/relevant_data/SB2223.csv", "wb") as f:
            f.write(response.content)
        with open("./data/all_data/SB2223.csv", "wb") as f:
            f.write(response.content)
        print("Serie B updated")

    if "D2" in leagues:
        URL = "https://www.football-data.co.uk/mmz4281/" + year + "/D2.csv"
        response = requests.get(URL)
        with open("./data/relevant_data/D22223.csv", "wb") as f:
            f.write(response.content)
        with open("./data/all_data/D22223.csv", "wb") as f:
            f.write(response.content)
        print("Bundesliga2 updated")

    if "NE" in leagues:
        URL = "https://www.football-data.co.uk/mmz4281/" + year + "/N1.csv"
        response = requests.get(URL)
        with open("./data/relevant_data/NE2223.csv", "wb") as f:
            f.write(response.content)
        with open("./data/all_data/NE2223.csv", "wb") as f:
            f.write(response.content)
        print("Eredivise updated")

    if "BE" in leagues:
        URL = "https://www.football-data.co.uk/mmz4281/" + year + "/B1.csv"
        response = requests.get(URL)
        with open("./data/relevant_data/BE2223.csv", "wb") as f:
            f.write(response.content)
        with open("./data/all_data/BE2223.csv", "wb") as f:
            f.write(response.content)
        print("Jupiler League updated")

    if "PO" in leagues:
        URL = "https://www.football-data.co.uk/mmz4281/" + year + "/P1.csv"
        response = requests.get(URL)
        with open("./data/relevant_data/PO2223.csv", "wb") as f:
            f.write(response.content)
        with open("./data/all_data/PO2223.csv", "wb") as f:
            f.write(response.content)
        print("Liga-Portugal updated")


if __name__ == "__main__":
    arguments = pd.read_json("./interface_files/update_leagues.json", typ="series")

    year = str(arguments["year"])

    update_leagues(
        ["PL", "L1", "BL", "SA", "LL", "CS", "E2", "S2", "SB", "D2", "NE", "BE", "PO"],
        year,
    )

    df_dict = write_return_csv(csv_boo_old=True, csv_boo_new=False)
