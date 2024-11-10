from dash import Input, Output
import plotly.express as px
import pandas as pd
import yfinance as yf
from calculations.blackscholes import BlackScholes
from app import app
import plotly.graph_objects as go
import plotly.express as px
from calculations.forecast import (
    model_geometric_brownian_motion, 
    model_arima, 
    model_prophet
)


@app.callback(
    Output("graph", "figure"),
    Output("stock", "children"),
    Output("period_no", "min"),
    Output("period_no", "max"),
    Output("period_no", "value"),
    Input("ticker", "value"),
    Input("period_no","value"),
    Input("period_type","value"),
    Input("plot", "value")
)
def update_figure(name, period_no, period_type, plot):
    
    _period_map = {
        0: {
            "hours": {"code": "h", "max": 24, "min": 1},
            "days": {"code": "d", "max": 30, "min": 1},
            "months": {"code": "mo", "max": 12, "min": 1},
            "years": {"code": "y", "max": 5, "min": 1}
        },
        1: {
            "hours": {"code": "h", "max": 24, "min": 1},
            "days": {"code": "d", "max": 3, "min": 1},
            "months": {"code": "mo", "max": 3, "min": 1},
            "years": {"code": "y", "max": 3, "min": 1}
        }
    }

    _interval_map = {
        0 : {
                "hours": "1m",
                "days": "1m",
                "months": "1h",
                "years": "1d"
        },
        1 : {
                "hours": "1m",
                "days": "1m",
                "months": "1d",
                "years": "1d" 
        }
    }

    _min = _period_map[plot][period_type]["min"]
    _max = _period_map[plot][period_type]["max"]

    if not _min <= period_no <= _max:
        period_no = _min 

    period = str(period_no) + _period_map[plot][period_type]["code"]
    ticker = pd.read_csv("data/tickers.csv").query(f'name == "{name}"').symbol
    interval = _interval_map[plot][period_type]

    data = yf.download(tickers=ticker.iloc[0], period=period, interval=interval)

    if plot:
        fig = go.Figure(px.line(data.Close, x=data.index, y="Close"))
    else:
        def _split_data(data, period):
            if period == "hours":
                window = 10
            else:
                window = 7

            lag = (len(data) % window)
            box_data = []

            for i in range(lag, len(data), window):
                r = [x for x in range(i, i + window)]
                box_data.append(data.iloc[r]["Adj Close"])
            
            box_data_T = []        
            for i in range(window):
                temp = []
                for j in range(len(box_data)):
                    temp.append(box_data[j][i])
                box_data_T.append(temp)

            return box_data_T, [x.index[0] for x in box_data]

        box_data, box_index = _split_data(data, period_type)
        fig = go.Figure(px.box(y=box_data, x=box_index))

    fig.layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',

    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='Gray', color="white")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Gray', color="white", title_font_color="red")
    fig.update_layout(
        xaxis_title=f"Time",
        yaxis_title=f"Stock Price",
        width=1000,
        height=500
    )
    fig.update_traces(line_color='#28788C')

    return fig, round(data["Close"].iloc[-1], 2), _min, _max, period_no


@app.callback(
    Output("ticker", "options"),
    Output("stock-currency", "children"),
    Output("exchange", "children"),
    Output("ticker", "value"),
    Output("currency", "value"),
    Input("index", "value"),
    Input("ticker", "value"),
    Input("currency", "value"),
)
def query(index, ticker, user_currency):
    data = pd.read_csv("data/tickers.csv").query(f'stockindex == "{index}"')
    currency = data.iloc[0].currency
    
    stock_list = list(data.query(f'stockindex == "{index}"').name)
    
    if ticker not in stock_list:
        ticker = stock_list[0]
    
    exchange = data.query(f'name == "{ticker}"').exchange.iloc[0]
    
    return stock_list, currency, exchange, ticker, user_currency



@app.callback(
    Output("option-price", "children"),
    Output("mu", "children"),
    Output("sigma-annual", "children"),
    Output("delta", "children"),
    Output("gamma", "children"),
    Output("vega", "children"),
    Output("theta", "children"),
    Output("rho", "children"),
    Output("sigma-implied", "children"),
    Output("sigma-daily", "children"),
    Input("ticker", "value"),
    Input("maturity_days", "value"),
    Input("strike", "value"),
    Input("option", "value"),
    Input("stock", "children"),
    Input("american", "value"),
    Input("vol-days-input", "value"),
    Input("currency", "value"),
    Input("sigma-implied-input", "value"),
    Input("days_in_year", "value")
)
def calculations(
        ticker, 
        maturity_days, 
        strike, 
        put_option, 
        stock_price, 
        american, 
        vol_days,
        currency,
        implied_option_price,
        days_in_year
    ):

    _american = True if american else False
    _put_option = True if put_option else False
    
    if not strike:
        if _put_option:
            strike = stock_price * 1.1
        else:
            strike = stock_price * 0.9

    symbol = pd.read_csv("data/tickers.csv").query(f'name == "{ticker}"').symbol.iloc[0]

    model = BlackScholes(
        ticker=symbol,
        stock_price=stock_price,
        put_option=_put_option,
        strike=strike,
        maturity_days=maturity_days,
        currency=currency,
        american=_american,
        days_in_year=days_in_year
    )

    data = model.option_calculations()
    currency_round = 0 if currency in ("JPY", "KRW") else 2

    return (
        round(data["option_price"], currency_round),
        model.mu,
        model.sigma,
        data["delta"],
        data["gamma"],
        data["vega"],
        data["theta"],
        data["rho"],
        model.implied_volatility(implied_option_price),
        model.daily_volatility(vol_days) if vol_days else "N/A",
    )

@app.callback(
    Output("gbm", "children"),
    Output("arima", "children"),
    Output("prophet", "children"),
    Input("ticker", "value"),
    Input("maturity_days", "value"),
    Input("mu", "children"),
    Input("sigma-annual", "children"),
    Input("stock", "children"),
    Input("days_in_year", "value")
)
def forecasts(ticker, maturity_days, mu, sigma, S0, days_in_year):
    return (
        model_geometric_brownian_motion(S0, mu, sigma, maturity_days, days_in_year),
        model_arima(ticker, maturity_days),
        model_prophet(ticker, maturity_days)
    )
