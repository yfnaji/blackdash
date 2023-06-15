from dash import dcc, html
import pandas as pd
import dash_bootstrap_components as dbc


data = pd.read_csv("data/tickers.csv")
tickers = data.name
stockindex = list(data.stockindex.unique())
currencies = list(data.currency.unique())
stock_default = stockindex[0]


stock = tickers[0]

block_stock = html.Div(
    [
        html.H5(
            [
                "By Yasser Naji | ",
                "v1.0.1 | ",
                html.A(
                    "GitHub", 
                    href="https://github.com/yfnaji/blackdash",
                    target="_blank",
                    rel="noopener noreferrer"
                ),
                
            ], 
            className="author"
        ),
        html.H2("Stock"),
        html.H5("Index", className="header-h5"),
        dcc.Dropdown(stockindex, value=stock_default, className="black-dropdown", id="index", clearable=False),
        html.H5("Stock", className="header-h5"),
        dcc.Dropdown(tickers, value=stock, className="black-dropdown", id="ticker", clearable=False),
        html.Div(
            [
                html.H5("Exchange:", className="exchange-h5"),
                html.H5(id="exchange", className="exchange-h5")
            ],
            className="row-div"
        ),
        html.H5("Period", className="header-h5"),
        html.Div(
            [
                dcc.Input(
                        value=1, 
                        id="period_no",
                        type="number",
                        className="input-box",
                    ),
                dcc.Dropdown(
                    [
                        "years",
                        "months",
                        "days",
                        "hours",
                    ],
                    value="years",
                    className="period-dropdown",
                    id="period_type",
                    clearable=False,
                ),
            ],
            className="row-div"
        ),
        html.H5("Plot", className="header-h5"),
        html.Div(
            dbc.RadioItems(
            options=[
                    {"label":"Box", "value": 0},
                    {"label":"Line", "value": 1}
                ],
                id="plot",
                value=1,
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
            ),
            className="radio-group",
        )
    ]
)

price_stock = html.Div(
    [
        html.H5("Stock Price"),
        html.Div(
            [
                html.H5(id="stock"),
                html.H5(id="stock-currency")
            ],
            className="row-div"
        )
    ],
)

price_strike = html.Div(
    [
        html.H5("Strike Price"),
        dcc.Input(
                value=75, 
                className="input-box",
                id="strike",
                type="number",
                debounce=True
        ),
    ],
)

div_maturity = html.Div(
        [
            html.H5("Days until maturity"),
            dcc.Input(
                value=1, 
                min=1,
                id="maturity_days", 
                type="number",
                className="input-box",
                debounce=True
            ),
        ]
    ) 

div_amer_euro = html.Div(
        dbc.RadioItems(
        options=[
                {"label":"American", "value": 1},
                {"label":"European", "value": 0}
            ],
            id="american",
            value=0,
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
        ),
        className="radio-group",
)

div_call_put = html.Div(
    dbc.RadioItems(
    options=[
            {"label":"Call", "value": 0},
            {"label":"Put", "value": 1}
        ],
        id="option",
        value=0,
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-primary",
        labelCheckedClassName="active",
    ),
    className="radio-group",
)

div_days = html.Div(  
    [
        html.H5("Days", className="header-days"),
        dbc.RadioItems(
        options=[
                {"label":"Calendar", "value": 365},
                {"label":"Trading", "value": 252}
            ],
            id="days_in_year",
            value=252,
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
        )
    ],
    className="radio-group",
)

div_option = html.Div(

    [
        html.Div(id="option-price"),
        dcc.Dropdown(
            currencies,
            value="USD",
            className="currency-dropdown", 
            id="currency",
            clearable=False,
        ),
    ],
    className="row-div"
)

div_calcs = html.Div(
    [
        html.Tr(
            [
                html.Td("Option Price"),
                html.Td(id="option-price"),
                html.Td(
                    dcc.Dropdown(
                        currencies,
                        value="USD",
                        className="currency-dropdown", 
                        id="currency",
                        clearable=False,
                    ),
                )
            ]
        ),
        html.Tr(
            [
                html.Td("Annual Return"),
                html.Td(id="mu")
            ]
        ),
        html.H3("Greeks", className="greeks-h3"),
        html.Tr(
            [
                html.Td("Delta"),
                html.Td(id="delta")
            ]
        ),
        html.Tr(
            [
                html.Td("Gamma"),
                html.Td(id="gamma")
            ]
        ),
        html.Tr(
            [
                html.Td("Vega"),
                html.Td(id="vega")
            ]
        ),
        html.Tr(
            [
                html.Td("Theta"),
                html.Td(id="theta")
            ]
        ),
        html.Tr(
            [
                html.Td("Rho"),
                html.Td(id="rho")
            ]
        ),
    ]
)


div_vol_annual = html.Div(
    [
        html.H5("Annual"),
        html.H5(id="sigma-annual")
    ],
    className="row-div"
)

div_vol_implied = html.Div(
    [
        html.Div(
            [
                html.H5("Implied"),
                html.H5(id="sigma-implied")
            ],
            className="row-div"
        ),
        html.Div(
            html.Div(     
                dcc.Input(
                    id="sigma-implied-input", 
                    className="input-box",
                    type="number",
                    placeholder="Option $",
                    debounce = True,
                )
            )
        )
    ]
)

div_vol_days = html.Div(
    [
        html.Div(
            [
                html.H5("Daily "),
                html.H5(id="sigma-daily")
            ],
            className="row-div"
        ),
        html.Div(
            [
                dcc.Input(
                    className="input-box",
                    id="vol-days-input",
                    type="number",
                    min=0,
                    value=100,
                    debounce = True,
                    placeholder="Days",
                )
            ]
        )
    ]
)
