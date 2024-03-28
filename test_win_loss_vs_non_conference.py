import pytest
from pandas import DataFrame
from nba_api.stats.endpoints import leaguegamefinder
from datetime import datetime
from win_loss_versus_non_conference import (
    get_inter_conference_win_loss_records,
    aggregate_inter_conference_win_loss_records,
)

# Mock data for LeagueGameFinder response
MOCK_GAME_FINDER_DATA = DataFrame(
    {"TEAM_ID": [1, 2, 3, 4], "WL": ["W", "L", "W", "L"]}
)


@pytest.fixture
def mock_game_finder(mocker):
    """
    A pytest fixture that mocks the LeagueGameFinder API call.

    This fixture creates a mock of the LeagueGameFinder class from the
    nba_api.stats.endpoints module, specifically mocking the `get_data_frames`
    method to return predefined data. This allows for controlled testing of
    functions that depend on the LeagueGameFinder's output.

    Args:
        mocker: The pytest-mock's mocker object used for setting up the mock.

    Returns:
        A mock object representing the LeagueGameFinder class with a mocked
        `get_data_frames` method.
    """
    return mocker.patch.object(
        leaguegamefinder,
        "LeagueGameFinder",
        return_value=mocker.Mock(
            get_data_frames=mocker.Mock(return_value=[MOCK_GAME_FINDER_DATA])
        ),
    )


def test_get_inter_conference_win_loss_records(mock_game_finder):
    """
    Test the get_inter_conference_win_loss_records function for accuracy in
    calculating win-loss records.

    This test verifies that the get_inter_conference_win_loss_records function
    correctly calculates the win-loss records for Eastern and Western
    conferences based on mocked game data. It checks if the function processes
    the data correctly to produce the expected win-loss records.

    Args:
        mock_game_finder: A pytest fixture that mocks the LeagueGameFinder API
                            call, ensuring that the function under test uses
                            predetermined, controlled data for its calculations.

    The test will pass if the function returns the correct win-loss records for each conference as expected
    from the mocked data.
    """
    season = "2021-22"
    result = get_inter_conference_win_loss_records(season)
    expected = {
        "Eastern": {"Wins": 2, "Losses": 2},
        "Western": {"Wins": 2, "Losses": 2},
    }
    assert result == expected
