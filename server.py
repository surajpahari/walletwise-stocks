from flask import Flask, jsonify, request,Response
from actions.getInsights import extractInsights
from actions.getStockChart import getChartData, getLastStat
import actions.getForecastData 
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"



# Get the insights from the stock id (may use sockets later)
@app.route('/get-stock-insights', methods=['GET'])
def getStockInsights():
    stockName = request.args.get('name')
    print(stockName)
    if stockName:
        return extractInsights(stockName)
    else:
        return jsonify(message="invalid-stock")



# Get the current price of the stock
@app.route('/get-stock-chart', methods=['GET'])
def getStockChart():
    stockId = request.args.get('id')
    stockName = request.args.get('name')
    if stockId and stockName:
        print(f"Current working directory: {os.getcwd()}")
        response = getChartData(stockId, stockName)
        if response == 'File does not exist':
            return jsonify(message="File does not exist")
        else:
            return Response(response, mimetype='application/json')
    else:
        return jsonify(message="invalid-stock")


# Get the data for the last
@app.route('/get-current-data', methods=['GET'])
def getCurrentData():
    stockId = request.args.get('id')
    stockName = request.args.get('name')
    if stockId and stockName:
        response = getLastStat(stockId, stockName)
        if response == 'File does not exist':
            return jsonify(message="File does not exist")
        else:
            return Response(response, mimetype='application/json')
    else:
        return jsonify(message="invalid-stock")


#get the forecast data
@app.route('/get-forecast-data', methods=['GET'])
def getForecastData():
    stockId = request.args.get('id')
    stockName = request.args.get('name')
    if stockId and stockName:
        try:
            response = actions.getForecastData.getForeCastData(stockName, stockId)
            return Response(response, mimetype='application/json')
        except ValueError as e:
            return jsonify(error=str(e)), 404
        except Exception as e:
            # logging.error(f"Failed to get forecast data: {e}")
            return jsonify(error="Failed to get file"), 500
    else:
        return jsonify(message="invalid-stock"), 400

# Get the insights from the stock id (may use sockets later)
@app.route('/get-stock-lstm', methods=['GET'])
def getStockLstm():
    stockName = request.args.get('name')
    stockId = request.args.get('id')
    if stockName:
        return (actions.getForecastData.getLstm(stockId,stockName))
    else:
        return jsonify(message="invalid-stock")


if __name__ == '__main__':
    app.run(debug=True)


