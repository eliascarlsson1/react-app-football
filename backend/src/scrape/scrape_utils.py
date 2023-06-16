import pandas as pd


def filter_scrape_for_upcoming_games(scrape: pd.DataFrame) -> pd.DataFrame:
    time_now = pd.Timestamp.now()
    print(time_now)
    scrape["datetime"] = pd.to_datetime(scrape["date"] + " " + scrape["time"])  # type: ignore

    # Filter for games that are upcoming
    scrape = scrape[scrape["datetime"] > time_now]
    scrape = scrape.drop(columns=["datetime"])
    return scrape


def filter_scrape_for_last_scraped(scrape: pd.DataFrame) -> pd.DataFrame:
    # It has column called "scrape_time" which is the time the game was scraped
    # For every game, hometeam, awayteam, date identical get the latest scrape
    # make an id column of hometeam, awayteam, date and time

    scrape["id"] = (
        scrape["home_team"] + scrape["away_team"] + scrape["date"] + scrape["time"]
    )

    # Filter scrape to only have one of each id, with the latest scrape_time
    scrape = scrape.sort_values(by=["scrape_time"], ascending=False)  # type: ignore
    scrape = scrape.drop_duplicates(subset=["id"], keep="first")
    scrape = scrape.drop(columns=["id"])
    return scrape


if __name__ == "__main__":
    df = pd.read_csv("./data/scrape.csv")  # type: ignore
    filtered_df = filter_scrape_for_upcoming_games(df)
    filtered_df = filter_scrape_for_last_scraped(filtered_df)
    print(filtered_df)
