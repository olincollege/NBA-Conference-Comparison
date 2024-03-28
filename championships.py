import pandas as pd
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import franchisehistory
from conferences import get_teams_by_conference


def get_championships_by_conference(save_to_csv=False):
    franchise_history = franchisehistory.FranchiseHistory(league_id="00")
    history_data = franchise_history.get_data_frames()[0]

    # Get unique franchises based on franchise ID or similar unique identifier
    unique_franchises = history_data.drop_duplicates(subset=["TEAM_ID"])

    team_conferences = get_teams_by_conference()
    championships_tally = {"Eastern": 0, "Western": 0}

    for _, row in unique_franchises.iterrows():
        team_id = row["TEAM_ID"]
        league_titles = row["LEAGUE_TITLES"]

        # Find the current conference for the team
        conference = (
            "Eastern" if team_id in team_conferences["Eastern"] else "Western"
        )
        championships_tally[conference] += league_titles

    if save_to_csv:
        df = pd.DataFrame(
            list(championships_tally.items()),
            columns=["Conference", "Championships"],
        )
        df.to_csv("championships_by_conference.csv", index=False)
        print(
            "Championships by conference data saved to 'championships_by_conference.csv'"
        )

    return championships_tally


# Example usage
print("Total championships by conference:")
championships_by_conference = get_championships_by_conference(save_to_csv=True)
print(championships_by_conference)


def plot_championships_by_conference_from_csv(
    csv_filename="championships_by_conference.csv",
):
    # Read the championships data from the CSV file
    data = pd.read_csv(csv_filename)

    # Set up the bar chart
    fig, ax = plt.subplots()
    ax.bar(data["Conference"], data["Championships"], color=["blue", "red"])

    # Add some text for labels and title
    ax.set_ylabel("Number of Championships")
    ax.set_title("NBA Championships by Conference")
    ax.set_xticks(data["Conference"])
    ax.set_xticklabels(data["Conference"])

    # Show the plot
    plt.show()


# Example usage
# plot_championships_by_conference_from_csv()
