from dash import Dash, Input, Output, dcc, html
from pipeline.pull_data import pull_data
import pandas as pd
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
        dcc.Store(id='pbp_data', storage_type='memory'),
        html.H1(children="Waker"),
        html.P(
            children="Test dashboard for Waker fantasy football app visualization",
        ),
        dcc.Graph(id='graph'),
        html.H4(children='Season'),
        dcc.Dropdown(
            id="season_dropdown",
            options=list(range(1999, 2022)),
            value=2022
        ),
        html.H4(children='Home Team'),
        dcc.Dropdown(
            id="home_dropdown",
            placeholder='Select a home team'
        ),
        html.H4(children='Away Team'),
        dcc.Dropdown(
            id="away_dropdown",
            placeholder='Select an away team'
        ),
        html.H4(children='Show/Hide Win Probabilities'),
        dcc.Checklist(
            id='checklist',
            options=['Home', 'Away'],
            value=['home_wp', 'away_wp'],
            inline=True
        )
    ])
# TODO:
# Visualization/Dashboard stuff:
# 1. Implement new pull_data() using ot_transform() DONE
# 2. Store and access that data DONE
# 3. More ways to expand functionality
#       - 'High-impact plays' (scores, turnovers)
#       - Highest win percentage swing plays
# 4. Possibly a database
# 5. How often is the play-by-play data updated? Is there a way to get it realtime? AWS?
# 6. Brock Purdy & SF Defense performance vs teams (strength of schedule)
# Fantasy stuff:
# 1. Look into OOP design pattern for storing player stats, teams, leagues, etc.
# 2. How to calculate projections more accurately


@app.callback(
    Output('pbp_data', 'data'),
    Input('season_dropdown', 'value')
)
def store_pbp_data(value):
    df = pull_data(years=value)
    return df.to_dict('records')


@app.callback(
    Output('home_dropdown', 'options'),
    Input('pbp_data', 'data')
)
def update_home_dropdown(data):
    df = pd.DataFrame(data)
    return df.home_team.unique()


@app.callback(
    Output('away_dropdown', 'options'),
    Input('pbp_data', 'data'),
    Input('home_dropdown', 'value')
)
def update_away_dropdown(data, home):
    df = pd.DataFrame(data)
    mask = df['home_team'] == home
    df = df.loc[mask, ]
    return df.away_team.unique()


@app.callback(
    Output("graph", "figure"),
    Input('pbp_data', 'data'),
    Input("home_dropdown", "value"),
    Input("away_dropdown", "value"),
    Input("checklist", "value")
)
def update_line_chart(data, home, away, checklist):
    df = pd.DataFrame(data)
    mask = (df['home_team'] == home) & (df['away_team'] == away)
    df = df.loc[mask, ]
    fig = px.line(df, x='time_elapsed', y=checklist)
    fig.update_layout(yaxis_range=[0, 1])
    return fig


app.run_server(debug=True)
