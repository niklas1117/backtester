
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



class LimitOrder:
    """has to become an observer that listens to ticks and sends info to broker"""

    def __init__(self, limit, instrument, action, quantity, broker):#, ??open_id=None):

        self.limit = limit        
        self.instrument = instrument
        self.action = action #'BUY' if quantity > 0 else 'SELL'
        assert quantity != 0 
        if self.action in ['BUY', 'BUY_CLOSE']:
            self.quantity = quantity
        elif self.action in ['SELL', 'SELL_CLOSE']:
            self.quantity = - quantity
        self.volume_left = quantity
        self.broker = broker
        self.state = 'SUBMITTED'
        self.execution = Execution(broker)


    def evaluate(self, bars):
        bar = bars[self.instrument]
        fill = self.execution.evaluate_limit(self.limit, self.volume_left, 
            self.action, bar)
        if fill is not None:
            self.volume_left -= fill[1]
        if self.volume_left == 0:
            self.state = 'FILLED'
        return fill

    def get_remaining(self):
        return self.volume_left

    def execute(self):
        return True

    def __repr__(self):
        return f"""Limit Order({self.volume_left} of {self.instrument} at {self.limit})"""

class Slippage():
    """avoid it by using limit orders"""    
    def __init__(self,):
        ...

    def calculate(self) -> float:
        ...

class Tax():
    """capital gains tax, only applicable to close orders"""
    def __init__(self):
        self.rate = 0.2

    def calculate(self, gain) -> float:
        return gain * self.rate

# capital gains algorithm -> check amount sell, go to first order of that 
#   instrument and tax these orders until theyve all been taxed or until 
#   there are not enough sell orders to be taxed 

    # def add_order(self, order):
    #     # maybe add another order to this order to close it
    #     pass

        # change status maybe??

    # create an order execute object that returns a position

    # submitting two orders at once that connects them? open and close position

    # broker checks the order and decides to go into a position

# slippage depends on the order
# comission depends on the broker 
# tax is constant



# orders go to the portfolio class and get executed here
# this is just for order execution
# positoins are created in portfolio