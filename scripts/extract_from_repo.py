import argparse
import requests
import os

def download_csv(id, symbol):
    destination_folder = '../project/scripts/data/csvs'
    url = f"https://github.com/Aabishkar2/nepse-data/blob/main/data/company-wise/{symbol}.csv"
    # Adjust the URL to directly access the raw file
    raw_url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
    
    response = requests.get(raw_url)
    csv_file_name = os.path.join(destination_folder, symbol +"_"+id+ ".csv")
    if response.status_code == 200:
        with open(csv_file_name, 'wb') as file:
            file.write(response.content)
        print(f"File '{csv_file_name}' downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download CSV file for a given symbol.")
    parser.add_argument("-sym", "--symbol", required=True, help="Symbol for the company CSV file to download")
    parser.add_argument("-i", "--id", required=True, help="ID for the company CSV file to download")
    args = parser.parse_args()
    download_csv(args.id, args.symbol)

