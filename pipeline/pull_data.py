import nfl_data_py as nfl
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 1000)


<<<<<<< HEAD
def pull_data(years, columns=None):
    return nfl.import_pbp_data(years=years, columns=columns)


def pull_wp_data(years):
    df = nfl.import_pbp_data(years=years)
    df.loc[:, 'time_elapsed'] = 3600 - df['game_seconds_remaining'].copy()
    for game_id in df['game_id'].unique():
        game_mask = (df['game_id'] == game_id)
        if not df.loc[game_mask, 'game_half'].isin(['Overtime']).empty:
            ot_mask = (df['game_half'] == 'Overtime')
            df.loc[ot_mask, 'time_elapsed'] = 4500 - df['game_seconds_remaining'].copy()
    return df
def pull_wp_data(years, columns=None):
    df = nfl.import_pbp_data(years=years, columns=columns)
    df["time_elapsed"] = 3600 - df['game_seconds_remaining']
    for game in df.game_id.unique():
        mask = df['game_id'] == game
        if not (df.loc[mask, 'game_half'] == 'Overtime').empty:
            ot_mask = df['game_half'] == 'Overtime'
            df.loc[ot_mask, "time_elapsed"] = 4500 - df['game_seconds_remaining']
    return df

