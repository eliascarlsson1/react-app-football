from selenium import webdriver
import time
import pandas as pd
import json
from typing import List, Dict


def scrape_league(country: str, tournament: str):
    def fi2(a: str):
        try:
            driver.find_element("xpath", a).click()
        except:
            return False

    def ffi2(a: str):
        if fi2(a) != False:
            fi2(a)
            return True
        else:
            return None

    def reject_ads():
        ffi2('//*[@id="onetrust-reject-all-handler"]')

    top_link = "https://www.oddsportal.com/{}/{}/{}/".format(
        "football", country, tournament
    )
    driver = webdriver.Chrome()
    driver.get(top_link)
    reject_ads()

    # sleep for five
    # time.sleep(5)

    game_links = get_game_links(driver, top_link)
    if len(game_links) == 0:
        print("No games found ", top_link)
        driver.close()
        return

    # Collect the over/under data for each game, and team names

    over_under_string = "/#over-under;2"
    one_x_two_string = "/#1X2;2"
    data_rows = []

    for link in game_links:

        # Get over/under odds
        driver.get(link + over_under_string)
        info = get_teams_and_date(driver)
        over_under_odds = get_over_under_odds(driver)
        if over_under_odds == None:
            continue
        if len(info) == 0:
            continue
        # Make a dataframe row and append to data_rows
        encoded_odds_over_under = json.dumps(over_under_odds)
        scrape_time = pd.Timestamp.utcnow().isoformat()
        data_rows.append([country, tournament, scrape_time] + info + [encoded_odds_over_under])  # type: ignore

    # Convert data_rows to a dataframe
    old_df = pd.read_csv("./data/scrape.csv")  # type: ignore
    df = pd.DataFrame(
        data_rows,
        columns=[
            "country",
            "tournament",
            "scrape_time",
            "home_team",
            "away_team",
            "date",
            "time",
            "odds_over_under",
        ],
    )
    df = pd.concat([old_df, df], ignore_index=True)  # type: ignore
    df.to_csv("./data/scrape.csv", index=False)

def get_teams_and_date(driver: webdriver.Chrome) -> List[str]:
    # Return [home_team, away_team, date, time]
    home_team_path = (
        "/html/body/div[1]/div/div[1]/div/main/div[2]/div[3]/div[1]/div[1]/div/div[1]/p"
    )
    try:
        home_team = driver.find_element("xpath", home_team_path)
    except:
        print("home_team_path incorrect")
        driver.close()
        return []

    away_team_path = (
        "/html/body/div[1]/div/div[1]/div/main/div[2]/div[3]/div[1]/div[3]/div[1]/p"
    )
    try:
        away_team = driver.find_element("xpath", away_team_path)
    except:
        print("away_team_path incorrect")
        driver.close()
        return []

    date_path = "/html/body/div[1]/div/div[1]/div/main/div[2]/div[3]/div[2]/div[1]/p[2]"
    try:
        date = driver.find_element("xpath", date_path)
    except:
        print("date_path incorrect")
        driver.close()
        return []

    time_path = "/html/body/div[1]/div/div[1]/div/main/div[2]/div[3]/div[2]/div[1]/p[3]"
    try:
        time = driver.find_element("xpath", time_path)
    except:
        print("time_path incorrect")
        driver.close()
        return []

    return [home_team.text, away_team.text, date.text, time.text]


def get_game_links(driver: webdriver.Chrome, top_link: str) -> List[str]:
    all_games_div_path = "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]"
    # print the text "test" and driver.find_element("xpath", test)
    try:
        all_games_div = driver.find_element("xpath", all_games_div_path)
    except:
        print("all_games_div_path incorrect")
        driver.close()
        return []

    # Find the div that contains all the games
    all_games_div_children = all_games_div.find_elements("xpath", ".//*")  # type: ignore
    game_links: List[str] = []
    for child in all_games_div_children:
        link = child.get_attribute("href")  # type: ignore
        if link == None:  # type: ignore
            continue
        if link == top_link:
            continue
        if link.startswith(top_link) == False:
            continue
        if link in game_links:
            continue

        game_links.append(link)

    return game_links


def get_over_under_odds(driver: webdriver.Chrome) -> Dict[str, Dict[str, List[float]]] | None:
    # Return dict: Dict[odds_type: Dict[bookmaker: List[odds]]
    # List odds in order, 0 first, 1 second...

    # Navigate to the over/under page
    time.sleep(0.5)
    ou_odds_div_path = "/html/body/div[1]/div/div[1]/div/main/div[2]/div[4]"
    try:
        ou_odds_div = driver.find_element("xpath", ou_odds_div_path)
    except:
        print("all_over_under_odds_path incorrect")
        driver.close()
        return

    # Fill the dict for each bet type
    bookmaker_to_odds: Dict[str, Dict[str, List[float]]] = {}
    ou_odds_div_children = ou_odds_div.find_elements("xpath", ".//div")  # type: ignore
    for child in ou_odds_div_children:
        text_rel_path = ".//div/div[2]/p[1]"
        try:
            ou = child.find_element("xpath", text_rel_path)  # type: ignore
        except:
            continue

        ## Scraping over under
        if ou.text.startswith("Over/Under"):
            odds_dict = {}
            key = ou.text

            # Scroll down
            driver.execute_script("arguments[0].scrollIntoView()", child)  # type: ignore
            time.sleep(0.3)

            try:
                child.click()
            except:
                continue
            bookmaker_divs_rel_path = ".//div[2]/*"
            try:
                bookmaker_divs = child.find_elements("xpath", bookmaker_divs_rel_path)  # type: ignore
            except:
                print("bookmaker_divs_rel_path incorrect")
                driver.close()
                return

            ## Scraping every bookmaker
            for bookmaker_div in bookmaker_divs:
                bookmaker_rel_path = ".//div[1]/a[2]/p"
                odds_over_rel_path = ".//div[3]/div/div/"
                odds_under_rel_path = ".//div[4]/div/div/"
                try:
                    bookmaker = bookmaker_div.find_element("xpath", bookmaker_rel_path)  # type: ignore
                    odds_high = bookmaker_div.find_element("xpath", odds_over_rel_path + "a")  # type: ignore
                    odds_low = bookmaker_div.find_element("xpath", odds_under_rel_path + "a")  # type: ignore
                except:
                    try:
                        bookmaker = bookmaker_div.find_element("xpath", bookmaker_rel_path)  # type: ignore
                        odds_high = bookmaker_div.find_element("xpath", odds_over_rel_path + "p")  # type: ignore
                        odds_low = bookmaker_div.find_element("xpath", odds_under_rel_path + "p")  # type: ignore
                    except:
                        continue
                odds_dict[bookmaker.text] = [odds_low.text, odds_high.text]
            bookmaker_to_odds[key] = odds_dict

    return bookmaker_to_odds


# if __name__ == "__main__":
#     country = "england"
#     tournament = "premier-league"

#     scrape_league(country, tournament)
