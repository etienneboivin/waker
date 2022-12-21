import nfl_data_py as nfl
import pandas as pd
import numpy as np


def pull_data(years, columns=None):
    return nfl.import_pbp_data(years=years, columns=columns)
