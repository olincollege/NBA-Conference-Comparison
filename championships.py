from nba_api.stats.endpoints import franchisehistory
from conferences import get_teams_by_conference


def get_championships_by_conference():
    franchise_history = franchisehistory.FranchiseHistory(league_id="00")
    history_data = franchise_history.get_data_frames()[0]
    team_conferences = get_teams_by_conference()

    championships_tally = {"Eastern": 0, "Western": 0}

    for _, row in history_data.iterrows():
        team_id = row["TEAM_ID"]
        league_titles = row["LEAGUE_TITLES"]

        # Find the conference for the team
        conference = (
            "Eastern" if team_id in team_conferences["Eastern"] else "Western"
        )
        championships_tally[conference] += league_titles

    return championships_tally


print("Total championships by conference:")
print(get_championships_by_conference())
