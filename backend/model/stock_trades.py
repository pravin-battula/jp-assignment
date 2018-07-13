import datetime

from backend.response import response
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import Integer, String
from sqlalchemy import DateTime

from backend.connectors import sql


class StockTrades(sql.base_model):
    """Table definition for stocktrades table."""

    __tablename__ = 'stock_trades'

    stock_name = Column(
        'stock_name', String(200), primary_key=True, nullable=False)
    trade_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    trade_price = Column(Integer, nullable=True)
    trade_quantity = Column(Integer, nullable=True)
    trade_type = Column(String(100), nullable=True)
    last_dividend = Column(Integer, nullable=True)

    def to_dict(self):
        """Return a dictionary of a product_live_time."""
        return {
            'stock_name': self.stock_name,
            'trade_timestamp': str(self.trade_timestamp),
            'trade_price': self.trade_price,
            'trade_quantity': self.trade_quantity,
            'trade_type':self.trade_type,
            'last_dividend':self.last_dividend
        }


@sql.wrap_db_errors
def save_stock_trade(
        stock_name, trade_price, trade_quantity, trade_type, last_dividend):
    trade_data = {
        'stock_name': stock_name,
        'trade_price': trade_price,
        'trade_quantity': trade_quantity,
        'trade_type':trade_type,
        'last_dividend':last_dividend
    }

    stock_data_to_add = StockTrades(**trade_data)
    with sql.db_session() as session:
        session.add(stock_data_to_add)
        timed_release_insert_response = {'trade_data': trade_data}
        return response.Response(message=timed_release_insert_response)


@sql.wrap_db_errors
def get_stock_details(stock_name):
    with sql.db_session() as session:
        stock = session.query(StockTrades).get(stock_name)
        if not stock:
            return response.create_not_found_response("stock {stock_name} not found ".format(stock_name))
        return stock.to_dict()


@sql.wrap_db_errors
def calculate_dividend(stock_name, price, stock_ins=None):
    if not stock_ins:
        stock_ins = get_stock_details(stock_name)
    if stock_ins:
        last_dividend = stock_ins['last_dividend']
        dividend_yield = int(last_dividend)/int(price)
        return response.Response(message={'dividend_yield':dividend_yield})

    return stock_ins

@sql.wrap_db_errors
def calculate_pe_ratio(stock_name, price):
    stock_ins = get_stock_details(stock_name)
    if stock_ins:
        response_msg = calculate_dividend(stock_name, price, stock_ins)
        dividend = int(response_msg.message['dividend_yield'])
        pe_ratio = int(price)/dividend
        return response.Response(message={'pe_ratio':pe_ratio})

    return stock_ins


def create_tables():
    base_model = sql.base_model
    db_engine = sql.db_engine

    base_model.metadata.create_all(db_engine)
    return {'tables_creation':'success'}


def drop_tables():
    base_model = sql.base_model
    db_engine = sql.db_engine

    base_model.metadata.drop_all(db_engine)
    return {'tables_drop':'success'}