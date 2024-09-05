import dash
from dash import dcc, html, dash_table
import pandas as pd
import json
import os

# Initialize Dash app
app = dash.Dash(__name__)

# Load initial data
def load_data():
    output_file = 'output1.json'
    output_path = os.path.join(os.path.dirname(__file__), output_file)
    if os.path.exists(output_path):
        with open(output_path, 'r') as json_file:
            return json.load(json_file)
    return []

df = pd.DataFrame(load_data())

# Layout of the app
app.layout = html.Div([
    html.H1("Email Breach Information Dashboard"),
    dash_table.DataTable(
        id='breach-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        sort_action='native',
        sort_by=[{"column_id": "Scan Date", "direction": "desc"}],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '10px'},
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
