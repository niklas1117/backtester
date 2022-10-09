from abc import ABC, abstractmethod

import pandas as pd
from backtester.event import OrderEvent


class Portfolio(ABC):

    fill_dir = {
        'BUY':1,
        'SELL':-1
    }
        
    @abstractmethod
    def update_signal(self, signal):
        raise NotImplementedError('update signal is not implemented in Portfolio')

    @abstractmethod
    def update_fill(self, fill):
        raise NotImplementedError('update fill not implemented')


class BasicPortfolio(Portfolio):

    def __init__(self, initial_capital, start_date=None, feed=None, 
            events=None):
        self.feed = feed
        self.events = events
        self.start_date = start_date
        self.instruments = self.bars.instruments
        self.initial_capital = initial_capital
        self.all_positions = self.create_all_positions() # quantity
        self.current_positions = {i:0 for i in self.instruments}
        self.all_holdings = self.create_all_holdings() # quantity*price
        self.current_holdings = self.create_current_holdings()

    def create_all_positions(self):
        d = {i:0 for i in self.instruments}
        d['datetime'] = self.start_date
        return [d]
    
    def create_all_holdings(self):
        d = {i:0 for i in self.instruments}
        d['datetime'] = self.start_date
        d['cash'] = self.initial_capital
        d['commission'] = 0
        d['total'] = self.initial_capital
        return [d]

    def create_current_holdings(self):
        d = {i:0 for i in self.instruments}
        d['cash'] = self.initial_capital
        d['commission'] = 0 
        d['total'] = self.initial_capital
        return d

    def update_timeindex(self, event):
        pos_dict = self.current_positions
        pos_dict['datetime'] = self.feed.current_date
        self.all_positions.append(pos_dict)
        hold_dict = self.current_holdings
        hold_dict['datetime'] = self.feed.current_date
        self.all_holdings.append(hold_dict)

    def update_positions_from_fill(self, fill):
        dir = self.fill_dir[fill.direction]
        self.current_positions[fill.instrument] += (dir*fill.quantity)

    def update_holdings_from_fill(self, fill):
        dir = self.fill_dir[fill.direction]
        fill_cost = fill.fill_price
        cost = self.fill_dir[fill.direction] * fill_cost * fill.quantity
        self.current_holdings[fill.instrument] += cost
        self.current_holdings['cash'] -= (cost + fill.commission)
        self.current_holdings['commission'] += fill.commission
        self.current_holdings['total'] -= (cost + fill.commission)

    def update_fill(self, fill):
        self.update_positions_from_fill(fill)
        self.update_holdings_from_fill(fill)

    def generate_basic_order(self, signal):
        # these will become elaborate and will implement risk management
        # and position sizing
        order = None
        instrument = signal.instrument
        close = self.feed.current_bars[instrument]['close']
        direction = signal.signal_type
        strength = signal.strength
        quantity = round(100 * strength)
        cur_quantity = self.current_positions[instrument]
        order_type = 'LIMIT'
        if direction == 'BUY' and cur_quantity == 0:
            order = OrderEvent(instrument, order_type, quantity, 'BUY', 
                limit=close*0.98)
        if direction == 'SELL' and cur_quantity == 0:
            order = OrderEvent(instrument, order_type, quantity, 'SELL',    
            limit=close*1.02)       
        if direction == 'SELL_CLOSE' and cur_quantity > 0:
            order = OrderEvent(instrument, order_type, abs(cur_quantity), 
                'SELL', limit=close*1.02)
        if direction == 'BUY_CLOSE' and cur_quantity < 0:
            order = OrderEvent(instrument, order_type, abs(cur_quantity), 
            'BUY', limit=close*0.98)
        return order

    def update_signal(self, signal):
        order_event = self.generate_basic_order(signal)
        self.events.put(order_event)
    
    def create_equity_curve_df(self):
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1.0+curve['returns']).cumprod()
        self.equity_curve = curve

    