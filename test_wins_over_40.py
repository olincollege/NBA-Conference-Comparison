import pytest
from pandas import DataFrame
from nba_api.stats.endpoints import leaguestandings

# Replace 'nba_wins_analysis' with the actual name of your Python module where the function is defined
from wins_over_40 import get_wins_over_40_single_season


@pytest.fixture
def mock_standings_data():
    """
    A pytest fixture that provides mock NBA standings data.

    Generates a DataFrame mimicking the data from the LeagueStandings API
    endpoint, suitable for testing functions that require NBA standings data.

    Returns:
        DataFrame: A DataFrame with mock standings data for NBA teams.
    """
    return DataFrame(
        {
            "Conference": ["East", "East", "West", "West"],
            "WINS": [41, 39, 50, 55],
        }
    )


def test_get_wins_over_40_single_season(mocker, mock_standings_data):
    """
    Test get_wins_over_40_single_season function for correct win calculations.

    Verifies that the function accurately computes the number of wins over 40
    for teams in each conference using mocked standings data.

    Args:
        mocker: pytest-mock's mocker object to patch dependencies.
        mock_standings_data: Fixture providing mock data for NBA standings.

    The function is tested with a mock season. It checks that the function
    returns the correct tally of wins over 40 for each conference based on
    the mocked data.
    """
    # Mock the LeagueStandings API call to return controlled data
    mocker.patch.object(
        leaguestandings.LeagueStandings,
        "get_data_frames",
        return_value=[mock_standings_data],
    )

    season = "2021-22"
    result = get_wins_over_40_single_season(season)

    expected = {
        "Eastern Conference": 1,  # 41 - 40 = 1, 39 is not over 40
        "Western Conference": 25,  # 50 - 40 = 10, 55 - 40 = 15, total = 25
    }

    assert result == expected
