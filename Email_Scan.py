import os
import json
import base64
import pandas as pd
import dash
from dash import dcc, html, dash_table, Input, Output, State
from pymongo import MongoClient
import requests
from time import sleep
from datetime import datetime

# Initialize MongoDB connection
def init_mongo():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['breachDatabase']
    return db['breachResults']

collection = init_mongo()

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Email Breach Information Dashboard", style={'textAlign': 'center', 'color': '#007bff'}),

    # API Key Input
    html.Div([
        html.Label("API Key:", style={'fontSize': '16px', 'fontWeight': 'bold'}),
        dcc.Input(id="api-key", type="text", placeholder="Enter your API Key", style={'width': '60%', 'padding': '10px', 'borderRadius': '5px'}),
        html.Button('Save API Key', id='save-key-btn', n_clicks=0, style={'marginLeft': '10px', 'padding': '10px', 'borderRadius': '5px', 'backgroundColor': '#007bff', 'color': 'white', 'border': 'none'}),
        html.Div(id='save-key-confirmation', style={'marginTop': '10px', 'textAlign': 'center'})
    ], style={'padding': '20px', 'textAlign': 'center'}),

    # File Upload Section
    html.Div([
        html.Label("Upload Email List (Excel or CSV):", style={'fontSize': '16px', 'fontWeight': 'bold'}),
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
            style={
                'width': '60%', 'height': '80px', 'lineHeight': '80px', 'borderWidth': '2px',
                'borderStyle': 'dashed', 'borderRadius': '10px', 'textAlign': 'center',
                'margin': '0 auto', 'backgroundColor': '#f8f9fa'
            },
            multiple=False
        ),
        html.Div(id='output-file-upload', style={'textAlign': 'center', 'padding': '10px'}),
        html.Div(id='upload-confirmation', style={'marginTop': '10px', 'textAlign': 'center'})
    ], style={'padding': '20px'}),

    # Start Scan Button
    html.Div([
        html.Button('Start Scan', id='start-scan-btn', n_clicks=0, style={'padding': '15px', 'borderRadius': '5px', 'backgroundColor': '#28a745', 'color': 'white', 'border': 'none', 'display': 'block', 'margin': '20px auto'}),
        html.Div(id='scan-confirmation', style={'marginTop': '10px', 'textAlign': 'center'})
    ], style={'textAlign': 'center'}),

    # Table for displaying breach data
    html.Div(id='breach-table-container', children=[], style={'padding': '20px'})
])

# API Headers and URL for breach directory
BASE_URL = 'https://breachdirectory.p.rapidapi.com/'
HEADERS_TEMPLATE = {
    'x-rapidapi-host': 'breachdirectory.p.rapidapi.com',
    'x-rapidapi-key': ''  # Placeholder for API Key
}

# Function to load email addresses from Excel or CSV file
def load_emails(file_path):
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            return []
        # Assume emails are in the first column
        return df.iloc[:, 0].dropna().tolist()
    except Exception as e:
        print(f"Error loading file: {e}")
        return []

# Function to call breach directory API and get breach info for an email
def get_breach_info(email, api_key):
    headers = HEADERS_TEMPLATE.copy()
    headers['x-rapidapi-key'] = api_key
    url = f'{BASE_URL}?func=auto&term={email}'
    try:
        response = requests.get(url, headers=headers)
        sleep(1)  # To avoid hitting API rate limits
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"API request error: {e}")
    return {}

# Function to extract breach sources from API response
def extract_breach_sources(breach_info):
    """ Extract breach sources from the breach info. """
    if 'sources' in breach_info:
        return ", ".join(breach_info['sources'])
    return 'Not Available'

# Function to scan emails and return breach data
def scan_emails(email_list, api_key):
    breach_data = []
    for email in email_list:
        breach_info = get_breach_info(email, api_key)
        found_status = breach_info.get('found', 'Not Available')
        breach_sources = extract_breach_sources(breach_info)  # Extracting the sources
        breach_info_str = json.dumps(breach_info, indent=2)
        
        # Create a breach record with an added "Sources" column
        breach_record = {
            "Email": email,
            "Scan Date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "Found": found_status,
            "Sources": breach_sources,  # New column for sources
            "Breach Info": breach_info_str
        }
        
        # Insert into MongoDB and convert _id to string
        insert_result = collection.insert_one(breach_record)
        breach_record["_id"] = str(insert_result.inserted_id)  # Convert ObjectId to string
        breach_data.append(breach_record)
    return breach_data

# Callback to handle Save API Key button click
@app.callback(
    Output('save-key-confirmation', 'children'),
    Input('save-key-btn', 'n_clicks'),
    State('api-key', 'value')
)
def handle_save_api_key(n_clicks, api_key):
    if n_clicks > 0 and api_key:
        return html.Div("API Key has been saved.", style={'color': 'green'})
    return html.Div("Please enter an API key.", style={'color': 'red'})

# Callback to handle the Start Scan button click
@app.callback(
    Output('scan-confirmation', 'children'),
    Output('breach-table-container', 'children'),
    Input('start-scan-btn', 'n_clicks'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('api-key', 'value')
)
def handle_start_scan(n_clicks, contents, filename, api_key):
    if n_clicks > 0 and contents and api_key:
        try:
            # Parse and decode the uploaded file
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)

            # Save the uploaded file locally
            upload_dir = './uploads/'
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(decoded)

            # Load emails from the saved file and scan them
            emails = load_emails(file_path)
            if not emails:
                return "No emails found in the uploaded file.", html.Div(style={'textAlign': 'center'})

            breach_data = scan_emails(emails, api_key)
            df = pd.DataFrame(breach_data)

            # Display the data in a table with the new "Sources" column
            table = dash_table.DataTable(
                columns=[
                    {"name": "Email", "id": "Email"},
                    {"name": "Scan Date", "id": "Scan Date"},
                    {"name": "Found", "id": "Found"},
                    {"name": "Sources", "id": "Sources"},  # New "Sources" column
                    {"name": "Breach Info", "id": "Breach Info"}
                ],
                data=df.to_dict('records'),
                filter_action="native",  # Enables filtering, similar to the image
                style_table={'overflowX': 'auto', 'minWidth': '100%'},
                style_cell={'textAlign': 'left', 'padding': '10px', 'border': '1px solid #dee2e6', 'whiteSpace': 'normal', 'height': 'auto'},
                style_header={
                    'backgroundColor': '#003366',  # Darker blue for headers like in the image
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
                style_data={'fontSize': '14px', 'color': 'black'}
            )

            return "Scan complete!", html.Div([table], style={'padding': '20px'})

        except Exception as e:
            return f"An error occurred: {e}", html.Div(style={'textAlign': 'center'})
    return "", html.Div("Click the 'Start Scan' button to begin scanning.", style={'textAlign': 'center'})

if __name__ == '__main__':
    app.run_server(debug=True)
