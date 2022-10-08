import logging

def log(message):
    """add a filename to log to file"""
    print(message)
    logging.basicConfig(filename='backtest_log.txt', level=logging.INFO, 
        format='%(message)s', filemode='w')
    logging.info(message)