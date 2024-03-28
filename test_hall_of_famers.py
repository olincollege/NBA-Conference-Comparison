import pytest
from pandas import DataFrame
from nba_api.stats.endpoints import teamdetails
from hall_of_famers import fetch_team_hof

# Mock data for TeamDetails response
MOCK_TEAM_DETAILS_HOF = DataFrame({"HOF": ["Player1", "Player2", "Player3"]})


def test_fetch_team_hof(mocker):
    # Mock the TeamDetails API call to return controlled data
    mock_team_details = mocker.patch.object(teamdetails, "TeamDetails")
    mock_team_details.return_value.get_data_frames.return_value = [
        None,
        None,
        None,
        None,
        None,
        MOCK_TEAM_DETAILS_HOF,
    ]

    team_id = "team_id_1"
    assert (
        fetch_team_hof(team_id) == 3
    )  # Expecting 3 Hall of Famers from the mocked data
