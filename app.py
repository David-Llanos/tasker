import os
import pandas as pd
import dash
from dash import dcc, html, dash_table, Output, Input, State, MATCH
import dash_bootstrap_components as dbc

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
        id={'type': 'dynamic-table', 'index': i},
        columns=[{"name": c, "id": c} for c in df.columns],
        data=df.to_dict('records'),
        editable=True,
    )
    add_button = html.Button('Add Row', id={'type': 'dynamic-add-button', 'index': i})
    save_button = html.Button('Save', id={'type': 'dynamic-save-button', 'index': i})
    children.extend([html.H2(file), table, add_button, save_button, html.Hr()])  # H2 for the file name, Hr for separating the tables

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
    State({'type': 'dynamic-table', 'index': MATCH}, 'data'))
def save_changes(n_clicks, rows):
    filename=''
    if n_clicks is not None:
        df = pd.DataFrame(rows)
        filename=f"{directory}/{n_clicks}.csv"
        df.to_csv(filename, index=False)
        print(f"{filename} saved !")
    return 'Save'

if __name__ == '__main__':
    app.run_server(debug=True)
