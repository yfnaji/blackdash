from dash.dependencies import Input, Output
from dash import html
from layouts import (
    div_amer_euro,
    div_maturity,
    div_call_put,
    div_vol_annual,
    div_vol_implied,
    div_vol_days,
    block_stock,
    price_stock,
    price_strike,
    div_calcs,
    div_days
)
import dash_bootstrap_components as dbc
from dash import dcc
import plotly.graph_objects as go
import callbacks
import plotly.express as px


image_path = "assets/BlackDash-Vector.svg"

fig = go.Figure(data=px.line())

fig.layout = go.Layout(
             paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
)
fig['data'][0]['line']['color']='rgb(204, 204, 204)'
graph = html.Div(
    dcc.Graph(id='graph', figure=fig),
    className="graph"
)

top = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Img(src=image_path)
                    ],
                    className="div-stock-logo"
                ),
                html.Div(
                    block_stock,
                    className="div-stock-content"
                ),
            ],
            className="div-stock" 
        ),
        html.Div(
            graph,
            className="div-graph"
        )
    ],
    className="row1"
)

bottom = html.Div(
    [
        html.Div(
            [
                html.H3("Prices"),
                price_stock,
                price_strike,
                div_days
            ],
            className="div-config"
        ),
            html.Div(
                [
                    html.H3("Option Config"),
                    div_amer_euro,
                    div_call_put,
                    div_maturity
                ],
                className="div-config"
        ),
            html.Div(
                [
                    html.H3("Calculations"),
                    div_calcs
                ],
                className="div-config"
        ),
            html.Div(
                [
                    html.H3("Volatility"),
                    div_vol_annual,
                    div_vol_implied,
                    div_vol_days
                ],
                className="div-config"
        ),
            html.Div(
                [
                    html.H3("Forecasting"),
                    html.H5("Geometric Brownian Motion"),
                    html.H5(id="gbm"),
                    html.H5("Prophet"),
                    html.H5(id="prophet"),
                    html.H5("ARIMA"),
                    html.H5(id="arima"),
                ],
                className="div-config"
        ),
    ],
    className="row2"
)

layout = html.Div([top, bottom])
