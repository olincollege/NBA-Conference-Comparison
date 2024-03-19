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

nba_teams = teams.get_teams()
nba_players = players.get_players()


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
    return None


def fetch_team_data(id):
    """
    Fetches the pandas dataframe corresponding with the given
    team NBA_API ID number.

    Args:
        id (int): Number denoting a specific team dataframe

    Returns:
        Returns a pandas dataframe containing the corresponding
        team data. Returns none if the ID is not found.
    """
    team = franchisehistory.FranchiseHistory()  # draws all teams' data
    team = team.get_data_frames()[0]  # generates pandas data frame
    team = team.loc[(team["TEAM_ID"] == id)]  # selects specific team
    team = team.iloc[0]  # narrows the df to the first iteration of the team
    # team = team[
    #     [
    #         "TEAM_CITY",
    #         "TEAM_NAME",
    #         "GAMES",
    #         "WINS",
    #         "LOSSES",
    #         "WIN_PCT",
    #         "PO_APPEARANCES",
    #         "CONF_TITLES",
    #         "LEAGUE_TITLES",
    #         "START_YEAR",
    #     ]
    # ]  # narrows data frame to only needed data points
    return team


def sort_conferences():
    """
    Sorts teams
    """
    eastern_conference = [
        "Celtics",
        "Bucks",
        "Cavaliers",
        "Knicks",
        "Magic",
        "76ers",
        "Pacers",
        "Heat",
        "Bulls",
        "Hawks",
        "Nets",
        "Raptors",
        "Hornets",
        "Pistons",
        "Wizards",
    ]
    western_conference = [
        "Thunder",
        "Timberwolves",
        "Nuggets",
        "Clippers",
        "Pelicans",
        "Kings",
        "Mavericks",
        "Suns",
        "Lakers",
        "Warriors",
        "Rockets",
        "Jazz",
        "Grizzlies",
        "Trail Blazers",
        "Spurs",
    ]

    east_teams = [
        team for team in nba_teams if team["nickname"] in eastern_conference
    ]
    west_teams = [
        team for team in nba_teams if team["nickname"] in western_conference
    ]
    df_eastern = pd.DataFrame(east_teams)
    df_eastern = df_eastern["id"]
    df_western = pd.DataFrame(west_teams)
    df_western = df_western["id"]

    return df_eastern, df_western


def calculate_conference_averages(df_eastern, df_western):
    """
    Docstring
    """
    east_dataframes = []
    for id in df_eastern.values:
        df = fetch_team_data(id)
        east_dataframes.append(df)
    east = pd.concat(east_dataframes, ignore_index=True)
    east_mean = east.mean(numeric_only=True)
    west_dataframes = []
    for id in df_western.values:
        df = fetch_team_data(id)
        west_dataframes.append(df)
    west = pd.concat(west_dataframes, ignore_index=True)
    west_mean = west.mean(numeric_only=True)
    return east, west


if __name__ == "__main__":

    id = find_id("lebron")
    lebron_df = fetch_data(id)
    # print(lebron_df)
    # print(nba_teams)

    eastern_df, western_df = sort_conferences()
    df_eastern_averages, df_western_averages = calculate_conference_averages(
        eastern_df, western_df
    )
    print(eastern_df, western_df)
    print(type(eastern_df))
    print("Eastern Conference Teams:")
    print(df_eastern_averages)
    print("\nWestern Conference Teams:")
    print(df_western_averages)
