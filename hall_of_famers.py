import pandas as pd
from nba_api.stats.endpoints import teamdetails
from conferences import get_teams_by_conference


def fetch_team_hof(team_id):
    details = teamdetails.TeamDetails(team_id=team_id)
    hof_data = details.get_data_frames()[
        5
    ]  # Assuming TeamHof is the sixth dataset (index 5)
    return len(hof_data)


def tally_hof_by_conference(save_to_csv=False):
    team_conference_map = get_teams_by_conference()
    hof_count = {"East": 0, "West": 0}

    for conference, teams in team_conference_map.items():
        standardized_conference = "East" if "East" in conference else "West"
        for team_id in teams:
            hof_count[standardized_conference] += fetch_team_hof(team_id)

    if save_to_csv:
        df = pd.DataFrame(
            list(hof_count.items()), columns=["Conference", "Hall of Famers"]
        )
        df.to_csv("hall_of_famers_by_conference.csv", index=False)
        print("Hall of Famers data saved to 'hall_of_famers_by_conference.csv'")

    return hof_count


def plot_hof_by_conference_from_csv(
    csv_filename="hall_of_famers_by_conference.csv",
):
    data = pd.read_csv(csv_filename)
    data.set_index("Conference", inplace=True)
    data.plot(kind="bar")
    plt.ylabel("Number of Hall of Famers")
    plt.title("Number of Hall of Famers by Conference")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


# Example usage
tally_hof_by_conference(save_to_csv=True)
# plot_hof_by_conference_from_csv()
