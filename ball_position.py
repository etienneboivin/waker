from pull_data import pull_data
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from football_field import create_football_field

# Example game used, Super Bowl LIV
data = pull_data([2019])
superb_owl = data[data["game_id"] == "2019_21_SF_KC"]
superb_owl = superb_owl.dropna(axis=0, how='all')
superb_owl_subset = superb_owl[['posteam', 'game_seconds_remaining', 'yardline_100', 'yards_gained']]
superb_owl_subset = superb_owl_subset.dropna(axis=0, how='any')

# Endpoint of ball position line after play
superb_owl_subset['new_los'] = superb_owl_subset['yardline_100'] - superb_owl_subset['yards_gained']
superb_owl_subset['color'] = 'red'
superb_owl_subset['color'].mask(superb_owl_subset['posteam'] == 'SF', 'gold', inplace=True)

game_time = superb_owl_subset['game_seconds_remaining']
los = superb_owl_subset['yardline_100']
gained = superb_owl_subset['yards_gained']
new_los = superb_owl_subset['new_los']
colors = superb_owl_subset['color']

fig, ax = create_football_field() # TODO: Not graphing all lines when this is used as ax?
ax.hlines(y=game_time, xmin=los,
           xmax=new_los, colors=colors, lw=4)
plt.show()