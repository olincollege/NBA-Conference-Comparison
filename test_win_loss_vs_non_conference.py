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
    return mocker.patch.object(
        leaguegamefinder,
        "LeagueGameFinder",
        return_value=mocker.Mock(
            get_data_frames=mocker.Mock(return_value=[MOCK_GAME_FINDER_DATA])
        ),
    )


def test_get_inter_conference_win_loss_records(mock_game_finder):
    season = "2021-22"
    result = get_inter_conference_win_loss_records(season)
    expected = {
        "Eastern": {"Wins": 2, "Losses": 2},
        "Western": {"Wins": 2, "Losses": 2},
    }
    assert result == expected
