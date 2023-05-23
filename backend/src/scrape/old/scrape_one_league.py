from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import time
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains


def scrape(tournament, country, league, ngames):
    def fi(a):
        try:
            driver.find_element("xpath", a).text
        except:
            return False

    def ffi(a):
        if fi(a) != False:
            return driver.find_element("xpath", a).text

    def fffi(a):
        return ffi(a)

    def fi2(a):
        try:
            driver.find_element("xpath", a).click()
        except:
            return False

    def ffi2(a):
        if fi2(a) != False:
            fi2(a)
            return True
        else:
            return None

    def reject_ads():
        ffi2('//*[@id="onetrust-reject-all-handler"]')

    link = "https://www.oddsportal.com/{}/{}/{}/".format("soccer", country, tournament)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(link)
    reject_ads()
    odds_dict = {}
    i = 1
    k = 0

    while k < ngames:
        # Reload page
        driver.get(link)

        j = 1
        AvgH = ffi(
            '//*[@id="app"]/div/div[1]/div/main/div[2]/div[7]/div[{i}]/div[{j}]/div[1]/div[1]/div/span/p'.format(
                i=i, j=j
            )
        )
        AvgD = ffi(
            '//*[@id="app"]/div/div[1]/div/main/div[2]/div[7]/div[{i}]/div[{j}]/div[1]/div[2]/div/span/p'.format(
                i=i, j=j
            )
        )
        AvgA = ffi(
            '//*[@id="app"]/div/div[1]/div/main/div[2]/div[7]/div[{i}]/div[{j}]/div[1]/div[3]/div/span/p'.format(
                i=i, j=j
            )
        )
        while AvgH == None:
            j += 1
            AvgH = ffi(
                '//*[@id="app"]/div/div[1]/div/main/div[2]/div[7]/div[{i}]/div[{j}]/div[1]/div[1]/div/span/p'.format(
                    i=i, j=j
                )
            )
            AvgD = ffi(
                '//*[@id="app"]/div/div[1]/div/main/div[2]/div[7]/div[{i}]/div[{j}]/div[1]/div[2]/div/span/p'.format(
                    i=i, j=j
                )
            )
            AvgA = ffi(
                '//*[@id="app"]/div/div[1]/div/main/div[2]/div[7]/div[{i}]/div[{j}]/div[1]/div[3]/div/span/p'.format(
                    i=i, j=j
                )
            )

        if i > 5:
            driver.execute_script("window.scrollTo(0, 400);")
            time.sleep(0.5)
        target = '//*[@id="app"]/div/div[1]/div/main/div[2]/div[7]/div[{i}]/div[{j}]/div[1]/a'.format(
            i=i, j=j
        )
        a = ffi2(target)
        i += 1

        # If a = if we click a game
        if a:
            game = ffi('//*[@id="app"]/div/div[1]/div/main/div[2]/div[4]/ul/li[11]/p')
            odds_dict[game] = {}
            odds_dict[game]["Game"] = game
            odds_dict[game]["AvgH"] = AvgH
            odds_dict[game]["AvgA"] = AvgA
            odds_dict[game]["AvgD"] = AvgD

            url_new = driver.current_url.replace("#1X2;2", "") + "#over-under;2"
            driver.get(url_new)
            driver.get(url_new)
            time.sleep(0.3)

            odds = "nothing_yet"
            q = 0
            while odds != "Over/Under +2.5":
                q = q + 1
                odds = ffi(
                    '//*[@id="app"]/div/div[1]/div/main/div[2]/div[6]/div[{}]/div/div[2]/p[1]'.format(
                        q
                    )
                )

            odds_dict[game]["Date"] = ffi(
                '//*[@id="app"]/div/div[1]/div/main/div[2]/div[5]/div[2]/div[1]/div[2]'
            )
            odds_dict[game]["AvgO25"] = ffi(
                '//*[@id="app"]/div/div[1]/div/main/div[2]/div[6]/div[{}]/div/div[3]/div[1]/button/p'.format(
                    q
                )
            )
            odds_dict[game]["AvgU25"] = ffi(
                '//*[@id="app"]/div/div[1]/div/main/div[2]/div[6]/div[{}]/div/div[3]/div[2]/button/p'.format(
                    q
                )
            )
            k = k + 1

    driver.close()

    for key in odds_dict.keys():
        odds_dict[key]["HomeTeam"] = key.split(" - ")[0]
        odds_dict[key]["AwayTeam"] = key.split(" - ")[1]

    my_dataframe = pd.DataFrame(odds_dict).transpose().reset_index()
    my_dataframe["league"] = league

    return my_dataframe
