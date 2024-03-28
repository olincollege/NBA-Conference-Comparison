import pytest
from pandas import DataFrame
from nba_api.stats.endpoints import leaguestandings
from datetime import datetime
from win_loss import (
    get_single_season_conference_win_loss_records,
    aggregate_conference_win_loss_records,
)

# Sample data for the league standings
MOCK_STANDINGS_DATA = DataFrame(
    {
        "Conference": ["East", "East", "West", "West"],
        "WINS": [42, 38, 50, 48],
        "LOSSES": [40, 44, 32, 34],
    }
)


@pytest.fixture
def mock_league_standings(mocker):
    """
    A pytest fixture that mocks the LeagueStandings API call.

    This fixture mocks the 'get_data_frames' method of the LeagueStandings
    class in the nba_api.stats.endpoints module. It provides controlled,
    predictable data for testing functions that depend on the output of the
    LeagueStandings API call.

    Args:
        mocker: The pytest-mock's mocker object used for setting up the mock.

    Returns:
        A mock object representing the LeagueStandings class with a mocked
        `get_data_frames` method.
    """
    return mocker.patch.object(
        leaguestandings.LeagueStandings,
        "get_data_frames",
        return_value=[MOCK_STANDINGS_DATA],
    )


def test_get_single_season_conference_win_loss_records(mock_league_standings):
    """
    Test the get_single_season_conference_win_loss_records function for
    accuracy.

    This test verifies that the get_single_season_conference_win_loss_records
    function accurately calculates the win-loss records for the Eastern and
    Western conferences based on the mocked data provided by the
    `mock_league_standings` fixture.

    Args:
        mock_league_standings: A pytest fixture that mocks the LeagueStandings
                                API call, ensuring that the function under test
                                uses controlled data for its calculations.

    The test will pass if the function accurately computes the win-loss records
    for each conference as expected from the mocked standings data.
    """
    season = "2021-22"
    result = get_single_season_conference_win_loss_records(season)
    expected = {
        "Eastern Conference": {
            "Wins": 80,
            "Losses": 84,
        },  # Sum of East teams' wins and losses
        "Western Conference": {
            "Wins": 98,
            "Losses": 66,
        },  # Sum of West teams' wins and losses
    }
    assert result == expected
