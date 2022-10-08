class Event:

    pass

class MarketEvent(Event):

    def __init__(self):
        self.type = 'MARKET'

# https://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-II/

# create all the events here
# these will be imported to the 
# other classes that then add different events to the queue
# the event handler checks for type and then executes certain 
# methods for its classes