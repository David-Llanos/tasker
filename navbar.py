import dash_bootstrap_components as dbc 
from dash import dcc

navbar_style= {
'postion':'fixed',
'top':0,
'left':0,
'right':0,
'margin-left':'1rem',
'margin-right':'1rem',
'font-size': '24px',
'background-color':'gray',
'color':'white'
}

def Navbar():
    navbar = dbc.Nav(children=[

               dbc.NavItem(dcc.Link('Monitor', href='/monitor',
               style={'color':'white', 'font-size': '16px'}
               )),
               dbc.NavItem(dcc.Link('Agenda', href='/agenda',
               style={'color':'white', 'font-size': '16px'}
               )),
               dbc.NavItem(dcc.Link('Updates', href='/updates',
               style={'color':'white', 'font-size': '16px'}
               )),
            
               dbc.NavItem(dcc.Link('Setup', href='/mysetup',
               style={'color':'white', 'font-size': '16px'}
               )),
               dbc.NavItem(dcc.Link('Report', href='/reports',
               style={'color':'white', 'font-size': '16px'}
               )),
    
    ],
    pills=True,
    #card=True,
    #justified=False,
    fill=True,
    #sticky='top',
    #fixed='top',
    horizontal=True,
    style=navbar_style
    )
    return navbar