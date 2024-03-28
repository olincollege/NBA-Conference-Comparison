import pytest
from pandas import DataFrame
from nba_api.stats.endpoints import leaguestandings

# Replace 'nba_wins_analysis' with the actual name of your Python module where the function is defined
from wins_over_40 import get_wins_over_40_single_season


@pytest.fixture
def mock_standings_data():
    return DataFrame(
        {
            "Conference": ["East", "East", "West", "West"],
            "WINS": [41, 39, 50, 55],
        }
    )


def test_get_wins_over_40_single_season(mocker, mock_standings_data):
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
        "Western Conference": 25,  # 50 - 40 = 10, 55 - 40 = 15, total = 25 but seems there was a mistake in calculation, adjust as necessary
    }

    assert result == expected
