import pandas as pd
from nba_api.stats.endpoints import leaguestandings
from datetime import datetime


def get_single_season_conference_win_loss_records(season):
    """
    Fetch win-loss records for the Eastern and Western Conferences for a single season.

    Args:
    season (str): The NBA season to query, formatted as 'YYYY-YY' (e.g., '2019-20').

    Returns:
    dict: A dictionary containing win-loss records for each conference for the specified season.
    """
    # Fetch the standings for the specified season
    standings = leaguestandings.LeagueStandings(
        season=season, league_id="00", season_type="Regular Season"
    )
    standings_df = standings.get_data_frames()[0]

    # Initialize the records dictionary
    records = {
        "Eastern Conference": {"Wins": 0, "Losses": 0},
        "Western Conference": {"Wins": 0, "Losses": 0},
    }

    for conference in [
        "East",
        "West",
    ]:  # Corrected the conference names to match the data
        conf_teams = standings_df[standings_df["Conference"] == conference]
        total_wins = conf_teams["WINS"].sum()
        total_losses = conf_teams["LOSSES"].sum()

        # Append the 'ern' part to match the keys in the records dictionary
        conference_name = conference + "ern Conference"
        records[conference_name]["Wins"] = total_wins
        records[conference_name]["Losses"] = total_losses

    return records


# Example usage
season = "2019-20"  # Specify the season you want to check
conference_records = get_single_season_conference_win_loss_records(season)
print(conference_records)


def aggregate_conference_win_loss_records(seasons_back):
    """
    Aggregate win-loss records for the Eastern and Western Conferences over the specified number of past seasons.

    Args:
    seasons_back (int): The number of past seasons to aggregate.

    Returns:
    dict: A dictionary containing aggregated win-loss records for each conference over the specified seasons.
    """
    # Determine the current NBA season year
    current_year = datetime.now().year
    current_month = datetime.now().month
    start_year = current_year - 1 if current_month < 10 else current_year

    aggregated_records = {
        "Eastern Conference": {"Wins": 0, "Losses": 0},
        "Western Conference": {"Wins": 0, "Losses": 0},
    }

    for year in range(start_year - seasons_back, start_year):
        season = f"{year}-{str(year + 1)[-2:]}"
        single_season_records = get_single_season_conference_win_loss_records(
            season
        )

        for conference in ["Eastern Conference", "Western Conference"]:
            aggregated_records[conference]["Wins"] += single_season_records[
                conference
            ]["Wins"]
            aggregated_records[conference]["Losses"] += single_season_records[
                conference
            ]["Losses"]

    return aggregated_records


# Example usage
seasons_back = 5  # Last 10 seasons
conference_records = aggregate_conference_win_loss_records(seasons_back)
print(conference_records)
