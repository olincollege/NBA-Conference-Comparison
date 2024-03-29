import pandas as pd
from datetime import datetime
from nba_api.stats.endpoints import leaguegamefinder
import matplotlib.pyplot as plt


def get_inter_conference_win_loss_records(season):
    """
    Calculate win-loss records between Eastern and Western conferences.

    Args:
        season (str): The NBA season to query, formatted as 'YYYY-YY'.

    Returns:
        dict: A dictionary containing win-loss records for Eastern and Western
                conferences based on inter-conference games.

    This function retrieves the inter-conference games for the specified season
    and calculates the win-loss records for each conference.
    """
    eastern_vs_western = leaguegamefinder.LeagueGameFinder(
        vs_conference_nullable="West",
        season_nullable=season,
        league_id_nullable="00",
        season_type_nullable="Regular Season",
    ).get_data_frames()[0]

    records = {
        "Eastern": {"Wins": 0, "Losses": 0},
        "Western": {"Wins": 0, "Losses": 0},
    }

    # Calculate win-loss records for the Eastern conference against the Western
    for game in eastern_vs_western.itertuples():
        if game.WL == "W":
            records["Eastern"]["Wins"] += 1
        else:
            records["Eastern"]["Losses"] += 1

    # Infer Western conference records based on Eastern results
    records["Western"]["Wins"] = records["Eastern"]["Losses"]
    records["Western"]["Losses"] = records["Eastern"]["Wins"]

    return records


def aggregate_inter_conference_win_loss_records(seasons_back, save_to_csv=False):
    """
    Aggregate inter-conference win-loss records over multiple seasons.

    Args:
        seasons_back (int): The number of past seasons to include.
        save_to_csv (bool): If True, saves the data to a CSV file.

    Returns:
        dict: A dictionary with aggregated win-loss records for each conference.

    This function aggregates the win-loss records of Eastern and Western
    conferences against each other over the specified number of past seasons.
    Optionally, the aggregated data can be saved to a CSV file.
    """
    current_year = datetime.now().year
    start_year = current_year - seasons_back

    aggregated_records = {
        "Eastern": {"Wins": 0, "Losses": 0},
        "Western": {"Wins": 0, "Losses": 0},
    }

    for year in range(start_year, current_year):
        season = f"{year}-{str(year + 1)[-2:]}"
        season_records = get_inter_conference_win_loss_records(season)

        aggregated_records["Eastern"]["Wins"] += season_records["Eastern"]["Wins"]
        aggregated_records["Eastern"]["Losses"] += season_records["Eastern"]["Losses"]
        aggregated_records["Western"]["Wins"] += season_records["Western"]["Wins"]
        aggregated_records["Western"]["Losses"] += season_records["Western"]["Losses"]

    if save_to_csv:
        df = pd.DataFrame.from_dict(aggregated_records, orient="index")
        csv_filename = (
            f"inter_conference_win_loss_records_last_{seasons_back}_seasons.csv"
        )
        df.to_csv(csv_filename)

    return aggregated_records
