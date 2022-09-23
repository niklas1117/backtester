from typing import Protocol

class Subject(Protocol):
    def attach():
        ...
    def detach():
        ...
    def notify():
        ...

def feed_parser(df):
    ## this should take a dataframe and transform it into a feed of bars 
    return dict(df)
    

class Feed():
    def __init__():
        pass
    def attach():
        pass
    def detach():
        pass
    def notify():
        pass
    def start():
        pass
    def get_next_bar():
        pass
    def get_current_bar():
        pass
    def get_time_series():
        pass
    def __create_time_series():
        pass
    def reset():
        pass

class CSVFeed(Feed):
    pass