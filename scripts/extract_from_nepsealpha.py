import requests
from bs4 import BeautifulSoup
import os
import json

# URL to fetch data from
url = "https://www.nepsealpha.com/trading-signals/tech?type=ajax"

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.nepsealpha.com/trading-signals/tech',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

tableHeaders = [
    "Company",
    "Signal",
    "Risk",
    "Sector",
    "Daily Gain",
    "LTP",
    "Daily Volatility",
    "PRICE RELATIVE",
    "3M TREND",
    "RSI 14",
    "MACD VS Signal Line",
    "%B",
    "MFI 14",
    "Sto.14",
    "14-day CCI",
    "StochRSI",
    "10SMA",
    "Price > 20SMA",
    "Price > 50SMA",
    "Price > 200SMA",
    "5SMA > 20SMA",
    "SMA 50,200",
    "Volume Trend",
    "3 Month Beta"
]

def tableToJson(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all rows in the table
    table_rows = soup.find_all('tr')
    
    # Initialize an empty list to store JSON objects
    data = []
    
    # Iterate through each row
    for row in table_rows:
        # Initialize an empty dictionary for each row's data
        row_data = {}
        
        # Find all cells in the row
        cells = row.find_all('td')
        
        # Extract data from each cell and add to row_data dictionary
        if cells:
            for idx, header in enumerate(tableHeaders):
                if idx < len(cells):
                    row_data[header] = cells[idx].text.strip()
            data.append(row_data)
    
    return data 

# Check if the response.html file exists
if os.path.exists('response.html'):
    print("File already exists, no fetch.")
    # Read the content from the file
    with open('response.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
else:
    print("File does not exist, fetch.")
    # Send GET request
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        # Save the response content to a file
        with open('response.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        
        html_content = response.text
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        html_content = None

if html_content:
    # Convert HTML content to JSON
    json_data = tableToJson(html_content)
    
    # Write JSON data to a file
    with open("technicals.json", "w", encoding='utf-8') as file:
        json.dump(json_data, file, indent=4)
    
    print("JSON data has been written to technicals.json file.")

