from flask import jsonify
import scripts.extract_forecast;
import json
import os


csvFolder= '../project/scripts/data/csvs'
lstmFolder= '../project/scripts/data/lstms'
def checkCSVFileInLocal(filename):
    # Get the absolute path
    full_path = os.path.abspath(os.path.join(csvFolder, filename))
    print(f"Checking file at: {full_path}")
    return os.path.isfile(full_path), full_path

def checkLSTMfileInLocal(filename):
    # Get the absolute path
    full_path = os.path.abspath(os.path.join(lstmFolder, filename))
    print(f"Checking file at: {full_path}")
    return os.path.isfile(full_path), full_path



def getForeCastData(symbol,id):
    return scripts.extract_forecast.extract_forecast_data(symbol)



def read_json_file(full_filename):
    with open(full_filename, 'r') as file:
        return json.load(file)

def getLstm(stockid, stockName):
    closing_prices = [
        404.32, 153.67, 149.54, 162.20, 148.95,
        160.10, 155.78, 167.32, 152.88, 146.55,
        159.44, 163.12, 157.89, 165.23, 158.33,
        161.47, 154.22, 170.50, 160.80, 168.45,
        152.12, 164.90, 159.00, 167.78, 155.95,
        170.25, 162.60, 160.12, 168.55, 154.75
    ]
    
    # Concatenate the filename
    filename = f"{stockName}_{stockid}.json"
    print(filename)
    full_filename = f"local_directory/{filename}"  # Update with the actual path

    doesExist, full_filename = checkLSTMfileInLocal(filename)
    if doesExist:
        # Return the content of the JSON file
        data = read_json_file(full_filename)
        return jsonify(data)
    else:
        return jsonify([{'lstm':closing_prices}])

       

