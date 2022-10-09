from queue import Queue


class EventHandler:

    def __init__(self, feed, strategy, port, broker):
        self.events = Queue()

        self.feed = feed
        self.feed.events = self.events

        self.strategy = strategy
        self.strategy.events = self.events
        self.strategy.feed = self.feed

        self.port = port
        self.port.events = self.events
        self.port.feed = self.feed
        self.port.start_date = self.feed.current_date

        self.broker = broker
        self.broker.events = self.events
        self.broker.feed = self.feed

    def start(self):
        while True:
            self.feed.update_bars()
            # try:
            event = self.events.get(False)
            if event == 'eod':
                break
            # else:
            if event is not None:
                if event.type == 'MARKET':
                    port.update_timeindex(event)
                    broker.execute_orders(event)
                    strategy.calculate_signals(event)
                if event.type == 'SIGNAL':
                    port.update_signal(event)        
                if event.type == 'ORDER':
                    broker.submit_order(event)
                if event.type == 'FILL':
                    port.update_fill(event)

        print('done')




# https://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-I/

# this will loop through events in the queue and call methods in the 
# classes based on that
