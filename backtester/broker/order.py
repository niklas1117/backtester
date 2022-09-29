from typing import Protocol

class Action:
    def __init__(self):
    # buy or sell 
    # buy to close 
    # sell to close 
      pass

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

# class OrderState:
#     # submitted 
#     # accepted 
#     # partially filled
#     # canceled 
#     #
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
        if action == 'BUY':
            if  limit > bar.high:
                ret = bar.open
            elif limit >= bar.low:
                if limit > bar.open:
                    ret = bar.open
                else:
                    ret = limit
        elif action == 'SELL':
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

    def __init__(self, limit, instrument, quantity, broker):
        self.instrument = instrument
        self.volume = quantity #sell if negative
        self.action = 'BUY' if quantity > 0 else 'SELL'
        self.broker = broker
        self.limit = limit
        self.state = 'initialise'
        self.execution = Execution(broker)

    def evaluate(self, bars):
        bar = bars[self.instrument]
        fill = self.execution.evaluate_limit(self.limit, self.volume, 
            self.action, bar)
        return fill 


    def get_remaining(self):
        return self.volume

    

    def execute(self):
        return True

    def __repr__(self):
        return f'Limit Order ({self.volume} of {self.instrument} at {self.limit}'




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

