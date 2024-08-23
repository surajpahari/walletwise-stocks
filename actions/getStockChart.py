import os
import json
from flask import jsonify
from scripts import extract_from_repo
import pandas as pd

dataFolder = '../project/scripts/data/csvs'

# Check if file exists
def checkFileInLocal(filename):
    # Get the absolute path
    full_path = os.path.abspath(os.path.join(dataFolder, filename))
    print(f"Checking file at: {full_path}")
    return os.path.isfile(full_path), full_path

def getJson(filename, n):
    # Read the CSV file into a pandas DataFrame
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: File '{filename}' is empty.")
        return None

    # Get the last n rows from the DataFrame
    last_n_rows = df.tail(n)
    print(last_n_rows)

    # Convert the last n rows to JSON format
    json_data = last_n_rows.to_json(orient='records')

    return json_data

def getChartData(id, name):
    # Concatenate the filename
    filename = f"{name}_{id}.csv"
    
    # Check if the file exists
    doesExist, full_filename = checkFileInLocal(filename)
    if doesExist:
        return getJson(full_filename, 30)  # Assuming you want the last 60 rows in JSON format
    else:
        extract_from_repo.download_csv(id,name)
        doesExist, full_filename = checkFileInLocal(filename)
        # return(filename)
        if doesExist:
            return getJson(full_filename,30)
        return json.dumps({"message": "nothing here"})

def getLastStat(id, name):
    # Concatenate the filename
    filename = f"{name}_{id}.csv"
    # Check if the file exists
    doesExist, full_filename = checkFileInLocal(filename)
    if doesExist:
        return getJson(full_filename, 1)  # Assuming you want the last 60 rows in JSON format
    else:
        try:
            extract_from_repo.download_csv(id, name)
        except Exception:
            return json.dumps({"message": "nothing here"})
        
        doesExist, full_filename = checkFileInLocal(filename)
        if doesExist:
            return getJson(full_filename, 1)
        return json.dumps({"message": "nothing here"})

