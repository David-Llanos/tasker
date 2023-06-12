# NOTE: Maybe add row should create a new datatable to update the project
# this way we can combine adding rows and filtering capabilities.
# This way we could also separate updates on tables and JIRA


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

color_palettes = {
    'Contrasting': [
        "#FF0000", # Red
        "#00FF00", # Green
        "#0000FF", # Blue
    ],
    'Pastel': [
        "#FFB3BA", # Light Red
        "#FFDFBA", # Light Orange
        "#FFFFBA", # Light Yellow
    ],
    'Dark': [
        "#8B0000", # Dark Red
        "#006400", # Dark Green
        "#00008B", # Dark Blue
    ],
    'Vivid': [
        "#FF4500", # OrangeRed
        "#7FFF00", # Chartreuse
        "#00BFFF", # DeepSkyBlue
    ],
    'Light': [
        "#ADD8E6", # Light Blue
        "#90EE90", # Light Green
        "#FFB6C1", # Light Pink
    ],
    'David': [
        "#C0C0C0", # Silver
        "#FF6347", # Tomato
        "#ADFF2F", # GreenYellow
    ]
}




color_indices = {}



# Define a function to get the list of files
def get_files():
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    return csv_files



def refresh(files, palette):
    colors = color_palettes[palette]
    color_counter = 0
    children = []
    for i, file in enumerate(files):
        df = pd.read_csv(os.path.join(directory, file))

  
        if 'jira' in df.columns:
            jira_issues = df['jira'].dropna().unique()
            jira_issues_options = [{'label': i, 'value': i} for i in jira_issues]

            # [
            #         {'label': i, 'value': i}
            #         for i in df['A'].unique()
            #     ]    

            data_for_second_table = {c: [''] for c in df.columns}
            # If jira_issues_options is not empty, use the first option as the default value for the 'jira' column
            if jira_issues_options:
                data_for_second_table = {c: '' for c in df.columns}

            second_table = dash_table.DataTable(
                id={'type': 'dynamic-second-table', 'index': file},
                columns=[{"name": c, "id": c} for c in df.columns],
                data=[data_for_second_table],
                editable=True,
                dropdown={
                    'jira': {
                        'options': jira_issues_options,
                        # 'value':  jira_issues_options[0]                       
                    }
                },
                style_header={'backgroundColor': colors[color_counter]},  # Use colors from selected palette
                style_cell={
                    'width': '{}%'.format(len(df.columns)),
                    'textOverflow': 'ellipsis',
                    'overflow': 'hidden'
                }
            )
        else:
            second_table = dash_table.DataTable(
                id={'type': 'dynamic-second-table', 'index': file},
                columns=[{"name": c, "id": c} for c in df.columns],
                data=[{c: '' for c in df.columns}],
                editable=True,
                style_header={'backgroundColor': colors[color_counter]},  # Use colors from selected palette
                style_cell={
                    'width': '{}%'.format(len(df.columns)),
                    'textOverflow': 'ellipsis',
                    'overflow': 'hidden'
                }
            )


        table = dash_table.DataTable(
            id={'type': 'dynamic-table', 'index': file}, 
            columns=[{"name": c, "id": c} for c in df.columns],
            data=df.to_dict('records'),
            page_size=5,
            page_current= 0, 
            editable=True,
            filter_action="native",
            style_header={'backgroundColor': colors[color_counter]},  # Use colors from selected palette
            style_cell={
            'width': '{}%'.format(100./len(df.columns)),
            'textOverflow': 'ellipsis',
            'overflow': 'hidden'}
            )


        last_page_button = html.Button('last page', 
                                    id={'type': 'dynamic-last-page-button', 'index': file}, 
                                    style={'backgroundColor': colors[color_counter]})  # Use colors from selected palette
        add_button = html.Button('add row', 
                                id={'type': 'dynamic-add-button', 'index': file}, 
                                style={'backgroundColor': colors[color_counter]})  # Use colors from selected palette
        save_button = html.Button('Save :)', 
                                id={'type': 'dynamic-save-button', 'index': file}, 
                                style={'backgroundColor': colors[color_counter]})  # Use colors from selected palette
        update_button = html.Button('Update JIRA', 
                                id={'type': 'dynamic-update-button', 'index': file}, 
                                style={'backgroundColor': colors[color_counter]})  # Use colors from selected palette

        clear_filter_button = html.Button('clear all filters', 
                                  id={'type': 'dynamic-clear-filter-button', 'index': file}, 
                                  style={'backgroundColor': colors[color_counter]})  # Apply color from selected palette

   

        color_indices[file] = color_counter
        children.extend([
            html.H2(file), 
            table, 
            clear_filter_button, 
            last_page_button, 
            add_button, 
            save_button, 
            html.Hr(), 
            second_table,
            update_button,
            html.Hr(), 

        ])
        

        color_counter = (color_counter + 1) % len(colors)

    return children

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H1("tasker",style={'text-align':'center', 'color':'darkblue', 'font-style': 'italic'}),
            html.Br(),
            html.H2("select files"),

            dcc.Dropdown(
                id='file-dropdown',
                options=[{'label': i, 'value': i} for i in get_files()],
                value=[get_files()[0]],
                persistence=True,
                persistence_type='local', 
                multi=True
            ),
            html.Br(),
            html.H2("select color palette"),
            dcc.Dropdown(
                id='palette-dropdown',
                options=[{'label': i, 'value': i} for i in color_palettes.keys()],
                value='Pastel',
                persistence=True,
                persistence_type='local' 
            ),
            html.Br(),

            dbc.Button('refresh', id='refresh-button', color='primary')

        ], width=2),
        dbc.Col([
            html.Div(id='tables-container')
        ], width=10)
    ])
])


CALLBACKS=[]

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
    return 'Save :)'

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

#CLEAR FILTERS
@app.callback(
    Output({'type': 'dynamic-table', 'index': MATCH}, 'filter_query'),
    Input({'type': 'dynamic-clear-filter-button', 'index': MATCH}, 'n_clicks'),
)
def clear_filter(n_clicks):
    if n_clicks is not None:
        return ''  # Reset the filter_query property to an empty string
    return dash.no_update  # If the button was not clicked, don't update the filter_query


#UPDATE CLEAR FILTER BUTTON
@app.callback(
    Output({'type': 'dynamic-clear-filter-button', 'index': MATCH}, 'style'),
    Input('palette-dropdown', 'value'),
    State({'type': 'dynamic-clear-filter-button', 'index': MATCH}, 'id'),
    prevent_initial_call=True  # prevent callback from being fired on initial call
)
def update_clear_filter_button_color(selected_palette, button_id):
    color_list = color_palettes[selected_palette]
    color_index = color_indices.get(button_id['index'], 0)  # get color_index from the dictionary
    return {'backgroundColor': color_list[color_index]}

if __name__ == '__main__':
    app.run_server(debug=True)
