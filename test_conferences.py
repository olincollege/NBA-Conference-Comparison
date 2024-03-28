import pytest
from pandas import DataFrame
from nba_api.stats.endpoints import leaguestandings
from conferences import get_teams_by_conference

# Mocking the data returned from the NBA API
MOCK_STANDINGS_DATA = DataFrame(
    {
        "TeamID": [1610612737, 1610612738, 1610612744, 1610612747],
        "Conference": ["East", "East", "West", "West"],
    }
)


@pytest.fixture
def mock_league_standings(mocker):
    """
    Pytest fixture to mock the LeagueStandings API call in the NBA API.

    This fixture replaces the real call to the LeagueStandings endpoint with a
    mock, allowing for controlled and predictable testing environments. It uses
    predefined data to simulate the response from the NBA API.

    Args:
        mocker: The pytest-mock mocker object used to patch objects for mocking.

    Returns:
        A mock object representing the LeagueStandings class with a mocked
        `get_data_frames` method.
    """
    mock = mocker.patch.object(leaguestandings, "LeagueStandings")
    mock.return_value.get_data_frames.return_value = [MOCK_STANDINGS_DATA]
    return mock


def test_get_teams_by_conference(mock_league_standings):
    """
    Test the get_teams_by_conference function to ensure accurate conference
    mapping.

    This test verifies that the get_teams_by_conference function correctly
    assigns NBA teams to their respective conferences based on the mocked
    data provided by the `mock_league_standings` fixture. The test checks if
    the function correctly parses and uses the data to segregate teams into
    the Eastern and Western conferences.

    Args:
        mock_league_standings: A pytest fixture that mocks the LeagueStandings
        API call, providing controlled data for testing.

    The test will pass if the function accurately maps teams to their
    respective conferences using the mocked LeagueStandings data.
    """
    expected = {
        "Eastern": [1610612737, 1610612738],
        "Western": [1610612744, 1610612747],
    }
    result = get_teams_by_conference("2022-23")
    assert result == expected
