import pandas as pd
from datetime import datetime
from nba_api.stats.endpoints import leaguegamefinder
import matplotlib.pyplot as plt


def get_inter_conference_win_loss_records(season):
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


def aggregate_inter_conference_win_loss_records(
    seasons_back, save_to_csv=False
):
    current_year = datetime.now().year
    start_year = current_year - seasons_back

    aggregated_records = {
        "Eastern": {"Wins": 0, "Losses": 0},
        "Western": {"Wins": 0, "Losses": 0},
    }

    for year in range(start_year, current_year):
        season = f"{year}-{str(year + 1)[-2:]}"
        season_records = get_inter_conference_win_loss_records(season)

        aggregated_records["Eastern"]["Wins"] += season_records["Eastern"][
            "Wins"
        ]
        aggregated_records["Eastern"]["Losses"] += season_records["Eastern"][
            "Losses"
        ]
        aggregated_records["Western"]["Wins"] += season_records["Western"][
            "Wins"
        ]
        aggregated_records["Western"]["Losses"] += season_records["Western"][
            "Losses"
        ]

    if save_to_csv:
        df = pd.DataFrame.from_dict(aggregated_records, orient="index")
        csv_filename = (
            f"inter_conference_win_loss_records_last_{seasons_back}_seasons.csv"
        )
        df.to_csv(csv_filename)

    return aggregated_records


def plot_inter_conference_win_loss_records_from_csv(seasons_back):
    csv_filename = (
        f"inter_conference_win_loss_records_last_{seasons_back}_seasons.csv"
    )
    data = pd.read_csv(csv_filename, index_col=0)

    fig, ax = plt.subplots()
    data.plot(kind="bar", ax=ax, stacked=True)

    ax.set_ylabel("Number of Games")
    ax.set_title(
        f"NBA Inter-Conference Win-Loss Records Over the Last {seasons_back} Seasons"
    )
    ax.legend()

    plt.show()


# Example usage
seasons_back = 20
aggregate_inter_conference_win_loss_records(seasons_back, save_to_csv=True)
# plot_inter_conference_win_loss_records_from_csv(seasons_back)
