from inspect import indentsize
import  dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table as dt
from navbar import Navbar
import pandas as pd



nav = Navbar()

body = dbc.Container([ 

    dbc.Row([
                
                dbc.Col([    
                    html.Br(),
                    html.H5('Updates', style={'text-align':'center','color':'blue'}),

                ],width=12),

        ]),#Row
    ], fluid=True)#Container



def UPDATES():
    layout = html.Div([
        nav,
        body
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

app.layout=UPDATES()
if __name__ == '__main__':
    app.run_server()