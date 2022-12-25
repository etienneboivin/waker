import nfl_data_py as nfl
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 1000)
def pull_data(years, columns=None):
    return nfl.import_pbp_data(years=years, columns=columns)
