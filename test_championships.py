import pytest
from pandas import DataFrame
from nba_api.stats.endpoints import franchisehistory
from championships import (
    get_championships_by_conference,
)  # Make sure this import is correct

# Mocking the data returned from the NBA API
MOCK_FRANCHISE_HISTORY = DataFrame(
    {
        "TEAM_ID": ["team_id_1", "team_id_2", "team_id_3", "team_id_4"],
        "LEAGUE_TITLES": [3, 2, 5, 4],
    }
)

# Mocking the conference data
MOCK_TEAM_CONFERENCES = {
    "Eastern": ["team_id_1", "team_id_2"],
    "Western": ["team_id_3", "team_id_4"],
}


@pytest.fixture
def mock_franchise_history(mocker):
    mock = mocker.patch.object(franchisehistory, "FranchiseHistory")
    mock.return_value.get_data_frames.return_value = [MOCK_FRANCHISE_HISTORY]
    return mock


@pytest.fixture
def mock_get_teams_by_conference(mocker):
    # Adjust "championships" to the actual module name where get_teams_by_conference is located
    return mocker.patch(
        "championships.get_teams_by_conference",
        return_value=MOCK_TEAM_CONFERENCES,
    )


def test_get_championships_by_conference(
    mock_franchise_history, mock_get_teams_by_conference
):
    """
    Test the get_championships_by_conference function for accuracy.

    This test ensures that the get_championships_by_conference function
    accurately calculates the total number of championships won by teams in
    each NBA conference. It uses mocked data to simulate the franchise history
    and team conference mappings.

    Args:
        mock_franchise_history: A pytest fixture that mocks the
                                FranchiseHistory endpoint of the NBA API.
        mock_get_teams_by_conference: A pytest fixture that mocks the function
                                    returning team-conference mappings.

    The test will pass if the function correctly calculates the total
    championships based on the mocked franchise history and team conference
    data.
    """
    expected = {
        "Eastern": 5,  # 3 from team_id_1 and 2 from team_id_2
        "Western": 9,  # 5 from team_id_3 and 4 from team_id_4
    }
    result = get_championships_by_conference(save_to_csv=False)
    assert result == expected
