import pandas as pd
from datetime import datetime
from nba_api.stats.endpoints import leaguestandings
import matplotlib.pyplot as plt  # Make sure to import pyplot correctly


def get_wins_over_40_single_season(season):
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


def aggregate_wins_over_40(seasons_back, save_to_csv=False):
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

    if save_to_csv:
        # Convert the aggregated data to a DataFrame
        wins_over_40_df = pd.DataFrame.from_dict(
            aggregated_wins_over_40, orient="index", columns=["Wins Over 40"]
        )
        # Save the DataFrame to a CSV file
        csv_filename = (
            f"aggregated_wins_over_40_last_{seasons_back}_seasons.csv"
        )
        wins_over_40_df.to_csv(csv_filename)
        print(f"Aggregated wins over 40 data saved to {csv_filename}")

    return aggregated_wins_over_40


# Example usage
seasons_back = 20  # Example: Last 10 seasons
aggregate_wins_over_40(seasons_back, save_to_csv=True)


def plot_wins_over_40_from_csv(seasons_back):
    # Construct the CSV filename from the number of seasons back
    csv_filename = f"aggregated_wins_over_40_last_{seasons_back}_seasons.csv"

    # Read the aggregated data from the CSV file
    data = pd.read_csv(csv_filename, index_col=0)

    # Plot the data
    fig, ax = plt.subplots()
    data.plot(kind="bar", ax=ax, rot=0)

    # Customize the plot with labels and title
    ax.set_ylabel("Wins Over 40")
    ax.set_title(
        f"Aggregated Wins Over 40 by Conference for the Last {seasons_back} Seasons"
    )
    ax.legend()

    # Show the plot
    plt.show()


# Example usage
seasons_back = 10  # Specify the number of seasons back
plot_wins_over_40_from_csv(seasons_back)
