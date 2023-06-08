import os
import pandas as pd
import dash
from dash import dcc, html, dash_table, Output, Input, State, MATCH
import dash_bootstrap_components as dbc
import math

# initialize Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# directory containing the CSV files
directory = '/home/david/Documents/tasker/projects'

# get a list of all CSV files in the directory
# csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
# print(csv_files)

color_palettes = {
    'Palette 1': [
        "#00FF00", # Lime
        "#00FFFF", # Aqua
        "#FF00FF", # Fuchsia
    ],
    'Palette 2': [
        "#008000", # Green
        "#808000", # Olive
        "#800080", # Purple
    ],
    'Palette 3': [
        "#C0C0C0", # Silver
        "#FF6347", # Tomato
        "#ADFF2F", # GreenYellow
    ]
}


color_list = [
    "#00FF00", # Lime
    "#00FFFF", # Aqua
    "#FF00FF", # Fuchsia
    # "#800000", # Maroon
    "#008000", # Green
    "#808000", # Olive
    "#800080", # Purple
    "#008080", # Teal
    "#C0C0C0", # Silver
    "#FF6347", # Tomato
    "#ADFF2F", # GreenYellow
    "#FFD700", # Gold
    "#1E90FF", # DodgerBlue
    "#DDA0DD", # Plum
    "#20B2AA", # LightSeaGreen
    "#FFA07A"  # LightSalmon
]

# Define a function to get the list of files
def get_files():
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    return csv_files








# Define the refresh function
# def refresh(files,palette ):
#     colors = color_palettes[palette]
#     color_counter = 0
#     children = []
#     for i, file in enumerate(files):
#         df = pd.read_csv(os.path.join(directory, file))


#         table = dash_table.DataTable(
#             id={'type': 'dynamic-table', 'index': file}, 
#             columns=[{"name": c, "id": c} for c in df.columns],
#             data=df.to_dict('records'),
#             page_size=5,
#             page_current= 0, 
#             editable=True,
#             filter_action="native" ,
#             style_header={'backgroundColor': color_list[color_counter]}, # Apply color to table
#             )
#         last_page_button = html.Button('Last Page', 
#                                     id={'type': 'dynamic-last-page-button', 'index': file}, 
#                                     style={'backgroundColor': color_list[color_counter]})  # Apply color to button
#         add_button = html.Button('Add Row', 
#                                 id={'type': 'dynamic-add-button', 'index': file}, 
#                                 style={'backgroundColor': color_list[color_counter]})  # Apply color to button
#         save_button = html.Button('Save', 
#                                 id={'type': 'dynamic-save-button', 'index': file}, 
#                                 style={'backgroundColor': color_list[color_counter]})  # Apply color to button
      

#         children.extend([html.H2(file), table, last_page_button, add_button, save_button, html.Hr()])

#         # increment color_counter and use modulo to keep it within the length of color_list
#         color_counter = (color_counter + 1) % len(colors)

#     return children

def refresh(files, palette):
    colors = color_palettes[palette]
    color_counter = 0
    children = []
    for i, file in enumerate(files):
        df = pd.read_csv(os.path.join(directory, file))

        table = dash_table.DataTable(
            id={'type': 'dynamic-table', 'index': file}, 
            columns=[{"name": c, "id": c} for c in df.columns],
            data=df.to_dict('records'),
            page_size=5,
            page_current= 0, 
            editable=True,
            filter_action="native",
            style_header={'backgroundColor': colors[color_counter]},  # Use colors from selected palette
        )
        last_page_button = html.Button('Last Page', 
                                    id={'type': 'dynamic-last-page-button', 'index': file}, 
                                    style={'backgroundColor': colors[color_counter]})  # Use colors from selected palette
        add_button = html.Button('Add Row', 
                                id={'type': 'dynamic-add-button', 'index': file}, 
                                style={'backgroundColor': colors[color_counter]})  # Use colors from selected palette
        save_button = html.Button('Save', 
                                id={'type': 'dynamic-save-button', 'index': file}, 
                                style={'backgroundColor': colors[color_counter]})  # Use colors from selected palette
      

        children.extend([html.H2(file), table, last_page_button, add_button, save_button, html.Hr()])

        # increment color_counter and use modulo to keep it within the length of color_list
        color_counter = (color_counter + 1) % len(colors)

    return children



app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("Select Files"),
            dcc.Dropdown(
                id='file-dropdown',
                options=[{'label': i, 'value': i} for i in get_files()],
                value=[get_files()[0]],
                multi=True
            ),
            html.Br(),
            html.H2("Select Color Palette"),
            dcc.Dropdown(
                id='palette-dropdown',
                options=[{'label': i, 'value': i} for i in color_palettes.keys()],
                value='Palette 1'
            ),
            html.Br(),

            dbc.Button('Refresh', id='refresh-button', color='primary')
        ], width=2),
        dbc.Col([
            html.Div(id='tables-container')
        ], width=10)
    ])
])


# ADD ROW
@app.callback(
    Output({'type': 'dynamic-table', 'index': MATCH}, 'data'),
    Input({'type': 'dynamic-add-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'dynamic-table', 'index': MATCH}, 'data'),
    State({'type': 'dynamic-table', 'index': MATCH}, 'columns'))
def add_row(n_clicks, rows, columns):
    if n_clicks is not None:
        rows.append({c['id']: '' for c in columns})
    return rows

# SAVE CHANGES
@app.callback(
    Output({'type': 'dynamic-save-button', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-save-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'dynamic-table', 'index': MATCH}, 'data'),
    State({'type': 'dynamic-save-button', 'index': MATCH}, 'id'))  # new State to get the file name
def save_changes(n_clicks, rows, button_id):  # added filename argument
    if n_clicks is not None and button_id is not None:
        df = pd.DataFrame(rows)
        file_path = os.path.join(directory, button_id['index'])  # Here use 'index' from id to get the file name
        df.to_csv(file_path, index=False)
        print(f"{file_path} saved !")
    return 'Save'

# GO TO LAST PAGE
@app.callback(
    Output({'type': 'dynamic-table', 'index': MATCH}, 'page_current'),
    Input({'type': 'dynamic-last-page-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'dynamic-table', 'index': MATCH}, 'data'),
    State({'type': 'dynamic-table', 'index': MATCH}, 'page_current'))
def go_to_last_page(n_clicks, rows, current_page):
    if n_clicks is not None:
        page_size = 5
        last_page = math.ceil(len(rows) / page_size) - 1
        return last_page
    return dash.no_update


# HANDLE REFRESH
@app.callback(
    Output('tables-container', 'children'),
    [Input('refresh-button', 'n_clicks'),
     Input('file-dropdown', 'value'),
     Input('palette-dropdown', 'value')]
)
def handle_refresh(n_clicks, files, palette):
    if files:
        return refresh(files, palette)
    else:
        return []


if __name__ == '__main__':
    app.run_server(debug=True)
