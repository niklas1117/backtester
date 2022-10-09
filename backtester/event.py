from datetime import datetime
from backtester.log import log


class Event:
    pass


class MarketEvent(Event):

    def __init__(self, bars):
        self.type = 'MARKET'
        self.bars = bars

class SignalEvent(Event):

    def __init__(self, instrument, datetime, signal_type, strength):
        self.type = 'SIGNAL'
        self.instrument = instrument
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength


class OrderEvent(Event):

    def __init__(self, instrument, order_type, quantity, direction, 
            limit):
        self.type = 'ORDER'
        self.instrument = instrument
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction
        self.limit = limit

    def log_order(self):
        log(f"""SUBMITTED: {self.instrument}, {self.type}, {self.quantity}, 
            {self.direction}""")


class FillEvent(Event):

    def __init__(self, timeindex, instrument, exchange, quantity, 
            direction, fill_price, comission):
        self.type = 'FILL'
        self.timeindex = timeindex
        self.instrument = instrument
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