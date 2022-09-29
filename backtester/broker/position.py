
class Position:

    def __init__(self, instrument, price, quantity, orders:Order|list[Order]):
       
        self.instrument = instrument
        self.price = price
        self.quantity = quantity #sell if negative

    