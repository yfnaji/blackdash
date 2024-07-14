# BlackDash Web App

BlackDash (Black-Scholes Dashboard) is a simple dynamic web app that provides the user an easy-to-use interface to calculate option prices for stocks in particular indices and provide relevant analyses.

This project is still a work in progress, there are several other features to be included as well as enhancing current functionalities.

<img width="1433" alt="blackdash-ui" src="https://github.com/user-attachments/assets/e09dfca7-8b49-43bf-9cc0-e433ea13e72f">

# Stock

<img width="225" alt="stock" src="https://github.com/user-attachments/assets/18a328b8-9dcf-49b9-9ed3-226a6f48c43a">

## Index

The stocks will be provided from the following indices:

* Dow Jones
* FTSE 100
* NIKKEI 225
* CAC 40
* DAX
* Strait Times Index
* Hang Seng Index
* Swiss Market Index
* Korea Composite Stock Price Index

## Period

There are 4 period intervals to pick from:

- Years
- Months
- Days
- Hours

The duration can be chosen which will in turn amend the graph to represent the stock price variations in that period.

# Prices

<img width="262" alt="prices" src="https://github.com/user-attachments/assets/317d2fad-97c5-48f9-aa0f-db3f8616cfa4">

The stock price is displayed under the `Prices` header along with its associated currency. The strike price can be configured any value for your option. 

`Calendar` days assumes 365 days in a year in the calculation of the option price, while `Trading` days assumes 252 days. There is currently ongoing work for a more sophisticated approach to dates by utilising the ISDA standard, and potentially others.

# Option Config

<img width="262" alt="option_pricing" src="https://github.com/user-attachments/assets/17e637df-d6dc-487f-a93c-6a7452d91614">

## European Options

An option where you may *only be exercised at the maturity date* is known as a *European Option*.

A European call option has value*:

$$
S\Phi\left(d_1\right) + Ke^{-r(T-t)}\Phi\left(d_2\right)
$$

where

$$d_1=\frac{\ln\left(S / K\right) + (r-\frac{\sigma^2}{2})(T-t)}{\sigma\sqrt{t}} \ \ \ \ \ \ \ d_2 = d_1-\sigma\sqrt{T-t}$$

The price for a put options is:

$$
Ke^{-r(T-t)}\Phi\left(-d_2\right) - S\Phi\left(-d_1\right)
$$

\* The the stock price $S$ will be adjusted for dividends.

## American Options

American options slightly differ to European options with the fact that the contract can be exercised at any point before the maturity date (as opposed to European options where one can only exercise at the maturity date).

This extra flexibility would make American options a little more valuable than it European counterpart, however, it is not straightforward to calculate its price. We often resort to numerical approximation schemes such as finite difference to price American options. In BlackDash, a variation of the Monte-Carlo method known as *Longstaff-Schwartz* has been implemented.

# Calculations

<img width="321" alt="calculations" src="https://github.com/user-attachments/assets/fe3b3c31-131e-464c-b064-0343f9d90d02">

The calculation for the `Option Price` has been provided in the previous section for European and American options.

The `Annual Return` is calculated as follows:

$$
\frac{\ln\left(S_N / S_0\right)}{\text{days} - 1}
$$

where $S_0$ and $S_N$ are first and last stock prices in the defined duration, and $\text{days}$ is the number of days until maturity.

## The Greeks

The Greeks are sensitivities of the option price with respect to certain parameters. They are defined as the following

* $\frac{\text{d}V}{\text{d}t} = \theta$ 

* $\frac{\text{d}V}{\text{d}S} = \Delta$

* $\frac{\text{d}^2V}{\text{d}S^2} = \Gamma$

* $\frac{\text{d}V}{\text{d}\sigma} = \nu$

* $\frac{\text{d}V}{\text{d}r} = \rho$

Example: for $\sigma$ we measure the change in the option price $V$ with respect to a change in a single unit of time $t$. If $\nu=2$ (volatility sensitivity), then the option price $V$ will increase by $2 when volatility moves up by 1.

## Volatility

<img width="190" alt="volatility" src="https://github.com/user-attachments/assets/c8312970-1788-4a68-aa00-3b91f0585639">

The *volatility* $\sigma$ is the magnitude of randomness of the asset price.

BlackDash calculates three types of volatilities:


* **Daily Volatility**: The average fluctutation from the mean price in $N$ days, calculated as:

$$
\sum^{N - 1}_{i=0} \frac{\left(\ln\left(S_i / S_{i+1}\right) - \frac{\ln\left(S_N / S_0\right)}{\text{N} - 1}\right)^2}{N - 2}
$$

* **Annual Volatility**: This is the same as the above but with fixed value $N=365$

* **Implied Volatility**: The *implied* volatility for a given option price - this is still a work in progress. Calculating the implied volatility requires solving an implicit function numerically. At the moment, the Brent-Dekker method has been implemented and will be enhanced in the future.

# Forcasting (Obsolete)

This section will be removed in the next iteration.
