from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from typing import List


def scrape(): 
    country = "england"
    tournament = "premier-league"

    def fi(a: str):
        try:
            driver.find_element("xpath", a).text
        except:
            return False
        
    def ffi(a: str):
        if fi(a) != False :
            return driver.find_element("xpath", a).text
                
    def fffi(a: str):
        return(ffi(a))    
        
    def fi2(a: str):
        try:
            driver.find_element("xpath", a).click()
        except:
            return False

    def ffi2(a: str):
        if fi2(a) != False :
            fi2(a)
            return(True)
        else:
            return(None)
        
    def reject_ads():
        ffi2('//*[@id="onetrust-reject-all-handler"]')
    
    top_link = 'https://www.oddsportal.com/{}/{}/{}/'.format("football", country, tournament)
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
    all_games_div_children = all_games_div.find_elements("xpath", ".//*") # type: ignore
    game_links: List[str] = []
    for child in all_games_div_children:
        link= child.get_attribute("href") # type: ignore
        if link == None: # type: ignore
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
    get_odds(driver, game_links[0])
    

def get_odds(driver: webdriver.Chrome, link: str):
        driver.get(link+"/#over-under;2")
        time.sleep(0.5)
        print(link+"/#over-under;2")
        ou_odds_div_path = "/html/body/div[1]/div/div[1]/div/main/div[2]/div[4]"
        try:
            ou_odds_div = driver.find_element("xpath", ou_odds_div_path)
        except:
            print("all_over_under_odds_path incorrect")
            driver.close()
            return

        # Find all divs that are the first level children of the over/under div
        # Not the second level
        ou_odds_div_children = ou_odds_div.find_elements("xpath", ".//div") # type: ignore
        for child in ou_odds_div_children:
            # print xpath of child
            text_rel_path = ".//div/div[2]/p[1]"
            try:
                ou = child.find_element("xpath", text_rel_path) # type: ignore
            except:
                print("NO TEXT FOUND")
                continue
            print(ou.text)
            time.sleep(2)

if __name__ == "__main__":
    scrape()