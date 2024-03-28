import pandas as pd
from nba_api.stats.endpoints import teamdetails
from conferences import get_teams_by_conference


def fetch_team_hof(team_id):
    """
    Fetch the number of Hall of Fame inductees for a given NBA team.

    Args:
        team_id (str): The identifier for the NBA team.

    Returns:
        int: The count of Hall of Fame inductees for the specified team.

    This function accesses the TeamDetails endpoint of the NBA API and
    retrieves the Hall of Fame inductees list for the specified team,
    returning the count of inductees.
    """
    details = teamdetails.TeamDetails(team_id=team_id)
    hof_data = details.get_data_frames()[
        5
    ]  # Assuming TeamHof is the sixth dataset (index 5)
    return len(hof_data)


def tally_hof_by_conference(save_to_csv=False):
    """
    Tally the number of Hall of Fame inductees by NBA conference.

    Args:
        save_to_csv (bool): If True, the tally will be saved to a CSV file.
                            Defaults to False.

    Returns:
        dict: A dictionary with the count of Hall of Fame inductees for each
        conference.

    This function iterates through all NBA teams, counts the Hall of Fame
    inductees for each, and aggregates these counts by conference. Optionally,
    it can save the results to a CSV file.
    """
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
