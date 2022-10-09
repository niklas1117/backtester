from backtester.feed import CSVFeed
from backtester.strategy import BasicStragegy
from backtester.portfolio import BasicPortfolio
from backtester.broker import BacktestExecutionHandler
from backtester.event_handler import EventHandler

feed = CSVFeed('test_csv.csv')
strategy = BasicStragegy()
port = BasicPortfolio(100_000)
broker = BacktestExecutionHandler()

handler = EventHandler(feed, strategy, port, broker)
handler.start()
