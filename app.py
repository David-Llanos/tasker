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
    )
    last_page_button = html.Button('Last Page', id={'type': 'dynamic-last-page-button', 'index': file}, n_clicks=0)
    add_button = html.Button('Add Row', id={'type': 'dynamic-add-button', 'index': file})
    save_button = html.Button('Save', id={'type': 'dynamic-save-button', 'index': file})
    children.extend([html.H2(file), table, last_page_button, add_button, save_button, html.Hr()])



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
