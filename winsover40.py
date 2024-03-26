import pandas as pd
from datetime import datetime
from nba_api.stats.endpoints import leaguestandings


def get_wins_over_40_single_season(season):
    """
    Calculate the total number of wins over 40 for each team in each conference for a single season.

    Args:
    season (str): The NBA season to query, formatted as 'YYYY-YY' (e.g., '2019-20').

    Returns:
    dict: A dictionary containing the total wins over 40 for each conference.
    """
    standings = leaguestandings.LeagueStandings(
        season=season, league_id="00", season_type="Regular Season"
    )
    standings_df = standings.get_data_frames()[0]

    wins_over_40 = {"Eastern Conference": 0, "Western Conference": 0}

    for conference in ["East", "West"]:
        conf_teams = standings_df[standings_df["Conference"] == conference]
        for index, team in conf_teams.iterrows():
            if team["WINS"] > 40:
                wins_over_40[conference + "ern Conference"] += team["WINS"] - 40

    return wins_over_40


def aggregate_wins_over_40(seasons_back):
    """
    Aggregate the total wins over 40 for each team in each conference over the specified number of past seasons.

    Args:
    seasons_back (int): The number of past seasons to aggregate.

    Returns:
    dict: A dictionary containing the aggregated total wins over 40 for each conference.
    """
    current_year = datetime.now().year
    current_month = datetime.now().month
    start_year = current_year - 1 if current_month < 10 else current_year

    aggregated_wins_over_40 = {"Eastern Conference": 0, "Western Conference": 0}

    for year in range(start_year - seasons_back, start_year):
        season = f"{year}-{str(year + 1)[-2:]}"
        season_wins_over_40 = get_wins_over_40_single_season(season)

        for conference in ["Eastern Conference", "Western Conference"]:
            aggregated_wins_over_40[conference] += season_wins_over_40[
                conference
            ]

    return aggregated_wins_over_40


# Example usage
seasons_back = 20  # Last 10 seasons
total_wins_over_40 = aggregate_wins_over_40(seasons_back)
print(total_wins_over_40)
