import pytest
from pandas import DataFrame
from nba_api.stats.endpoints import leaguestandings
from datetime import datetime

# Assuming these functions are in 'conference_win_loss.py'
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
    return mocker.patch.object(
        leaguestandings.LeagueStandings,
        "get_data_frames",
        return_value=[MOCK_STANDINGS_DATA],
    )


def test_get_single_season_conference_win_loss_records(mock_league_standings):
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
