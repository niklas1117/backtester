

class Position:

    def __init__(self, fill, instrument):
       
        self.instrument = instrument
        self.price = fill[0]
        self.quantity = fill[1] #sell if negative
        self.orders = [fill]

    def add(self, fill):
        self.orders.append(fill)

        new_quantity = self.quantity+fill[1]
        # self.price = ((self.price*self.quantity)+(fill[0]*fill[1]))/new_quantity
        self.quantity += fill[1]

    def get_value(self, bars):
        bar = bars[self.instrument]
        return bar.close * self.quantity

    def __repr__(self):
        return f'Position({self.quantity} {self.instrument} at {self.price}'