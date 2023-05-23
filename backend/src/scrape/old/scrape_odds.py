import pandas as pd
from python_scripts.old.scrape_one_league import scrape

parameters = pd.read_json("./interface_files/current_scrape_parameters.json", typ="series")

stopcount = 0
ngames = parameters["ngames"]
country = parameters["countries"]
tournament = parameters["tournaments"]
leagues = parameters["leagues"]

df_dict = {}
for i in range(len(tournament)):
    df_dict[tournament[i]] = df = scrape(tournament[i], country[i], leagues [i], ngames)

dataframes_names = [key for key in df_dict]
dataframes = [df_dict[key] for key in dataframes_names]
my_df = pd.concat(dataframes).reset_index()

my_df.to_csv("./data/scrape_data/latest_scrape.csv")
print("Scrape complete!")
## Append league to dataframe --> write one dataframe