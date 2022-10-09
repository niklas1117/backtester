from datetime import datetime
from log import log


class Event:
    pass


class MarketEvent(Event):

    def __init__(self):
        self.type = 'MARKET'


class SignalEvent(Event):

    def __init__(self, symbol, datetime, signal_type):
        self.type = 'SIGNAL'
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = self.strength


class OrderEvent(Event):

    def __init__(self, symbol, order_type, quantity, direction):
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def log_order(self):
        log(f"""SUBMITTED: {self.symbol}, {self.type}, {self.quantity}, 
            {self.direction}""")


class FillEvent(Event):

    def __init__(self, timeindex, symbol, exchange, quantity, 
            direction, fill_price, comission):
        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_price = fill_price
        self.comission = comission


# https://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-II/

# create all the events here
# these will be imported to the 
# other classes that then add different events to the queue
# the event handler checks for type and then executes certain 
# methods for its classes