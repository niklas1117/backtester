from typing import Protocol 

## broker obides the observer protocol and should implement everything that a 
## broker might do -> should be closesly connected to orders 

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


# brokers have methods that allow to place orders
# orders are connected to a broker 

class Broker:

    #gets notified when a new tick happens

    def __init__(self, starting_balance=10_000):

        self.cash = starting_balance
        self.equity = self.cash
        self.pos_value = 0

        self.positions = {}
        self.orders = {} 

        self.order_id = 0

        # order_id and object, when tick check if order can be 
        # submitted and if they are done, delte them 
        pass

    def update(self, bars=None,eof=None):
        if bars is not None:
            self.on_bars(bars)
        if eof is not None:
            self.on_eof()

    def on_bars(self, bars):
        self.evaluate_orders(bars)
        self.update_equity(bars)
        print(f'\nDATE: {bars.datetime}')
        self.log_equity()

    def submit_order(self, order:Order):

        #initialise the order when inputting into this method
        self.orders[self.order_id] = order
        self.order_id += 1
        print(f'SUBMITTED: {order}')
        #>>>>>log

        ## when submitting an order, a closing order can also be submitted
        # that can be attached to the position
        pass
    
    def evaluate_orders(self, bars):
        ids = []
        for id, order in self.orders.items():
            fill = order.evaluate(bars)
            if fill is not None:
                assert self.cash - fill[0]*fill[1] > 0, "Cash can't be negative"
                self.cash -= fill[0]*fill[1]
                self.create_position(fill, order.instrument)
                ids.append(id)
        for id in ids:
            del self.orders[id] ## instead of deleting just change the order state
                

    def create_position(self, fill, instrument):
        print(f'FILLED: {fill[1]} {instrument} at {fill[0]}')
        if instrument not in self.positions.keys():
            self.positions[instrument] = Position(fill, instrument)
        else:
            self.positions[instrument].add(fill)

    def update_equity(self, bars):
        self.pos_value = sum([i.get_value(bars) for i in self.positions.values()])

        self.equity = self.cash + self.pos_value

    def log_equity(self):
        print(f'EQUITY: {round(self.equity, 2)}')
        print(f'CASH: {round(self.cash, 2)}')
        print(f'POSITIONS: {round(self.pos_value, 2)}')


    def check_order(self):
        pass

    def on_eof(self):
        pass

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

