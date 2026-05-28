from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash
import dash_bootstrap_components as dbc

from layout import layout
from callbacks import register_callbacks

from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = layout

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)