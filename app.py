from dash import Dash
import dash_bootstrap_components as dbc


external_stylesheets = [
    dbc.themes.CYBORG, 
    "assets/styles.css",
    "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap"
]

app = Dash(
        __name__,
        external_stylesheets=external_stylesheets
    )
