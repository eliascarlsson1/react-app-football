import pandas as pd
from typing import Dict, Any, List
from ..data_handling.data_handling_utils import concatenate_df_dict


class Elo_Tilt_Handler:
    __all_df_dict: Dict[str, pd.DataFrame] = {}

    # Structure: {league: {date: {team: elo}}}
    __league_elo_dict: Dict[str, Dict[str, Dict[str, float]]] = {}

    # Structure: {league: {date: {team: tilt}}}
    __league_tilt_dict: Dict[str, Dict[str, Dict[str, float]]] = {}

    def __init__(self, all_df_dict: Dict[str, pd.DataFrame]):
        self.__all_df_dict = all_df_dict

    def get_elo(self, league: str, date: str, team: str) -> float:
        if league not in self.__league_elo_dict:
            self.__calculate_for_league(league, "elo")

        ## Check so date and team exists
        if date not in self.__league_elo_dict[league]:
            raise Exception("{} not in league_elo_dict".format(date))
        if team not in self.__league_elo_dict[league][date]:
            raise Exception("{} not in league_elo_dict".format(team))

        return self.__league_elo_dict[league][date][team]

    def get_elo_by_date(self, league: str, date: str) -> Dict[str, float]:
        if league not in self.__league_elo_dict:
            self.__calculate_for_league(league, "elo")

        ## Check so date and team exists
        if date not in self.__league_elo_dict[league]:
            raise Exception("{} not in league_elo_dict".format(date))

        return self.__league_elo_dict[league][date]

    def get_tilt(self, league: str, date: str, team: str) -> float:
        if league not in self.__league_tilt_dict:
            self.__calculate_for_league(league, "tilt")

        ## Check so date and team exists
        if date not in self.__league_tilt_dict[league]:
            raise Exception("{} not in league_tilt_dict".format(date))
        if team not in self.__league_tilt_dict[league][date]:
            raise Exception("{} not in league_tilt_dict".format(team))

        return self.__league_tilt_dict[league][date][team]

    def get_tilt_by_date(self, league: str, date: str) -> Dict[str, float]:
        if league not in self.__league_tilt_dict:
            self.__calculate_for_league(league, "tilt")

        ## Check so date and team exists
        if date not in self.__league_tilt_dict[league]:
            raise Exception("{} not in league_tilt_dict".format(date))

        return self.__league_tilt_dict[league][date]

    def __calculate_for_league(self, league: str, elo_or_tilt: str):
        league_df = get_league_dataframe(self.__all_df_dict, league)
        all_teams: list[str] = list(league_df["HomeTeam"].unique())  # type: ignore
        all_dates: list[str] = list(league_df["Date"].unique())  # type: ignore
        all_dates.append("last_date")

        first_date_dict = {}
        for team in all_teams:
            if elo_or_tilt == "elo":
                first_date_dict[team] = 1000
            if elo_or_tilt == "tilt":
                first_date_dict[team] = 1

        league_dict = {}
        first_date = all_dates[0]
        league_dict[first_date] = first_date_dict

        for i in range(1, len(all_dates)):
            this_date = all_dates[i]
            last_date = all_dates[i - 1]
            dict_last_date_copy = league_dict[last_date].copy()  # type: ignore
            league_dict[this_date] = calculate_from_prev_date(
                last_date, league_df, dict_last_date_copy, elo_or_tilt  # type: ignore
            )

        if elo_or_tilt == "elo":
            self.__league_elo_dict[league] = league_dict
        if elo_or_tilt == "tilt":
            self.__league_tilt_dict[league] = league_dict


def get_league_dataframe(df_dict: dict[str, pd.DataFrame], league: str) -> pd.DataFrame:
    league_files = []
    for key in df_dict.keys():
        if league in key:
            league_files.append(key)  # type: ignore

    return concatenate_df_dict(df_dict, league_files)


def calculate_new_elo(row: Any, elo_last_date: Dict[str, float]) -> Dict[str, float]:
    ht: str = row["HomeTeam"]
    at: str = row["AwayTeam"]

    ht_elo: float = elo_last_date[ht]
    at_elo: float = elo_last_date[at]

    we_ht: float = 1 / (1 + 10 ** ((at_elo - (ht_elo + 70)) / 400))
    we_at: float = 1 / (1 + 10 ** ((ht_elo - (at_elo - 70)) / 400))

    if row["FTR"] == "H":
        ht_res: float = 1
        at_res: float = 0
    elif row["FTR"] == "A":
        ht_res: float = 0
        at_res: float = 1
    else:
        ht_res: float = 0.5
        at_res: float = 0.5

    ht_elo: float = ht_elo + 40 * (ht_res - we_ht)
    at_elo: float = at_elo + 40 * (at_res - we_at)

    teams_list: Dict[str, float] = {}
    teams_list[ht] = ht_elo
    teams_list[at] = at_elo
    return teams_list


def calculate_new_tilt(
    row: Dict[str, Any], tilt_last_date: Dict[str, float]
) -> Dict[str, float]:
    ht: str = row["HomeTeam"]
    at: str = row["AwayTeam"]
    tg: float = row["FTAG"] + row["FTHG"]

    ht_tilt_old: float = tilt_last_date[ht]
    at_tilt_old: float = tilt_last_date[at]

    ht_tilt: float = 0.95 * ht_tilt_old + 0.05 * tg / at_tilt_old / 2.5
    at_tilt: float = 0.95 * at_tilt_old + 0.05 * tg / ht_tilt_old / 2.5

    teams_list: Dict[str, float] = {}
    teams_list[ht] = ht_tilt
    teams_list[at] = at_tilt
    return teams_list


def calculate_from_prev_date(
    last_date: str,
    big_df: pd.DataFrame,
    dict_last_date: Dict[str, int],
    elo_or_tilt: str,
) -> Dict[str, int]:
    update_list: List[Dict[str, int]] = []
    games_last_date: pd.DataFrame = big_df.loc[big_df["Date"] == last_date]
    for i, row in games_last_date.iterrows():  # type: ignore
        if elo_or_tilt == "elo":
            update_list.append(calculate_new_elo(row, dict_last_date))  # type: ignore
        elif elo_or_tilt == "tilt":
            update_list.append(calculate_new_tilt(row, dict_last_date))  # type: ignore

    # Loop over list
    for i in range(len(update_list)):
        for team, value in update_list[i].items():
            dict_last_date[team] = value

    return dict_last_date
