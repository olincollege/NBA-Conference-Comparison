from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import franchisehistory
from nba_api.stats.static import teams
from nba_api.stats.static import players

from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard

import pandas as pd
import matplotlib_inline as plt
import datetime


if __name__ == "__main__":

    nba_teams = teams.get_teams()
    nba_players = players.get_players()

    # print(nba_players)
    print(len(nba_players))
