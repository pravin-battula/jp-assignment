
from backend.model import stock_trades
from backend.response import response

def save_stock_trade(args_data):
    stock_name = args_data.get('stock_name')
    trade_price = args_data.get('price')
    trade_quantity = args_data.get('quantity')
    trade_type = args_data.get('trade_type')
    last_dividend = args_data.get('last_dividend')

    return stock_trades.save_stock_trade(stock_name, trade_price, trade_quantity, trade_type, last_dividend)

def get_stock_details(stock_name):
    #import pdb; pdb.set_trace()
    stock = stock_trades.get_stock_details(stock_name)
    if stock:
        return response.Response(message=stock)
    return stock


def calculate_dividend(stock_name, price):
    return stock_trades.calculate_dividend(stock_name, price)


def calculate_pe_ratio(stock_name, price):
    return stock_trades.calculate_pe_ratio(stock_name, price)


def create_tables():
    return stock_trades.create_tables()


def drop_tables():
    return stock_trades.drop_tables()