from typing import Protocol 
from backtester.log import log
# from backtester.broker import Position # position has to be changed 
                       # (broker does not want to know about pos)
from backtester.event import FillEvent, OrderEvent
from abc import ABC, abstractmethod

class Execution:
    
    def __init__(self, broker):
        self.broker = broker 
        self.volume_limit = 0.2

    def evaluate_price(self, limit:float, action:str, bar):
        ret = None
        if action in ['BUY', 'BUY_CLOSE']:
            if  limit > bar.high:
                ret = bar.open
            elif limit >= bar.low:
                if limit > bar.open:
                    ret = bar.open
                else:
                    ret = limit
        elif action in ['SELL', 'SELL_CLOSE']:
            if limit < bar.low:
                ret = bar.open
            elif limit <= bar.high:
                if limit < bar.open:
                    ret = bar.open
                else:
                    ret = limit
        else: assert(False)
        return ret
    
    def evaluate_volume(self, volume, bar):
        max_volume = self.volume_limit * bar.volume
        volume_filled =  min(max_volume, volume)
        return volume_filled 

    def evaluate_limit(self, limit, volume ,action, bar):
        fill_price = self.evaluate_price(limit, action, bar)
        fill_volume = self.evaluate_volume(volume, bar)
        if fill_price is not None:
            return (fill_price, fill_volume)
        else:
            return None


class Comission():

    def __init__(self, relative, minimum):
        self.relative = relative 
        self.minimum = minimum 
    
    def calculate(self, price, quantity) -> float:
        return max(self.relative*price*quantity, self.minimum)


class ExecutionHandler(ABC):

    @abstractmethod
    def submit_order(self):
        ...
    
    @abstractmethod
    def execute_orders(self):
        ...
    

class BacktestExecutionHandler(ExecutionHandler):

    fill_dir = {
        'BUY':1,
        'SELL':-1
    }

    def __init__(self, events=None, feed=None):
        self.events = events
        self.feed = feed
        self.execution = Execution(self)
        self.comission = Comission(0.0005, 3)
        self.orders = []

    def submit_order(self, order):
        self.orders.append(order)
        # maybe log here instead of inside order event

    def execute_orders(self, event):
        bars = self.feed.get_current_bars()
        for order in self.orders:
            bar = bars[order.instrument]
            fill = self.execution.evaluate_limit(order.limit, order.quantity, 
                order.direction, bar) # if order executed fill has info
            if fill is not None:
                comission = self.comission.calculate(fill[0], fill[1])
                fill_event = FillEvent(bar.datetime, order.instrument, None,
                    fill[1], order.direction, fill[0], comission)
                dir = self.fill_dir[order.direction]
                order.quantity += dir*fill[1]
                self.events.put(fill_event)
            if order.quantity == 0:
                del order
