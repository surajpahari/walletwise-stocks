import os
import json
import argparse
import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define the directory to save JSON files
json_dir = 'data'

# Create the directory if it doesn't exist
if not os.path.exists(json_dir):
    os.makedirs(json_dir)

# JSON fetching through virtual browser
def fetch_json_from_page(symbol, id):
    base_url = "https://www.nepalstock.com.np/company/detail/"
    url = base_url + id
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-http2"])
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        page = context.new_page()

        # Capture network requests
        json_responses = []

        def handle_response(response):
            # Handling the response
            content_type = response.headers.get('content-type', '')
            # logging.debug(f"Received response: {response.url} with status: {response.status} and content type: {content_type}")

            if 'application/json' in content_type:
                try:
                    json_data = response.json()
                    json_responses.append({
                        'url': response.url,
                        'status': response.status,
                        'json': json_data
                    })

                    # Destructuring the URL
                    destructured = response.url.split('/')
                    final_url = ''
                    # Ensure the URL has enough parts to avoid IndexError
                    if len(destructured) > 2:
                        base_url = destructured[-2]
                        query_parts = destructured[-1].split('?')
                        final_url = base_url + '_' + query_parts[0]
                    else:
                        logging.error(f"Unexpected URL structure: {response.url}")

                    # Construct the file path according to the specified structure

                    # Filtering only security and graphdata responses
                    if destructured[-2] in ['security', 'graphdata']:
                        file_dir = os.path.join(json_dir, symbol + '_' + destructured[-1])
                        if not os.path.exists(file_dir):
                            os.makedirs(file_dir)
                        file_name = os.path.join(file_dir, destructured[-2] + ".json")

                        with open(file_name, 'w') as file:
                            json.dump(json_data, file, indent=4)
                        logging.debug(f"Saved JSON response from {response.url} to {file_name}")

                except Exception as e:
                    logging.error(f"Failed to process response from {response.url}: {e}")

        # Calling handle_response on each response
        page.on("response", handle_response)

        # Setting 3 retries in case it fails to fetch in first attempt
        retries = 3
        for attempt in range(retries):
            try:
                logging.debug(f"Attempt {attempt + 1} to navigate to {url}")
                page.goto(url, wait_until="networkidle")
                # Wait for some time to capture network requests (adjust as necessary)
                page.wait_for_timeout(10000)
                break
            except (PlaywrightTimeoutError, Exception) as e:
                logging.error(f"Error navigating to {url} on attempt {attempt + 1}: {e}")
                if attempt == retries - 1:
                    raise
        browser.close()
        return json_responses

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Fetch JSON from a webpage.')
    parser.add_argument('-sym', '--symbol', type=str, required=True, help='Symbol of the company')
    parser.add_argument('-id', '--id', type=str, required=True, help='ID of the company')
    args = parser.parse_args()

    # Fetch JSON using symbol and id
    fetch_json_from_page(args.symbol, args.id)

