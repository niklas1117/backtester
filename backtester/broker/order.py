from typing import Protocol


# class OrderType:
#     # mid price
#     # market 
#     # stop 
#     # stop limit
#     # market if touched 
#     # limit if touched
#     # trail 
#     # trail limit 
#     # relative
#     # market on close 
#     # limit on price

#     ## different algos 
#     pass

class Bar(Protocol):

    open:float
    high:float
    low:float
    close:float
    volume:float

class Execution:
    
    def __init__(self, broker):
        self.broker = broker 
        self.volume_limit = 0.2

    def evaluate_price(self, limit:float, action:str, bar:Bar):
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
    
    def evaluate_volume(self, volume, bar:Bar):
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

class LimitOrder:

    def __init__(self, limit, instrument, action, quantity, broker):#, ??open_id=None):

        self.limit = limit        
        self.instrument = instrument
        self.action = action #'BUY' if quantity > 0 else 'SELL'
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

