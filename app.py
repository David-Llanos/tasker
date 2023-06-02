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
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
print(csv_files)

# create a DataTable, "Add Row" button and "Save" button for each CSV file
color_list = [
    "#00FF00", # Lime
    "#00FFFF", # Aqua
    "#FF00FF", # Fuchsia
    "#800000", # Maroon
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

color_counter = 0
children = []
for i, file in enumerate(csv_files):
    df = pd.read_csv(os.path.join(directory, file))
    table = dash_table.DataTable(
        id={'type': 'dynamic-table', 'index': file}, 
        columns=[{"name": c, "id": c} for c in df.columns],
        data=df.to_dict('records'),
        page_size=2,
        page_current= 0, 
        editable=True,
        filter_action="native" ,
        style_header={'backgroundColor': color_list[color_counter]}, # Apply color to table
    )
    last_page_button = html.Button('Last Page', 
                                   id={'type': 'dynamic-last-page-button', 'index': file}, 
                                   style={'backgroundColor': color_list[color_counter]})  # Apply color to button
    add_button = html.Button('Add Row', 
                             id={'type': 'dynamic-add-button', 'index': file}, 
                             style={'backgroundColor': color_list[color_counter]})  # Apply color to button
    save_button = html.Button('Save', 
                              id={'type': 'dynamic-save-button', 'index': file}, 
                              style={'backgroundColor': color_list[color_counter]})  # Apply color to button
    children.extend([html.H2(file), table, last_page_button, add_button, save_button, html.Hr()])  # Added the last_page_button here

    # Increment the color counter
    color_counter += 1

    # If we've gone through all the colors, reset the counter
    if color_counter == len(color_list):
        color_counter = 0



app.layout = html.Div(children=children)

@app.callback(
    Output({'type': 'dynamic-table', 'index': MATCH}, 'data'),
    Input({'type': 'dynamic-add-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'dynamic-table', 'index': MATCH}, 'data'),
    State({'type': 'dynamic-table', 'index': MATCH}, 'columns'))
def add_row(n_clicks, rows, columns):
    if n_clicks is not None:
        rows.append({c['id']: '' for c in columns})
    return rows


@app.callback(
    Output({'type': 'dynamic-save-button', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-save-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'dynamic-table', 'index': MATCH}, 'data'),
    State({'type': 'dynamic-save-button', 'index': MATCH}, 'index'))  # new State to get the file name
def save_changes(n_clicks, rows, filename):  # added filename argument
    if n_clicks is not None and filename is not None:
        df = pd.DataFrame(rows)
        file_path = os.path.join(directory, filename)
        df.to_csv(file_path, index=False)
        print(f"{file_path} saved !")
    return 'Save'



# The callback for going to last page

@app.callback(
    Output({'type': 'dynamic-table', 'index': MATCH}, 'page_current'),
    Input({'type': 'dynamic-last-page-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'dynamic-table', 'index': MATCH}, 'data'),
    State({'type': 'dynamic-table', 'index': MATCH}, 'page_current'),
    prevent_initial_call=True)
def go_to_last_page(n_clicks, rows, current_page):
    if n_clicks is not None:
        last_page = (len(rows) - 1) // 2  # Updated formula
        return last_page
    return dash.no_update



if __name__ == '__main__':
    app.run_server(debug=True)