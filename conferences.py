import pandas as pd
from nba_api.stats.endpoints import leaguestandings


def get_teams_by_conference(season="2022-23"):
    """
    Fetches the current season's teams and separates them into Eastern and Western conferences.

    Args:
    season (str): The NBA season to query, formatted as 'YYYY-YY'.

    Returns:
    dict: A dictionary with keys 'Eastern' and 'Western', each containing a list of team IDs.
    """
    # Fetch the standings for the specified season
    standings = leaguestandings.LeagueStandings(season=season)
    standings_df = standings.get_data_frames()[0]

    # Separate teams by conference
    eastern_teams = standings_df[standings_df["Conference"] == "East"][
        "TeamID"
    ].tolist()
    western_teams = standings_df[standings_df["Conference"] == "West"][
        "TeamID"
    ].tolist()

    return {"Eastern": eastern_teams, "Western": western_teams}
