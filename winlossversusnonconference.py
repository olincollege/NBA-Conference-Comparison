import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder


def get_inter_conference_win_loss_records(season):
    """
    Calculate the win-loss records for each conference against the other for a given season.

    Args:
    season (str): The NBA season to query, formatted as 'YYYY-YY' (e.g., '2021-22').

    Returns:
    dict: A dictionary containing the win-loss records for each conference against the other.
    """
    # Initialize the records dictionary
    records = {
        "Eastern": {"Wins": 0, "Losses": 0},
        "Western": {"Wins": 0, "Losses": 0},
    }

    # Fetch games where Eastern conference teams played against Western conference teams
    eastern_vs_western = leaguegamefinder.LeagueGameFinder(
        vs_conference_nullable="West",
        season_nullable=season,
        league_id_nullable="00",
        season_type_nullable="Regular Season",
    ).get_data_frames()[0]

    # Fetch games where Western conference teams played against Eastern conference teams
    western_vs_eastern = leaguegamefinder.LeagueGameFinder(
        vs_conference_nullable="East",
        season_nullable=season,
        league_id_nullable="00",
        season_type_nullable="Regular Season",
    ).get_data_frames()[0]

    # Aggregate wins and losses
    for game in eastern_vs_western.itertuples():
        if game.WL == "W":
            records["Eastern"]["Wins"] += 1
        else:
            records["Eastern"]["Losses"] += 1

    for game in western_vs_eastern.itertuples():
        if game.WL == "W":
            records["Western"]["Wins"] += 1
        else:
            records["Western"]["Losses"] += 1

    return records


# Example usage
season = "2021-22"  # Specify the season you want to check
inter_conference_records = get_inter_conference_win_loss_records(season)
print(inter_conference_records)


def aggregate_inter_conference_win_loss_records(seasons_back):
    """
    Aggregate the win-loss records for each conference against teams from the opposite conference over a specified number of past seasons.

    Args:
    seasons_back (int): The number of past seasons to aggregate.

    Returns:
    dict: A dictionary containing the aggregated win-loss records for each conference against the opposite conference.
    """
    current_year = pd.to_datetime("today").year
    current_month = pd.to_datetime("today").month
    start_year = current_year - 1 if current_month < 10 else current_year

    # Initialize the aggregated records dictionary
    aggregated_records = {
        "Eastern": {"Wins": 0, "Losses": 0},
        "Western": {"Wins": 0, "Losses": 0},
    }

    for year in range(start_year - seasons_back, start_year):
        season = f"{year}-{str(year + 1)[-2:]}"
        season_records = get_inter_conference_win_loss_records(season)

        for conference in ["Eastern", "Western"]:
            aggregated_records[conference]["Wins"] += season_records[
                conference
            ]["Wins"]
            aggregated_records[conference]["Losses"] += season_records[
                conference
            ]["Losses"]

    return aggregated_records


# Example usage
seasons_back = 10  # Last 5 seasons
total_inter_conference_records = aggregate_inter_conference_win_loss_records(
    seasons_back
)
print(total_inter_conference_records)
