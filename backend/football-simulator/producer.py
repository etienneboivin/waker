import nfl_data_py as nfl
import json
import sys
from time import sleep
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Producer


class FootballProducer:
    def __init__(self, config, game_id, speed):
        self.game_id = game_id
        self.speed = speed
        self.producer = Producer(config)

    def run_game(self):
        pbp = nfl.import_pbp_data([int(self.game_id[:4])])
        pbp_reduced = pbp[pbp["game_id"] == self.game_id].iloc[1:, :]  # skip first row, garbage line
        # transform to time elapsed, take diff
        pbp_reduced['game_seconds_elapsed'] = 3600 - pbp_reduced['game_seconds_remaining'].copy()
        pbp_reduced['diff'] = (pbp_reduced['game_seconds_elapsed'].diff()).copy()
        first_line = True

        for row in pbp_reduced.to_dict('records'):
            try:
                if first_line is True:
                    timestamp, desc, game_id = row['time'], row['desc'], row['game_id']
                    topic = game_id[:7]
                    result = {}
                    result[timestamp] = desc
                    jresult = json.dumps(result)
                    first_line = False

                    self.producer.produce(topic=topic, key=game_id, value=jresult, callback=callback)

                else:
                    timestamp, desc, game_id, diff = row['time'], row['desc'], row['game_id'], float(row['diff'])
                    topic = game_id[:7]
                    result = {}
                    result[timestamp] = desc
                    jresult = json.dumps(result)
                    diff /= self.speed

                    sleep(diff)

                    self.producer.produce(topic=topic, key=game_id, value=jresult, callback=callback)

                self.producer.flush()

            except TypeError:
                sys.exit()


def callback(err, msg):
    if err is not None:
        print('Failed to deliver message: %s: %s' %(str(msg.value()), str(err)))
    else:
        print('Message produced: %s' % (str(msg.value())))


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('config_file', type=FileType('r'), default="config.ini")
    parser.add_argument('game_id', type=str)
    # parser.add_argument('game_id', type=str,
    #                     help='Game ID formatted YYYY_WW_AWAY_HOME')
    parser.add_argument('--speed', type=float, default=1, required=False,
                        help='Speed up time series by a given multiplicative factor.')
    args = parser.parse_args()

    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    producer = FootballProducer(config, args.game_id, args.speed)
    producer.run_game()


if __name__ == '__main__':
    main()
