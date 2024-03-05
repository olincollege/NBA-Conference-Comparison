from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import franchisehistory
from nba_api.stats.static import teams
from nba_api.stats.static import players

from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard

import pandas as pd
import datetime

nba_teams = teams.get_teams()
nba_players = players.get_players()

print(nba_players)
