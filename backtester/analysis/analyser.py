import matplotlib.pyplot as plt
from datetime import datetime as dt
import numpy as np

class Analyzer:

    def __init__(self, equity_stats):
        self.datetime = [dt.fromisoformat(i) for i in equity_stats['datetime']]
        self.equity = equity_stats['equity']
        self.cash = equity_stats['cash']
        self.position = equity_stats['position']
        self.adj = equity_stats['adj']

    
    def plot(self, log_scale=False):
        fig, ax = plt.subplots(figsize=(13,7))
        ax.plot(self.datetime, self.equity, label='equity', color='black', 
            linewidth=1.5)
        ax.plot(self.datetime, self.cash, label='cash', linestyle='dashed', 
            color='green', linewidth=1, alpha=0.7)
        ax.plot(self.datetime, self.position, label='position', 
            linestyle='dashed', color='blue', linewidth=1, alpha=0.7)
        if log_scale:
            ax.set_yscale('log')
        fig.legend()
        plt.show()
    
    def summary(self):
        adj = self.adj
        rets = np.diff(self.equity)/self.equity[:-1] 
        dd = ((self.equity/np.maximum.accumulate(self.equity)) -1) 
        mean = np.mean(rets) * adj
        std = np.std(rets) * np.sqrt(adj)
        sharpe = mean/std
        max_dd = dd.min()
        return {'return':mean, 'stdev':std, 'sharpe': sharpe, 
            'max drawdown':max_dd}