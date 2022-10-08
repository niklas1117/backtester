from typing import Protocol 
from backtester.log import log
from . import Position # position has to be changed 
                       # (broker does not want to know about pos)


class Order(Protocol):
    instrument:str
    def evaluate():
        ...

# orders go to the portfolio class and get executed here
# this is just for order execution
# positoins are created in portfolio

class Broker:

    def __init__(self):
        self.equity = self.cash # maybe turn equity into a list 
        self.pos_value = 0
        self.comission = Comission(0.0005, 3)
        self.positions = {}
        self.orders = {} 
        self.order_id = 0

    def update(self, bars=None,eof=None):
        """Gets called by an observable"""
        if bars is not None:
            self.__on_bars(bars)
        if eof is not None:
            self.__on_eof()

    def submit_order(self, order:Order):
        self.orders[self.order_id] = order
        self.order_id += 1
        log(f'SUBMITTED: {order}')

    def get_limit_order_quantity(self, instrument):
        return sum([i.volume_left for i in self.orders.values() 
            if ((i.instrument == instrument) & (i.state =='SUBMITTED'))])

    @property
    def limit_order_value(self):
        return sum([i.volume_left*i.limit for i in self.orders.values() if i.state =='SUBMITTED'])
    
    def __on_bars(self, bars):
        self.__evaluate_orders(bars)
        self.__update_equity(bars)
        self.__log_equity()
        log(f'\nDATE: {bars.datetime}')

    def __on_eof(self):
        # close remaining orders
        pass

    def __evaluate_orders(self, bars):
        for id, order in self.orders.items():
            if order.state != 'FILLED':
                fill = order.evaluate(bars)
                if fill is not None:
                    self.__evaluate_order(fill, order)
                
    def __evaluate_order(self, fill, order:Order):
        """create position if aI have enough cash """
        price = fill[0]
        quantity = fill[1]
        cost = self.__calculate_cost(price, quantity)
        post_cash = self.cash - (price*quantity) -cost
        if post_cash < 0:
            log("Cash can't be negative")
        else:
            self.cash = post_cash
            self.__create_position(fill, order.instrument)

    def __calculate_cost(self, price, quantity):
        comission = self.comission.calculate(price, quantity)
        return comission

    def __create_position(self, fill, instrument):
        log(f'FILLED: {fill[1]} {instrument} at {fill[0]}')
        if instrument not in self.positions.keys():
            self.positions[instrument] = Position(fill, instrument)
        else:
            self.positions[instrument].add(fill)

    def __update_equity(self, bars):
        """maybe make equity a list or a dict"""
        self.pos_value = sum([i.get_value(bars) for i in self.positions.values()])
        self.equity = self.cash + self.pos_value
            
    def __log_equity(self):
        log(f'EQUITY: {round(self.equity, 2)}')
        log(f'CASH: {round(self.cash, 2)}')
        log(f'POSITIONS: {round(self.pos_value, 2)}')


class Comission():

    def __init__(self, relative, minimum):
        self.relative = relative 
        self.minimum = minimum 
    
    def calculate(self, price, quantity) -> float:
        return max(self.relative*price*quantity, self.minimum)