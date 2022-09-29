# Cost classes 

# Slippage not implemented yet, just do stop orders

class Comission():

    def __init__(self, relative, minimum):
        self.relative = relative 
        self.minimum = minimum 

    def calculate(self, price, quantity) -> float:
        cost = self.relative*price*quantity
        if cost < self.minimum:
            cost = self.minimum 
            

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