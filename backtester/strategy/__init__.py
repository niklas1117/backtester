import numpy as np 
import matplotlib.pyplot as plt
from datetime import datetime

# strategy is there to create signals 
# the signals will be then 

# the stats etc are supposed to go to the portfolio


class Strategy:
    def __init__(self, feed, broker):
        self.feed = feed 
        self.broker = broker
        self.instruments = self.feed.instruments
        self.status = 'waiting'
        self.feed.attach(broker)
        self.feed.attach(self)
        self.equity_stats = {
            'datetime':np.array(()), 
            'equity':np.array(()), 
            'cash':np.array(()), 
            'position':np.array(()),
            'adj':self.feed.adjustment_factor
        }

    def start(self):
        self.feed.start()

    def update(self, bars=None,eof=None):
        if bars is not None:
            self.__on_bars(bars)
            self.update_equity()
        if eof is not None:
            self.on_eof()

    def __on_bars(self, bars):
        self.on_bars(bars)

    def on_bars(self, bars):
        raise NotImplementedError('You have to create a subclass to test a strategy')
        # ts = self.feed.timeseries        
        # for instrument in self.instruments:
        #     close = ts[instrument]['close']
        #     if close <= sum(close[200:])/len(close[200:]):
        #         self.broker.submit_order

    def submit_order(self, order):
        self.broker.submit_order(order)

    @property
    def orders(self):
        return self.broker.orders

    @property
    def cash(self):
        return self.broker.cash

    @property
    def positons_value(self):
        return self.broker.pos_value

    @property
    def positions(self):
        return self.broker.positions

    @property  
    def limit_order_value(self):
        return self.broker.limit_order_value ## make all of these attributes (in broker)

    def get_limit_order_quantity(self, instrument):
        return self.broker.get_limit_order_quantity(instrument)

    def get_timeseries(self):
        return self.feed.timeseries

    def get_output(self):
        pass

    def update_equity(self):
        self.equity_stats['datetime'] = np.append(self.equity_stats['datetime'], 
            self.feed.current_date)
        self.equity_stats['equity'] = np.append(self.equity_stats['equity'], 
            self.broker.equity)
        self.equity_stats['cash'] = np.append(self.equity_stats['cash'], 
            self.broker.cash)
        self.equity_stats['position'] = np.append(self.equity_stats['position'], 
            self.broker.pos_value)

    def on_eof(self):
        pass