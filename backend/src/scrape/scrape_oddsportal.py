from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from typing import List, Dict


def scrape():
    country = "england"
    tournament = "premier-league"

    def fi(a: str):
        try:
            driver.find_element("xpath", a).text
        except:
            return False

    def ffi(a: str):
        if fi(a) != False:
            return driver.find_element("xpath", a).text

    def fffi(a: str):
        return ffi(a)

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
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(top_link)
    reject_ads()

    # sleep for five
    # time.sleep(5)

    all_games_div_path = "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]"
    # print the text "test" and driver.find_element("xpath", test)
    try:
        all_games_div = driver.find_element("xpath", all_games_div_path)
    except:
        print("all_games_div_path incorrect")
        driver.close()
        return

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

    if len(game_links) == 0:
        print("No games found ", top_link)
        driver.close()
        return

    # Collect the over/under data for each game
    # for link in game_links:
    print(get_odds(driver, game_links[0]))


## FIXME: Only works for over/under +2.5
def get_odds(
    driver: webdriver.Chrome, link: str
) -> Dict[str, Dict[str, List[float]]] | None:
    # Return dict: Dict[odds_type: Dict[bookmaker: List[odds]]
    # List odds in order, 0 first, 1 second...

    # Navigate to the over/under page
    driver.get(link + "/#over-under;2")
    time.sleep(0.5)
    print(link + "/#over-under;2")
    ou_odds_div_path = "/html/body/div[1]/div/div[1]/div/main/div[2]/div[4]"
    try:
        ou_odds_div = driver.find_element("xpath", ou_odds_div_path)
    except:
        print("all_over_under_odds_path incorrect")
        driver.close()
        return

    # Scrape over under 2.5 for all bookmakers
    bookmaker_to_odds: Dict[str, Dict[str, List[float]]] = {}
    ou_odds_div_children = ou_odds_div.find_elements("xpath", ".//div")  # type: ignore
    for child in ou_odds_div_children:
        text_rel_path = ".//div/div[2]/p[1]"
        try:
            ou = child.find_element("xpath", text_rel_path)  # type: ignore
        except:
            continue
        if ou.text.startswith("Over/Under"):
            odds_dict = {}
            key = ou.text
            try:
                print("Try clicking", key)
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
            print("bookmaker_divs", len(bookmaker_divs))
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


if __name__ == "__main__":
    scrape()
