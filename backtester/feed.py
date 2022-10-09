import csv
import datetime as dt
from typing import Protocol

import numpy as np
from backtester.event import MarketEvent

from backtester.bars import Bar, Bars

COL_TRANS = {
    '':'', 
    'Open':'open',
    'High':'high', 
    'Low':'low', 
    'Close':'close', 
    'Adj Close':'adj_close', 
    'Volume':'volume'
    }

def csv_parser(path):
    # check if columns names are in correct order and correct (not really)
    # takes a little while because creating Bar and Bars
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        columns = [(first, COL_TRANS[second]) 
            for first, second in zip(next(spamreader), next(spamreader))]
        columns[0] = ('', next(spamreader)[0])
        instruments = set([i[0] for i in columns[1:]])
        barfeed = {}
        for row in spamreader:
            data_dict = {inst:{} for inst in instruments}
            date = row[0]
            for value, col in zip(row[1:], columns[1:]):
                data_dict[col[0]]['datetime'] = date
                data_dict[col[0]][col[1]] = float(value)
            bars =  Bars({instrument: Bar(**value) for instrument, value in data_dict.items()})
            barfeed[date] = bars
    return barfeed


def df_parser(df):
    # check if columns names are in correct order and correct 
    bars_feed = {}
    for date, series in df.iterrows():
        instruments = set([i[0] for i in series.index])
        bars = {}
        for instrument in instruments:
            instrument_data = series[instrument]
            instrument_data['datetime'] = instrument_data.name
            instrument_data.rename({'Open':'open', 'High':'high', 'Low':'low', 
                'Close':'close', 'Adj Close':'adj_close', 'Volume':'volume'}, 
                inplace=True)
            bars[instrument] = Bar(**dict(instrument_data))
        bars_feed[date] = Bars(bars)
    return bars_feed


class Feed():

    """
    This is a bar feed that adheres to the subject protocol \n
    It that can be started and will notify observers of new ticks \n
    It is important that observers are attached in the correct order 
    """

    COLS = [
    'datetime', 
    'open', 
    'high', 
    'low', 
    'close', 
    'volume'
    ]

    FREQUENCY_TRANSLATION = {'1d':260}

    def __init__(self, bars_dict:dict, events=None, frequency='1d'):
        self._bars_dict = bars_dict
        self.events = events
        self.frequency = frequency
        self.current_bars = next(iter(self._bars_dict.values()))
        self.current_date = self.current_bars.datetime
        self.instruments = self.current_bars.instruments
        self.next_idx = 0
        self.dates = list(self._bars_dict.keys())
        self.__past_bars = {inst:{col:np.array([])for col in Feed.COLS} 
            for inst in self.instruments}

    def get_next_bars(self):
        if not self.next_idx == len(self.dates):
            self.current_bars = self._bars_dict[self.dates[self.next_idx]]
            self.current_date = self.current_bars.datetime
            self.append_to_past(self.current_bars)
            self.next_idx += 1
            return self.current_bars
        else:
            return 'eof'

    def get_current_date(self):
        return self.current_date

    def get_current_bars(self):
        return self.current_bars

    def get_timeseries(self):
        return self.timeseries

    def update_bars(self):
        bars = self.get_next_bars()
        self.events.put(MarketEvent(bars))
        # maybe make this a bit less structured 
        # (allow different amounts of instruments per date)

    @property
    def timeseries(self):
        return self.__past_bars

    def __append_instrument(self, instrument, datetime, open, high, low, close, 
            volume):
        """add each datapoint of a bar to the past_bars dict of dicts"""
        self.__past_bars[instrument]['datetime'] = np.append(
            self.__past_bars[instrument]['datetime'], datetime)
        self.__past_bars[instrument]['open'] = np.append(
            self.__past_bars[instrument]['open'], open)
        self.__past_bars[instrument]['high'] = np.append(
            self.__past_bars[instrument]['high'], high)
        self.__past_bars[instrument]['low'] = np.append(
            self.__past_bars[instrument]['low'], low)
        self.__past_bars[instrument]['close'] = np.append(
            self.__past_bars[instrument]['close'], close)
        self.__past_bars[instrument]['volume'] = np.append(
            self.__past_bars[instrument]['volume'], volume)
    
    def append_to_past(self, bars):
        for instrument in self.instruments:
            bar = bars[instrument]
            self.__append_instrument(instrument, **bar.to_dict())
        
    @property
    def adjustment_factor(self):
        return Feed.FREQUENCY_TRANSLATION[self.frequency]

    # def attach(self, observer:Observer):
    #     self.__observers.append(observer)
        
    # def detach(self, observer:Observer):
    #     raise NotImplementedError('one day I might add a detach method')

    # def notify(self, **kwargs):
    #     for observer in self.__observers:
    #         observer.update(**kwargs)

    # def start(self):
    #     #start can notify observers with a new bar or with eof when done
    #     print('feed started')
    #     for date, bars in self.__bars_dict.items():
    #         ## notify somehow when feed is started
    #         self.current_date = date
    #         self.current_bars = bars
    #         self.notify(bars=bars)
    #         self.append_to_past(bars)
    #     self.notify(eof='eof')

class CSVFeed(Feed):

    def __init__(self, csv_path, events=None):
        bars_dict=csv_parser(csv_path)
        super().__init__(bars_dict, events)
