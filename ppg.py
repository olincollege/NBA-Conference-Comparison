from nba_api.stats.endpoints import leaguedashteamstats
from datetime import datetime


def get_average_ppg_by_conference(season):
    """
    Calculate the average points per game for the Eastern and Western conferences in a given season.

    Args:
    season (str): The NBA season to query, formatted as 'YYYY-YY'.

    Returns:
    dict: A dictionary containing the average points per game for each conference.
    """
    east_stats = leaguedashteamstats.LeagueDashTeamStats(
        season=season,
        per_mode_detailed="PerGame",
        conference_nullable="East",
        season_type_all_star="Regular Season",
    )
    west_stats = leaguedashteamstats.LeagueDashTeamStats(
        season=season,
        per_mode_detailed="PerGame",
        conference_nullable="West",
        season_type_all_star="Regular Season",
    )

    east_avg_ppg = east_stats.get_data_frames()[0]["PTS"].mean()
    west_avg_ppg = west_stats.get_data_frames()[0]["PTS"].mean()

    return {"Eastern": east_avg_ppg, "Western": west_avg_ppg}


def get_average_ppg_over_seasons(seasons_back):
    """
    Calculate the average points per game for the Eastern and Western conferences over the past number of seasons.

    Args:
    seasons_back (int): The number of past seasons to include in the calculation.

    Returns:
    dict: A dictionary containing the average points per game for each conference over the specified seasons.
    """
    current_year = datetime.now().year
    current_month = datetime.now().month
    start_year = (
        current_year - seasons_back
        if current_month < 10
        else current_year - seasons_back + 1
    )

    eastern_ppg = []
    western_ppg = []

    for year in range(start_year, current_year):
        season = f"{year}-{str(year + 1)[-2:]}"
        avg_ppg = get_average_ppg_by_conference(season)
        eastern_ppg.append(avg_ppg["Eastern"])
        western_ppg.append(avg_ppg["Western"])

    return {
        "Eastern": sum(eastern_ppg) / len(eastern_ppg),
        "Western": sum(western_ppg) / len(western_ppg),
    }


# Example usage
season = "2021-22"
print(f"Average PPG in {season}:")
print(get_average_ppg_by_conference(season))

seasons_back = 5
print(f"\nAverage PPG over the last {seasons_back} seasons:")
print(get_average_ppg_over_seasons(seasons_back))
