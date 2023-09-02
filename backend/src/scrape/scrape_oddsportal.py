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
    time.sleep(1)
    reject_ads()

    login(driver)

    game_links = get_game_links(driver, top_link)
    if len(game_links) == 0:
        print("No games found ", top_link)
        driver.close()
        return

    # Collect the over/under + 1x2 data for each game, and team names
    over_under_string = "/#over-under;2"
    one_x_two_string = "/#1X2;2"

    for link in game_links:
        # Get over/under odds
        driver.get(link + over_under_string)
        time.sleep(2)
        info = get_teams_and_date(driver)
        over_under_odds = get_over_under_odds(driver)
        if len(info) == 0:
            print("No info found")
            continue
        if over_under_odds == None:
            print("No over/under odds found")
            continue
        encoded_odds_over_under = json.dumps(over_under_odds)

        # 1x2 odds
        driver.get(link + one_x_two_string)
        time.sleep(2)
        driver.get(link + one_x_two_string)
        time.sleep(3)
        one_x_two_odds = get_one_x_two_odds(driver, link + one_x_two_string)
        if one_x_two_odds == None:
            print("No one_x_two_odds found", info)
            continue
        encoded_one_x_two_odds = json.dumps(one_x_two_odds)

        # Make a dataframe row and append to data_rows
        scrape_time = pd.Timestamp.utcnow().isoformat()
        scrape_game_index = info[0] + info[1] + info[2]
        data_row = [country, tournament, scrape_time] + info + [encoded_odds_over_under] + [encoded_one_x_two_odds] + [scrape_game_index] + [link]  # type: ignore

        df = pd.DataFrame(
            [data_row],
            columns=[
                "country",
                "tournament",
                "scrape_time",
                "home_team",
                "away_team",
                "date",
                "time",
                "odds_over_under",
                "odds_one_x_two",
                "scrape_game_index",
                "oddsportal_link",
            ],
        )
        write_to_csv(df)


def login(driver: webdriver.Chrome):
    # Log in
    side_menu_button = "/html/body/div[1]/div/header/div[2]/div/div[2]/div[1]"
    try:
        driver.find_element("xpath", side_menu_button).click()
    except:
        print("side_menu_button incorrect")
        driver.close()
        return
    time.sleep(3)

    log_in_button = (
        "/html/body/div[1]/div/header/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]"
    )
    try:
        driver.find_element("xpath", log_in_button).click()
    except:
        print("login_button_path incorrect")
        time.sleep(60)
        driver.close()
        return
    time.sleep(3)

    oddsportal_username_path = (
        "/html/body/div[4]/div/div/div[2]/div/div/form/div[1]/div[2]/div/input"
    )
    oddsportal_username_path_alternative = (
        "/html/body/div[3]/div/div/div[2]/div/div/form/div[1]/div[2]/div/input"
    )
    try:
        driver.find_element("xpath", oddsportal_username_path).send_keys("anloan")  # type: ignore
    except:
        try:
            driver.find_element("xpath", oddsportal_username_path_alternative).send_keys("anloan")  # type: ignore
        except:
            print("oddsportal_username_path incorrect")
            driver.close()
            return
    time.sleep(3)

    oddsportal_password_path = (
        "/html/body/div[4]/div/div/div[2]/div/div/form/div[2]/div[2]/div/input"
    )
    oddsportal_password_path_alternative = (
        "/html/body/div[3]/div/div/div[2]/div/div/form/div[2]/div[2]/div/input"
    )
    try:
        driver.find_element("xpath", oddsportal_password_path).send_keys("pjy0pkd3rdp!YAF_vcj")  # type: ignore
    except:
        try:
            driver.find_element("xpath", oddsportal_password_path_alternative).send_keys("pjy0pkd3rdp!YAF_vcj")  # type: ignore
        except:
            print("oddsportal_password_path incorrect")
            driver.close()
            return
    time.sleep(3)

    log_in_button = "/html/body/div[4]/div/div/div[2]/div/div/form/div[4]/span/input"
    log_in_button_alternative = (
        "/html/body/div[3]/div/div/div[2]/div/div/form/div[4]/span/input"
    )
    try:
        driver.find_element("xpath", log_in_button).click()
    except:
        try:
            driver.find_element("xpath", log_in_button_alternative).click()
        except:
            print("login_button_path incorrect")
            driver.close()
            return


