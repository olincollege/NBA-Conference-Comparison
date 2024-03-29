import pandas as pd
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import franchisehistory
from conferences import get_teams_by_conference


def get_championships_by_conference(save_to_csv=False):
    """
    Fetches the number of championships won by teams in each conference.

    This function retrieves the franchise history from the NBA API to count the
    total number of league championships won by teams in the Eastern and
    Western conferences. It can optionally save the results to a CSV file.

    Args:
        save_to_csv (bool): If True, saves the championship tally to a CSV file.
                            Defaults to False.

    Returns:
        dict: A dictionary containing the total number of championships for each
            conference with keys 'Eastern' and 'Western'.

    Example:
        >>> get_championships_by_conference(save_to_csv=True)
        {'Eastern': 3, 'Western': 5}
    """
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
        conference = "Eastern" if team_id in team_conferences["Eastern"] else "Western"
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
