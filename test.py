from backtester.feed import CSVFeed
from backtester.strategy import BasicStragegy
from backtester.portfolio import BasicPortfolio
from backtester.broker import BacktestExecutionHandler
from backtester.event_handler import EventHandler

import matplotlib.pyplot as plt

feed = CSVFeed('test1.csv')
strategy = BasicStragegy(feed)
port = BasicPortfolio(100_000, feed=feed)
broker = BacktestExecutionHandler(feed=feed)

handler = EventHandler(feed, strategy, port, broker)
df = handler.start()
plt.plot(df['equity_curve'].values)
plt.show()