import json
import uuid

class Play:
    def __init__(self):
        self.play_id = str(uuid.uuid4().int) # uuid
        self.game_id = '' # game_id
        self.posteam = '' # posteam
        self.yardline = '' # yrdln
        self.yardline_100 = '' # yardline_100
        self.game_seconds = '' # game_seconds_remaining
        self.quarter = '' # qtr
        self.goal_bool = '' # goal_to_go
        self.game_time = '' # time
        self.ydstogo = '' # ydstogo
        self.play_desc = '' # desc

class Game:
    def __init__(self):
        self.game_id = '' # game_id
        self.date = '' # game_date
        self.home_team = '' # home_team
        self.away_team = '' # away_team
        self.season_type = '' # season_type
