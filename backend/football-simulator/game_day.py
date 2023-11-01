# Simulate some sunday football
# Season, week, producer for each game in a given week
# Delete the topic if it exists, then create it
# confluent_kafka.admin.AdminClient(conf)
# Just want it to run, create a bunch of producers then run its course. The data collection
# and other features can come right afterward. Good jumping off point.

import nfl_data_py as nfl
import threading
from producer import FootballProducer
from configparser import ConfigParser

config_parser = ConfigParser()
config_parser.read_file(open('config.ini'))
config = dict(config_parser['default'])


def game_day(season, week, speed=1):
    schedule = nfl.import_schedules([season])
    week_bool = (schedule['season'] == season) & (schedule['week'] == week)
    docket = schedule[week_bool]['game_id']
    threads = []
    for game in docket:
        prod = FootballProducer(config, game, speed)
        t = threading.Thread(target=prod.run_game)
        t.start()
        threads.append(t)


game_day(2022, 1, 2)

