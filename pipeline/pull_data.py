import nfl_data_py as nfl
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 1000)


def pull_wp_data(years, columns=None):
    df = nfl.import_pbp_data(years=years, columns=columns)
    df["time_elapsed"] = 3600 - df['game_seconds_remaining']
    for game in df.game_id.unique():
        mask = df['game_id'] == game
        if not (df.loc[mask, 'game_half'] == 'Overtime').empty:
            ot_mask = df['game_half'] == 'Overtime'
            df.loc[ot_mask, "time_elapsed"] = 4500 - df['game_seconds_remaining']
    return df

