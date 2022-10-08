class Portfolio:

    def __init__(self, starting_balance=10_000):

        self.starting_balance = starting_balance

        self.positions = {}

    def update(self, signal=None, fill=None):
        if signal is not None:
            self.update_signal(signal)
        if fill is not None:
            self.update_fill(fill)
        
    def update_signal(self, signal):
        raise NotImplementedError('update signal is not implemented in Portfolio')

    