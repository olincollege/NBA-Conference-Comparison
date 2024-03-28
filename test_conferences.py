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
    Fixture to mock LeagueStandings API call.
    """
    mock = mocker.patch.object(leaguestandings, "LeagueStandings")
    mock.return_value.get_data_frames.return_value = [MOCK_STANDINGS_DATA]
    return mock


def test_get_teams_by_conference(mock_league_standings):
    """
    Test to ensure teams are correctly separated into their conferences.
    """
    expected = {
        "Eastern": [1610612737, 1610612738],
        "Western": [1610612744, 1610612747],
    }
    result = get_teams_by_conference("2022-23")
    assert result == expected
