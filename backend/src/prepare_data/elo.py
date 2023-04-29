import pandas as pd
from ..data_handling.data_handling_utils import concatenate_df_dict

class EloHandler:
    __all_df_dict: dict[str, pd.DataFrame] = {}

    # Structure: {league: {date: {team: elo}}}
    __league_elo_dict: dict[str, dict[str, dict[str, int]]] = {}

    def __init__(self, all_df_dict: dict[str, pd.DataFrame]):
        self.__all_df_dict = all_df_dict

    def get_all_dict_keys(self) -> list[str]:
        return list(self.__all_df_dict.keys())
    

    def get_elo(self, league: str, date: str, team: str) -> int:
        if (league not in self.__league_elo_dict):
            self.__calculate_elo_for_league(league)
        
        return self.__league_elo_dict[league][date][team]
    
    def __calculate_elo_for_league(self, league: str):



def get_league_dataframe(df_dict: dict[str, pd.DataFrame], league: str) -> pd.DataFrame:
    league_files = []
    for key in df_dict.keys():
        if league in key:
            league_files.append(key)
    
    return concatenate_df_dict(df_dict, league_files)
