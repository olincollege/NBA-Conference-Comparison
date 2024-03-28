import matplotlib.pyplot as plt
from datetime import datetime
from nba_api.stats.endpoints import leaguestandings
import pandas as pd


def get_single_season_conference_win_loss_records(season):
    """
    Retrieves win-loss records for NBA conferences for a single season.

    Args:
        season (str): The NBA season to query, formatted as 'YYYY-YY'.

    Returns:
        dict: Win-loss records for the Eastern and Western Conferences.

    This function queries the NBA LeagueStandings endpoint to obtain and
    calculate the total wins and losses for each conference.
    """
    standings = leaguestandings.LeagueStandings(
        season=season, league_id="00", season_type="Regular Season"
    )
    standings_df = standings.get_data_frames()[0]

    records = {
        "Eastern Conference": {"Wins": 0, "Losses": 0},
        "Western Conference": {"Wins": 0, "Losses": 0},
    }

    for conference in ["East", "West"]:
        conf_teams = standings_df[standings_df["Conference"] == conference]
        total_wins = conf_teams["WINS"].sum()
        total_losses = conf_teams["LOSSES"].sum()

        conference_name = conference + "ern Conference"
        records[conference_name]["Wins"] = total_wins
        records[conference_name]["Losses"] = total_losses

    return records


def aggregate_conference_win_loss_records(seasons_back, save_to_csv=False):
    """
    Aggregates win-loss records for NBA conferences over multiple seasons.

    Args:
        seasons_back (int): Number of past seasons to include.
        save_to_csv (bool): If True, saves the data to a CSV file.

    Returns:
        dict: Aggregated win-loss records for Eastern and Western Conferences.

    This function accumulates win-loss records for the specified number of past
    seasons and optionally saves the aggregated data to a CSV file.
    """
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

    if save_to_csv:
        # Convert the aggregated records into a DataFrame for saving to CSV
        records_df = pd.DataFrame.from_dict(aggregated_records, orient="index")
        csv_filename = (
            f"conference_win_loss_records_last_{seasons_back}_seasons.csv"
        )
        records_df.to_csv(csv_filename)
        print(f"Aggregated win-loss records saved to {csv_filename}")

    return aggregated_records
