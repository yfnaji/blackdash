import yfinance as yf
from scipy.stats import norm
from math import sqrt, exp, log
import numpy as np
from .brentdekker import BrentDekker
import subprocess


class BlackScholes:

    def parameters(self, period="1y", calculate_drift=False):
        data = yf.download(tickers=self.ticker, period=period, interval="1d")
        days = len(data)
        s0 = data.iloc[0].Close
        sN = data.iloc[-1].Close
        data = data[::-1]

        avg_returns = log(sN / s0) / (days - 1)
        
        volatility = 0
        for i in range(len(data) - 1):
            lr = log(data.iloc[i].Close / data.iloc[i+1].Close)
            volatility += (lr - avg_returns) ** 2

        volatility /= days - 2

        if calculate_drift:
            drift = days * (avg_returns + (volatility) / 2)
            return drift, sqrt(days * volatility)

        volatility = sqrt(days * volatility)

        return volatility
    
    def _d1(self, implied_volatility_sigma=None):
        sigma = implied_volatility_sigma if implied_volatility_sigma else self.vol
        d1_numerator = np.log(self.stock_price / self.strike)
        d1_numerator += (self.drift + (sigma ** 2) / 2.0) * (self.tau)
        d1_denominator = sigma * sqrt(self.tau)
        return d1_numerator / d1_denominator

    def __init__(self, ticker, stock_price, strike, maturity_days, currency, put_option, american, days_in_year):
        
        def currency_converter(currency_from, currency_to):
            if currency_from == "USD":
                currency_ticker = currency_to
            else:
                currency_ticker = currency_from + currency_to
        
            currency_ticker += "=X"
            
            factor = yf.download(tickers=currency_ticker).iloc[-1].Close
            return factor

        self.ticker = ticker
        self.stock_price = stock_price[0]
        self.strike = strike

        self.tau = maturity_days / days_in_year
        self.days_in_year = days_in_year
        self.maturity_days = maturity_days
        self.put_option = put_option
        self.drift, self.vol = self.parameters(calculate_drift=True)
        self.american = american
        self.optimal_stop_time = None

        home_currency = yf.Ticker(ticker=self.ticker).info["currency"]
        same_currency = True if home_currency == currency else False
        self.currency_factor = currency_converter(home_currency, currency) if not same_currency else 1

    @property
    def mu(self):
        return round(self.drift, 5)

    @property
    def sigma(self):
        return round(self.vol, 5)

    def vega(self, implied_volatility_sigma=None):
        sigma = implied_volatility_sigma if implied_volatility_sigma else self.vol
        return self.stock_price * sqrt(self.tau) * norm.pdf(self._d1(sigma))

    def european_option_price(self, implied_volatility_sigma=None):

        sigma = implied_volatility_sigma if implied_volatility_sigma else self.vol
        d1 = self._d1(sigma)
        d2 = d1 - sigma * sqrt(self.tau)

        sgn = -1 if self.put_option else 1
        option_price = sgn * self.stock_price * norm.cdf(sgn * d1)
        option_price += -sgn * self.strike * exp(-self.drift * self.tau) * norm.cdf(sgn * d2)
        option_price *= self.currency_factor
        return option_price
    
    def american_option_price(self, implied_volatility_sigma=None):
        
        sigma = implied_volatility_sigma if implied_volatility_sigma else self.vol
        count = 0
        while True:

            command = [
                    "./calculations/longstaffschwartz/longstaffschwartz.sh", 
                    f"{self.drift}", 
                    f"{sigma}", 
                    f"{self.maturity_days}",
                    f"{self.stock_price}", 
                    f"{self.strike}",
                    f"{1 if self.put_option else 0}",
                    f"{self.days_in_year}"
                ]
            _data = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8")
            _data = _data.split()
            count += 1
            if float(_data[0]) > self.european_option_price(sigma) or count < 100:
                for i in range(len(_data)):
                    _data[i] = float(_data[i])
                break
        if implied_volatility_sigma:
            data = {
                "option_price": _data[0],
                "vega": _data[3]
            }
        else:
            data = {
                "option_price": _data[0] * self.currency_factor,
                "delta": round(_data[1], 5),
                "gamma": round(_data[2], 5),
                "vega": round(_data[3], 5),
                "rho": round(_data[4], 5),
                "theta": round(_data[5], 5)
            }

        return data


    def option_calculations(self):
        
        if self.american:
            data = self.american_option_price()

        else:
            option_price = self.european_option_price()
            d1 = self._d1()
            d2 = d1 - self.vol * sqrt(self.tau)
            delta = norm.cdf(d1)
            if self.put_option:
                delta -= 1.0
            gamma = (self.stock_price * self.vol * sqrt(self.tau))
            gamma = norm.pdf(d1) / gamma
            # vega = self.vega()
            sgn = -1 if self.put_option else 1
            rho = sgn * self.strike * self.tau * norm.cdf(sgn * d2)
            rho *= exp(-self.drift * self.tau)
            theta = (-self.stock_price * self.vol / (2 * sqrt(self.tau))) * norm.pdf(d1)
            theta += - sgn * self.drift * self.strike * exp(-self.drift * self.tau) * norm.cdf(sgn * d2)
            data = {
                "option_price": option_price * self.currency_factor,
                "delta": round(delta, 5),
                "gamma": round(gamma, 5),
                "vega": round(self.vega(), 5),
                "rho": round(rho, 5),
                "theta": round(theta, 5)
            }

        return data


    def implied_volatility(self, option_value):

        if not option_value:
            return "N/A"

        if self.american:
            def func(x):
                data = self.american_option_price(x)
                return {"f": data["option_price"] - option_value, "vega": data["vega"]}
        else:
            def func(x):
                return {"f": self.european_option_price(x) - option_value, "vega": self.vega(x)}
        
        sigma_prev = self.vol
        value = func(sigma_prev)
        sigma = sigma_prev - (value["f"] / value["vega"])
        i = 0

        while abs(sigma - sigma_prev) > 1e-5 and value["vega"]  > 1e-2 and i < 1000:
            i += 1
            
            value = func(sigma_prev)

            sigma_prev = sigma
            sigma = sigma_prev - (value["f"] / value["vega"])

            if abs(sigma) == np.inf:
                sigma = sigma_prev
                break
        
        sigma_newton = round(sigma, 5)

        func = lambda x: self.american_option_price(x)["option_price"] - option_value if self.american else self.european_option_price(x) - option_value

        a = self.vol # * (self.stock_price / self.european_option_price())
        fa = func(a)
        i = 0
        while i < 100:
            i += 0.01
            i = round(i, 2)
            b_plus = func(a + i)

            b_minus = func(a - i)

            if b_plus * fa < 0:
                b = self.vol + i
                break
            elif b_minus * fa < 0:
                b = self.vol - i
                break
        
        if b != 0 and not b:
            sigma_brentdekker = None
        else:
            try:
                sigma_brentdekker = round(BrentDekker(func, (a, b)).interpolate(), 5)
            except:
                sigma_brentdekker = None

        if sigma_newton and sigma_brentdekker:
            return min(abs(sigma_newton), abs(sigma_brentdekker))
        elif sigma_newton:
            return abs(sigma_newton)
        elif sigma_brentdekker:
            return abs(sigma_brentdekker)
        else:
            return "N/A"

    def daily_volatility(self, days):
        return round(self.parameters(period=f"{days}d"), 5)
