from math import exp, sqrt
import yfinance as yf
import pandas
from prophet import Prophet
import pmdarima
from numpy.random import randn, seed

seed(2718)

def model_geometric_brownian_motion(S0, mu, sigma, tau, days_in_year):
    return round(S0 * exp((mu - (sigma ** 2) / 2.0) * (tau / days_in_year) - (sqrt(tau / days_in_year) * sigma * randn(1))), 2)


def model_arima(ticker, tau):
    symbol = pandas.read_csv("data/tickers.csv").query(f'name == "{ticker}"').symbol.iloc[0]
    data = yf.download(tickers=symbol, period="1mo", interval="1d")
    dataframe = pandas.DataFrame(data.iloc[:,4], data.index)
    
    model = pmdarima.auto_arima(
        dataframe, 
        start_p=0, 
        start_q=0,
        test='adf',
        max_p=5,
        max_q=5,
        m=1,
        d=None,
        seasonal=True,
        start_P=0, 
        D=0, 
        trace=True,
        start_Q=0,
        error_action='ignore',  
        suppress_warnings=True, 
        stepwise=True
    )

    return round(model.predict(tau).iloc[-1], 2)
    

def model_prophet(ticker, tau):
    symbol = pandas.read_csv("data/tickers.csv").query(f'name == "{ticker}"').symbol.iloc[0]
    data = yf.download(tickers=symbol, period="1y", interval="1d")
    dataframe = pandas.DataFrame(data.iloc[:,4], data.index)
    dataframe.columns = ["y"]
    dataframe["ds"] = list(dataframe.index)
    forecast = Prophet()
    forecast.fit(dataframe)
    future = forecast.make_future_dataframe(periods=tau)
    future.tail()
    forecast = forecast.predict(future)
    predict = float(forecast.iloc[-1].yhat)
    return round(predict, 2)
