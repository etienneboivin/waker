from dash import Dash, Input, Output, dcc, html
from pipeline.pull_data import pull_wp_data
import pandas as pd
import plotly.express as px

data = pull_wp_data([2019])

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Waker",),
        html.P(
            children="Test dashboard for Waker fantasy football app visualization",
        ),
        dcc.Graph(id='graph'),
        html.H4(children='Home Team'),
        dcc.Dropdown(
            id="home_dropdown",
            options=data.home_team.unique()
        ),
        html.H4(children='Away Team'),
        dcc.Dropdown(
            id="away_dropdown",
            options=data.away_team.unique()
        ),
        html.H4(children='Show/Hide Win Probabilities'),
        dcc.Checklist(
            id='checklist',
            options=data.columns[94:96],
            value=data.columns[94:96],
            inline=True
        )
    ]
)


@app.callback(
    Output('away_dropdown', 'options'),
    Input('home_dropdown', 'value')
)
def update_away_dropdown(value):
    mask = data['home_team'] == value
    df = data.loc[mask, ]
    return df.away_team.unique()


@app.callback(
    Output("graph", "figure"),
    Input("home_dropdown", "value"),
    Input("away_dropdown", "value"),
    Input("checklist", "value")
)
def update_line_chart(home, away, checklist):
    mask = (data['home_team'] == home) & (data['away_team'] == away)
    df = data.loc[mask, ]
    fig = px.line(df, x='time_elapsed', y=checklist)
    fig.update_layout(yaxis_range=[0,1])
    return fig


app.run_server(debug=True)