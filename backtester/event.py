from datetime import datetime
from backtester.log import log


class Event:
    pass


class MarketEvent(Event):

    def __init__(self, bars):
        self.type = 'MARKET'
        self.bars = bars
        self.log_market()

    def log_market(self):
        try:
            log(f'\n MARKET: {self.bars.datetime}')
        except:
            log(self.bars)


class SignalEvent(Event):

    def __init__(self, instrument, datetime, signal_type, strength=1):
        self.type = 'SIGNAL'
        self.instrument = instrument
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength

    def log_signal(self):
        log(f'SIGNAL: {self.instrument}, {self.signal_type}, {self.strength}')


class OrderEvent(Event):

    def __init__(self, instrument, order_type, quantity, direction, 
            limit):
        self.type = 'ORDER'
        self.instrument = instrument
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction
        self.limit = limit
        self.log_order()

    def log_order(self):
        log(f'SUBMITTED: {self.instrument}, {self.order_type}, {self.quantity}, {self.direction}')


class FillEvent(Event):

    def __init__(self, timeindex, instrument, exchange, quantity, 
            direction, fill_price, commission):
        self.type = 'FILL'
        self.timeindex = timeindex
        self.instrument = instrument
        self.quantity = quantity
        self.direction = direction
        self.fill_price = fill_price
        self.commission = commission

    def log_fill(self):
        log(f'FILL: {self.instrument}, {self.quantity}, {self.direction}, {self.fill_price}, {self.comission}')
