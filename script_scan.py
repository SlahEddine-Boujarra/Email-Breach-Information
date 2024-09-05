import os
import json
import requests
import openpyxl
import pandas as pd
from time import sleep
from datetime import datetime

# Load email addresses from Excel file
file_path = r"C:\Users\Player\Desktop\haveibeenpwned\version_f\emails_check.xlsx"
workbook = openpyxl.load_workbook(file_path)
sheet = workbook.active
emails = [cell.value for cell in sheet['A'][1:] if cell.value is not None]

# Base URL and headers for the API
base_url = 'https://breachdirectory.p.rapidapi.com/'
headers = {
    'x-rapidapi-host': 'breachdirectory.p.rapidapi.com',
    'x-rapidapi-key': 'a6d40b3a17mshda5a0723a9ad3f3p151c1cjsnda4c5dd83768'  # Replace with your actual API key
}

# Function to get breach information for an email
def get_breach_info(email):
    url = f'{base_url}?func=auto&term={email}'
    response = requests.get(url, headers=headers)
    sleep(1)  # Sleep to avoid hitting rate limits
    if response.status_code == 200:
        return response.json()
    return {}

# Function to scan emails and get full breach info
def scan_emails(email_list):
    breach_data = []
    for email in email_list:
        breach_info = get_breach_info(email)
        
        # Extract the "found" status and handle cases where it's missing
        found_status = breach_info.get('found', 'Not Available')

        # Simplify or convert complex data to strings for DataTable
        breach_info_str = json.dumps(breach_info, indent=2)  # Convert to formatted JSON string

        breach_record = {
            "Email": email,
            "Scan Date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "Found": found_status,  # Add the "found" status
            "Breach Info": breach_info_str  # Add the breach info as a JSON string
        }
        breach_data.append(breach_record)
    return breach_data

# Function to save breach data to a JSON file
def save_breach_data_to_json(breach_data):
    output_file = 'output1.json'
    output_path = os.path.join(os.path.dirname(__file__), output_file)
    with open(output_path, 'w') as json_file:
        json.dump(breach_data, json_file, indent=2)
    print(f"Breach data saved to {output_file}")

# Update the data
updated_data = scan_emails(emails)
save_breach_data_to_json(updated_data)
