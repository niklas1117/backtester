
from typing import Mapping
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from backtester.feed import CSVFeed 
from backtester.broker import Broker
from backtester.broker.order import LimitOrder
from backtester.strategy import Strategy
from backtester.analysis import Analyzer


class NewStrat(Strategy):
    def on_bars(self, bars):
        ts = self.get_timeseries()
        ma = 500 
        for instrument in self.instruments:
            close = ts[instrument]['close']
            try:
                print(instrument, self.positions[instrument].quantity)
            except:
                pass
            if len(close) > ma:
                if close[-1] <= (0.8 * sum(close[ma:])/len(close[ma:])):
                    if self.cash >= ((close[-1])*1.1*50)+abs(self.limit_order_value):
                        self.submit_order(LimitOrder(close[-1], instrument, 'BUY' ,50, self.broker))
feed = CSVFeed('test1.csv')
broker = Broker()

strat = NewStrat(feed, broker)
strat.start()
