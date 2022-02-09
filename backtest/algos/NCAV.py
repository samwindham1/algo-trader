# Import the backtrader platform
import numpy as np
import pandas as pd

from . import BaseStrategy as base
from data.info.info import all_balance


class NCAV(base.Strategy):
    params = {
        'rebalance_days': 252,
        'target_percent': 0.95,
        'ncav_limit': 1.5
    }

    def __init__(self):
        base.Strategy.__init__(self)
        self.info = all_balance([d._name for d in self.datas])
        self.long = []

    def filter(self):
        self.long = []
        for d in self.datas:
            infos = self.info[self.info.Ticker == d._name]
            info = infos.loc[(pd.to_datetime(infos['Report Date']) > self.data.datetime.datetime()).idxmax()]

            ncav = (info['Total Current Assets'] - info['Total Liabilities']) / info['Shares (Basic)']

            if ncav > self.params.ncav_limit:
                self.long.append(d)

    def rebalance(self):
        for d in self.datas:
            if d in self.long:
                # Go long equal weight if in long list
                split_target = self.params.target_percent / len(self.long)
                self.order_target_percent(d, target=split_target)
            else:
                # Exit order or order none if not long list
                self.order_target_percent(d, target=0.0)

    def next(self):
        if self.order:
            # Skip if order is pending
            return

        # Rebalance portfolio
        if len(self) % self.params.rebalance_days == 0:
            self.filter()
            self.rebalance()

        # Retry order on next day if rejected
        elif self.order_rejected:
            self.rebalance()
            self.order_rejected = False
