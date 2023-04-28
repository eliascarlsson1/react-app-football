def prepare_one_game(
    HomeTeam, AwayTeam, OddsOver, OddsUnder, OddsH, OddsA, OddsD, year, league
):
    # Load season
    location = "./data/relevant_data/" + league + year + ".csv"
    raw_data = pd.read_csv(location)
    raw_data["GameIndex"] = (
        raw_data["Date"] + raw_data["HomeTeam"] + raw_data["AwayTeam"]
    )
    raw_data["TG"] = raw_data["FTHG"] + raw_data["FTAG"]

    # Create table
    tables = create_tables_for_every_date(raw_data)
    date = list(tables.keys())[-2]

    row_data = pd.DataFrame(
        {
            "HomeTeam": [HomeTeam],
            "AwayTeam": [AwayTeam],
            "AvgO25": [OddsOver],
            "AvgU25": [OddsUnder],
            "AvgA": [OddsA],
            "AvgH": [OddsH],
            "AvgD": [OddsD],
            "Date": [date],
            "GameIndex": ["Predicted_game"],
        }
    )

    row_data["Played"] = row_data.apply(played_avg, tables=tables, axis=1)
    row_data["HtPos"] = row_data.apply(position, team="HomeTeam", tables=tables, axis=1)
    row_data["AtPos"] = row_data.apply(position, team="AwayTeam", tables=tables, axis=1)
    row_data["HtSGLG"] = row_data.apply(
        glg, team="HomeTeam", s_or_c="Goals_Scored", data=raw_data, axis=1
    )
    row_data["AtSGLG"] = row_data.apply(
        glg, team="AwayTeam", s_or_c="Goals_Scored", data=raw_data, axis=1
    )
    row_data["HtCGLG"] = row_data.apply(
        glg, team="HomeTeam", s_or_c="Goals_Conceded", data=raw_data, axis=1
    )
    row_data["AtCGLG"] = row_data.apply(
        glg, team="AwayTeam", s_or_c="Goals_Conceded", data=raw_data, axis=1
    )
    row_data["HtASGPG"] = row_data.apply(
        average_scored_gpg, team="HomeTeam", tables=tables, axis=1
    )
    row_data["AtASGPG"] = row_data.apply(
        average_scored_gpg, team="AwayTeam", tables=tables, axis=1
    )
    row_data["HtACGPG"] = row_data.apply(
        average_conceded_gpg, team="HomeTeam", tables=tables, axis=1
    )
    row_data["AtACGPG"] = row_data.apply(
        average_conceded_gpg, team="AwayTeam", tables=tables, axis=1
    )
    row_data["HtASGP5G"] = row_data.apply(
        average_scored_gp5g, team="HomeTeam", tables=tables, data=raw_data, axis=1
    )
    row_data["AtASGP5G"] = row_data.apply(
        average_scored_gp5g, team="AwayTeam", tables=tables, data=raw_data, axis=1
    )
    row_data["HtACGP5G"] = row_data.apply(
        average_conceded_gp5g, team="HomeTeam", tables=tables, data=raw_data, axis=1
    )
    row_data["AtACGP5G"] = row_data.apply(
        average_conceded_gp5g, team="AwayTeam", tables=tables, data=raw_data, axis=1
    )
    row_data["HtASGP3G"] = row_data.apply(
        average_gp3g,
        team="HomeTeam",
        s_or_c="Goals_Scored",
        tables=tables,
        data=raw_data,
        axis=1,
    )
    row_data["AtASGP3G"] = row_data.apply(
        average_gp3g,
        team="AwayTeam",
        s_or_c="Goals_Scored",
        tables=tables,
        data=raw_data,
        axis=1,
    )
    row_data["HtACGP3G"] = row_data.apply(
        average_gp3g,
        team="HomeTeam",
        s_or_c="Goals_Conceded",
        tables=tables,
        data=raw_data,
        axis=1,
    )
    row_data["AtACGP3G"] = row_data.apply(
        average_gp3g,
        team="AwayTeam",
        s_or_c="Goals_Conceded",
        tables=tables,
        data=raw_data,
        axis=1,
    )
    row_data["HtpercentGO"] = row_data.apply(
        percent_games_over, team="HomeTeam", data=raw_data, axis=1
    )
    row_data["AtpercentGO"] = row_data.apply(
        percent_games_over, team="AwayTeam", data=raw_data, axis=1
    )
    files = []
    for filename in os.listdir("./data/all_data/"):
        if filename[0:2] == league:
            if int(year) >= int(filename[2:6]):
                files.append(filename)
    row_data["AGTM"] = row_data.apply(
        average_goals_this_matchup, files=files, year=year, axis=1
    )
    row_data["TG"] = "unknown"
    row_data["FTR"] = "unknown"

    prepared_game = row_data[all_x_par]

    return prepared_game
