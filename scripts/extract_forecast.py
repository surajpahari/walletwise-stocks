import requests
import logging
import re
import json

# URL to fetch data from
# Headers to mimic a browser request

def fetch_html(symbol):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.nepsealpha.com/stocks/AKPL/info',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    url = f'https://www.nepsealpha.com/ajax/forecast-menu/{symbol}'
    session = requests.Session()
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Ensure we notice bad responses
        return response.json()['html']  # Assuming the response is JSON with the HTML content
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"Symbol {symbol} not found (404)")
        else:
            raise e

def extract_data_from_html(html_content):
    # Use regex to find the 'var data = ...' part
    data_match = re.search(r'var data\s*=\s*(\[\[.*?\]\]);', html_content, re.DOTALL)
    min_rate_match = re.search(r'var minRate\s*=\s*(\d+);', html_content)
    max_rate_match = re.search(r'var maxRate\s*=\s*(\d+);', html_content)
    
    if data_match and min_rate_match and max_rate_match:
        data_str = data_match.group(1)
        data = json.loads(data_str)
        volume = [entry[0] for entry in data]
        ltp = [entry[1] for entry in data]
        min_rate = int(min_rate_match.group(1))
        max_rate = int(max_rate_match.group(1))
        return {
            'Volume': volume,
            'LTP': ltp,
            'min-rate': min_rate,
            'max-rate': max_rate
        }
    else:
        raise ValueError("No 'var data' or 'minRate' or 'maxRate' declaration found in the HTML content")

def extract_forecast_data(symbol):
    try:
        html_content = fetch_html(symbol)
        extracted_data = extract_data_from_html(html_content)
        return json.dumps(extracted_data, indent=4)
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except ValueError as e:
        logging.error(f"Value error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

