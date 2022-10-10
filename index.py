import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc 

from monitor import MONITOR
from agenda import AGENDA
from updates import UPDATES
from reports import REPORTS
from mysetup import MYSETUP

from dash import dash_table
import pandas as pd
import numpy as np
import plotly.express as px
from dash import dash_table as dt
#from dash.dash_table.Format import Group
from datetime import datetime
import getpass
import json

import sys


xternal_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

app.config.suppress_callback_exceptions=True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])



@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def render_content(pathname):
    if  pathname == '/agenda':
        return AGENDA()
    elif  pathname == '/updates':
        return UPDATES()    
    elif  pathname == '/reports':
        return REPORTS()
    elif pathname == '/mysetup':
        return MYSETUP()
    else:
        return MONITOR()

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
    