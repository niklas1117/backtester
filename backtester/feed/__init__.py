import csv
from typing import Protocol
from .bars import Bar, Bars


class Observer(Protocol):
    def update(bar):
        ...
    # in the strategy class, update will call on_bar to create orders 
    # in the broker class, update will call on_bar to fill orders 


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

    def __init__(self, bars_dict:dict):
        self.__bars_dict = bars_dict
        self.__observers = []
        self.__past_bars = {}

        self.current_date = None
        self.current_bars = None

    def attach(self, observer:Observer):
        self.__observers.append(observer)
        
    def detach(self, observer:Observer):
        raise NotImplementedError('one day I might add a detach method')

    def notify(self, **kwargs):
        for observer in self.__observers:
            observer.update(**kwargs)

    def start(self):
        #start can notify observers with a new bar or with eof when done
        print('feed started')
        for date, bars in self.__bars_dict.items():
            ## notify somehow when feed is started
            self.current_date = date
            self.current_bars = bars
            self.notify(bars=bars)
            self.__past_bars[date] = bars
        self.notify(eof='eof')

    def get_current_date(self):
        return self.current_date

    def get_current_bar(self):
        return self.current_bars

    def get_time_series(self):
        raise NotImplementedError('Need to create a dataframe type object')


class CSVFeed(Feed):

    def __init__(self, csv_path):
        bars_dict=csv_parser(csv_path)
        super().__init__(bars_dict)