def write_to_csv(df: pd.DataFrame):
    old_df = pd.read_csv("./data/scrape.csv")  # type: ignore
    df = pd.concat([old_df, df], ignore_index=True)  # type: ignore
    df.to_csv("./data/scrape.csv", index=False)


def get_teams_and_date(driver: webdriver.Chrome) -> List[str]:
    # Return [home_team, away_team, date, time]
    home_team_path = "/html/body/div[1]/div/div[1]/div/main/div[2]/div[3]/div[1]/div[1]/div/div[1]/span"
    try:
        home_team = driver.find_element("xpath", home_team_path)
    except:
        print("home_team_path incorrect")
        driver.close()
        return []

    away_team_path = (
        "/html/body/div[1]/div/div[1]/div/main/div[2]/div[3]/div[1]/div[3]/div[1]/span"
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


def get_over_under_odds(
    driver: webdriver.Chrome,
) -> Dict[str, Dict[str, List[str]]] | None:
    # Return dict: Dict[odds_type: Dict[bookmaker: List[odds]]
    # List odds in order, 0 first, 1 second...

    # Navigate to the over/under page
    ou_odds_div_path = "/html/body/div[1]/div/div[1]/div/main/div[2]/div[4]"
    try:
        ou_odds_div = driver.find_element("xpath", ou_odds_div_path)
    except:
        print("all_over_under_odds_path incorrect")
        return

    # Fill the dict for each bet type
    bookmaker_to_odds: Dict[str, Dict[str, List[str]]] = {}
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
            time.sleep(0.5)

            try:
                child.click()
            except:
                continue
            bookmaker_divs_rel_path = ".//div[2]/*"
            try:
                bookmaker_divs = child.find_elements("xpath", bookmaker_divs_rel_path)  # type: ignore
            except:
                print("bookmaker_divs_rel_path incorrect")
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

    if len(bookmaker_to_odds) == 0:
        return None
    return bookmaker_to_odds


def get_one_x_two_odds(
    driver: webdriver.Chrome, link: str
) -> Dict[str, List[str]] | None:
    # Return dict: Dict[bookmaker: List[odds]]

    one_x_two_path = "/html/body/div[1]/div/div[1]/div/main/div[2]/div[4]/div[1]/div"

    try:
        one_x_two_div = driver.find_element("xpath", one_x_two_path)
    except:
        driver.get(link)
        time.sleep(1)
        driver.get(link)
        time.sleep(5)
        try:
            one_x_two_div = driver.find_element("xpath", one_x_two_path)
        except:
            print("one_x_two_path incorrect")
            return

    bookmaker_to_odds: Dict[str, List[str]] = {}
    one_x_two_div_children = one_x_two_div.find_elements("xpath", ".//div")  # type: ignore
    betmaker_relative_path = ".//div[1]/a[2]/p"
    odds_1_path = ".//div[2]/div/div/"
    odds_x_path = ".//div[3]/div/div/"
    odds_2_path = ".//div[4]/div/div/"
    for child in one_x_two_div_children:
        try:
            betmaker = child.find_element("xpath", betmaker_relative_path)  # type: ignore
            if betmaker.text == "":
                continue
        except:
            continue
        try:
            odds_1 = child.find_element("xpath", odds_1_path + "p")  # type: ignore
            if odds_1.text == "":
                odds_1 = child.find_element("xpath", odds_1_path + "a")  # type: ignore
        except:
            print("odds_1 not found")
            continue

        try:
            odds_x = child.find_element("xpath", odds_x_path + "p")  # type: ignore
            if odds_x.text == "":
                odds_x = child.find_element("xpath", odds_x_path + "a")  # type: ignore
        except:
            print("odds_x not found")
            continue

        try:
            odds_2 = child.find_element("xpath", odds_2_path + "p")  # type: ignore
            if odds_2.text == "":
                odds_2 = child.find_element("xpath", odds_2_path + "a")  # type: ignore
        except:
            print("odds_2 not found")
            continue

        bookmaker_to_odds[betmaker.text] = [odds_1.text, odds_x.text, odds_2.text]

    if len(bookmaker_to_odds) == 0:
        return None

    return bookmaker_to_odds


# if __name__ == "__main__":
#     country = "england"
#     tournament = "premier-league"

#     scrape_league(country, tournament)
