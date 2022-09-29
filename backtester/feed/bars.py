from dataclasses import dataclass

## it is important to adjust ohlc for adjusted close if possible

## bar and bars should be subclasses of dictionaries!! that is way faster
## bars is a dict of bar and then barfeed is a dict of a dict of a dict

@dataclass(slots=True)
class Bar:
    datetime: str ## maybe change this one day to a datetime object
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float
    adjust_close: bool = True

    def __post_init__(self):
        adj_factor = self.adj_close/self.close
        if self.adjust_close:
            self.open = self.open * adj_factor
            self.high = self.high * adj_factor
            self.low = self.low * adj_factor
            self.close = self.adj_close

    ## make the bars adjustable if adjust_close = True


class Bars(dict):

    def __init__(self, bar_dict):
        self.__bar_dict = bar_dict
        self.__check_dates()

    def __check_dates(self):
        # check if dates are aligned 
        current_date = None
        for instrument, bar in self.__bar_dict.items():
            if current_date == None:
                current_date = bar.datetime
            elif current_date != bar.datetime:
                raise ValueError('bar datetimes are not aligned')
    
    def __setitem__(self, instrument:str, bar:Bar):
        self.__bar_dict[instrument] = bar
        self.__check_dates()

    def __getitem__(self, instrument:str) -> Bar:
        return self.__bar_dict[instrument]

    @property
    def instruments(self) -> list:
        return list(self.__bar_dict.keys())

    @property
    def datetime(self):
        return next(iter(self.__bar_dict.values())).datetime
