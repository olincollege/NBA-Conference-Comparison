import pytest
from pandas import DataFrame
from nba_api.stats.endpoints import teamdetails
from hall_of_famers import fetch_team_hof

# Mock data for TeamDetails response
MOCK_TEAM_DETAILS_HOF = DataFrame({"HOF": ["Player1", "Player2", "Player3"]})


def test_fetch_team_hof(mocker):
    """
    Test the fetch_team_hof function to ensure it accurately counts Hall of
    Famers.

    This test verifies that the fetch_team_hof function correctly fetches and
    counts the number of Hall of Fame inductees for a given team. It uses a
    mock of the TeamDetails endpoint from the NBA API to provide controlled
    return data for testing.

    Args:
        mocker: The pytest fixture used to mock dependencies for testing.

    The function is tested with a mock team ID, and the test checks if the
    function correctly interprets the mocked data and returns the expected
    count of Hall of Famers for that team.

    The test will pass if the function returns the correct number of Hall of
    Famers based on the mocked data.
    """
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
