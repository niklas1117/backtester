from typing import Protocol 


class Observer(Protocol):
    def update():
        ...


class Subject(Protocol):
    def attach():
        ...
    def detach():
        ...
    def notify():
        ...


class Order(Protocol):
    instrument:str
    def evaluate():
        ...


class Broker:

    def __init__(self, starting_balance=10_000):
        self.cash = starting_balance
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
        print(f'SUBMITTED: {order}')
    
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
        print(f'\nDATE: {bars.datetime}')

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
        print(post_cash, self.cash, (price*quantity) -cost)
        assert  post_cash >= 0, "Cash can't be negative"
        self.cash = post_cash
        self.__create_position(fill, order.instrument)

    def __calculate_cost(self, price, quantity):
        comission = self.comission.calculate(price, quantity)
        return comission

    def __create_position(self, fill, instrument):
        print(f'FILLED: {fill[1]} {instrument} at {fill[0]}') #>>>>>LOG
        if instrument not in self.positions.keys():
            self.positions[instrument] = Position(fill, instrument)
            print(self.positions)
        else:
            self.positions[instrument].add(fill)

    def __update_equity(self, bars):
        """maybe make equity a list or a dict"""
        self.pos_value = sum([i.get_value(bars) for i in self.positions.values()])
        self.equity = self.cash + self.pos_value
            
    def __log_equity(self):
        print(f'EQUITY: {round(self.equity, 2)}')
        print(f'CASH: {round(self.cash, 2)}')
        print(f'POSITIONS: {round(self.pos_value, 2)}')


class Position:

    def __init__(self, fill, instrument):
       
        self.instrument = instrument
        self.price = fill[0]
        self.quantity = fill[1] #sell if negative

    def add(self, fill):
        new_quantity = self.quantity+fill[1]
        self.price = ((self.price*self.quantity)+(fill[0]*fill[1]))/new_quantity
        self.quantity += fill[1]

    def get_value(self, bars):
        bar = bars[self.instrument]
        return bar.close * self.quantity


class Comission():

    def __init__(self, relative, minimum):
        self.relative = relative 
        self.minimum = minimum 
    
    def calculate(self, price, quantity) -> float:
        return max(self.relative*price*quantity, self.minimum)