from flask import Flask
from flask import jsonify
from flask import request
import json
import flask

from backend.logic import stock_trades
from backend.connectors import sql

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    """Hello World with an optional GET param "name"."""
    name = request.args.get('name', '')
    return jsonify({'success':'hello'})


@app.route('/save_trade', methods=['POST'])
def save_trade():
    return flaskify(stock_trades.save_stock_trade(request.get_json()))


@app.route('/get_stock_details/<stock_name>')
def get_stock_details(stock_name):
    return flaskify(stock_trades.get_stock_details(stock_name))


@app.route('/calculate_dividend/<stock_name>/<price>')
def calculate_dividend(stock_name, price):
    """
    Calculating divident ratio based on given stock and price.

    :param stock: Trade stock for which we need to calculate ratio.
    :param price: stock price.

    :return: divident ratio.
    """
    return flaskify(stock_trades.calculate_dividend(stock_name, price))


@app.route('/calculate_pe_ratio/<stock_name>/<price>')
def calculate_pe_ratio(stock_name, price):
    """
    Calculating P/E ratio based on given stock and price.

    :param stock: Trade stock for which we need to calculate ratio.
    :param price: stock price.

    :return: P/E ratio.
    """
    return flaskify(stock_trades.calculate_pe_ratio(stock_name, price))


@app.route('/calculate_volume_weighted/<stock_name>')
def calculate_volume_weighted(stock_name):
    """
    Calculating Volume Weighted Stock Price based on trades on last 5 minutes.
    :param stock: Trade stock for which we need to calculate ratio.
    :return: Volume Weighted Stock Price.
    """
    pass


@app.route('/calculate_share_index')
def calculate_share_index():
    """
    Calculating GBCE All Share Index using the geometric mean of the Volume
    Weighted Stock Price for all stocks.
    :return: GBCE All Share Index.
    """
    pass


@app.route('/create_tables')
def create_tables():
    return jsonify(stock_trades.create_tables())


@app.route('/drop_tables')
def drop_tables():
    return jsonify(stock_trades.drop_tables())


def flaskify(response,):
    status_code = response.status
    data = response.errors or response.message

    mimetype = 'text/plain'
    if isinstance(data, list) or isinstance(data, dict):
        mimetype = 'application/json'
        data = json.dumps(data)

    return flask.Response(response=data, status=status_code, mimetype=mimetype)
