from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import franchisehistory
from nba_api.stats.static import teams
from nba_api.stats.static import players

from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard

import pandas as pd
import matplotlib_inline as plt
import datetime


def find_id(name):
    """
    Returns nba team or player ID based on given name.

    Args:
        name (str): Team or player name

    Returns:
        A string denoting the indicated team or player NBA_API ID
        number. Returns none if the team or player is not found.
    """
    name = name.lower()
    for team in nba_teams:
        for key, value in team.items():
            if str(value).lower() == name:
                return "team", team["id"]
    for player in nba_players:
        for key, value in player.items():
            if str(value).lower() == name:
                return "player", player["id"]
    return None


def fetch_data(id):
    """
    Fetches the pandas dataframe corresponding with the given
    team or player NBA_API ID number.

    Args:
        id (int): Number denoting a specific team or player data

    Returns:
        Returns a pandas dataframe containing the corresponding
        team or player data. Returns none if the ID is not found.
    """
    if id[0] == "player":
        player = playercareerstats.PlayerCareerStats(
            player_id=f"{id[-1]}"
        )  # draws specific player's data
        player = player.get_data_frames()[0]  # generates pandas data frame
        player["AVG_PTS"] = player["PTS"] / player["GP"]
        player["AVG_PTS"] = player["AVG_PTS"].round(0)
        player["AVG_REB"] = player["REB"] / player["GP"]
        player["AVG_REB"] = player["AVG_REB"].round(0)
        player["AVG_AST"] = player["AST"] / player["GP"]
        player["AVG_AST"] = player["AVG_AST"].round(0)
        player["AVG_MIN"] = player["MIN"] / player["GP"]
        player["AVG_MIN"] = player["AVG_MIN"].round(0)
        player = player[
            [
                "SEASON_ID",
                "TEAM_ABBREVIATION",
                "AVG_PTS",
                "AVG_REB",
                "AVG_AST",
                "AVG_MIN",
                "PTS",
                "REB",
                "AST",
                "MIN",
            ]
        ]  # narrows data frame to only needed data points
        return player
    elif id[0] == "team":
        team = franchisehistory.FranchiseHistory()  # draws all teams' data
        team = team.get_data_frames()[0]  # generates pandas data frame
        team = team.loc[(team["TEAM_ID"] == id[-1])]  # selects specific team
        team = team.iloc[0]  # narrows the df to the first iteration of the team
        team = team[
            [
                "TEAM_CITY",
                "TEAM_NAME",
                "GAMES",
                "WINS",
                "LOSSES",
                "WIN_PCT",
                "PO_APPEARANCES",
                "CONF_TITLES",
                "LEAGUE_TITLES",
                "START_YEAR",
            ]
        ]  # narrows data frame to only needed data points
        return team
    else:
        return None


if __name__ == "__main__":

    nba_teams = teams.get_teams()
    nba_players = players.get_players()

    id = find_id("lebron")
    print(id)
