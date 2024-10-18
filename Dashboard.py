import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from pymongo import MongoClient
import pandas as pd

# Initialize MongoDB connection
def init_mongo():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['breachDatabase']
    return db['breachResults']

collection = init_mongo()

# Function to fetch all data from MongoDB
def fetch_breach_data():
    cursor = collection.find()
    data = list(cursor)
    return data

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Breach Data Dashboard", style={'textAlign': 'center', 'color': '#007bff'}),

    html.Div([
        html.Button('Load Data', id='load-data-btn', n_clicks=0, style={'padding': '15px', 'borderRadius': '5px', 'backgroundColor': '#28a745', 'color': 'white', 'border': 'none', 'display': 'block', 'margin': '20px auto'}),
    ], style={'textAlign': 'center'}),

    html.Div(id='breach-table-container', style={'padding': '20px'})
])

# Callback to load data from MongoDB and display it in a table
@app.callback(
    Output('breach-table-container', 'children'),
    Input('load-data-btn', 'n_clicks')
)
def load_data(n_clicks):
    if n_clicks > 0:
        # Fetch data from MongoDB
        breach_data = fetch_breach_data()
        
        # Convert MongoDB data to a Pandas DataFrame for displaying in a table
        df = pd.DataFrame(breach_data)
        
        # Convert ObjectId to string for proper display in the table
        if '_id' in df.columns:
            df['_id'] = df['_id'].astype(str)

        # Create Dash DataTable to display the data
        table = dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict('records'),
            filter_action="native",  # Enables filtering
            sort_action="native",    # Enables sorting
            style_table={'overflowX': 'auto', 'minWidth': '100%'},
            style_cell={'textAlign': 'left', 'padding': '10px', 'border': '1px solid #dee2e6', 'whiteSpace': 'normal', 'height': 'auto'},
            style_header={
                'backgroundColor': '#003366',  # Darker blue for headers
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'fontSize': '14px'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f9f9f9'
                }
            ],
            style_data={
                'fontSize': '14px',
                'color': 'black'
            }
        )
        
        return html.Div([table], style={'padding': '20px'})
    return html.Div("Click the 'Load Data' button to display breach data.", style={'textAlign': 'center', 'color': 'red'})

if __name__ == '__main__':
    app.run_server(debug=True)
