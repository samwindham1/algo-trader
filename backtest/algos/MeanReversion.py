import pandas as pd
import numpy as np
from . import BaseStrategy as base


class MeanReversion(base.Strategy):
    params = {
        'target_percent': 0.45,
        'riskfreerate': 0,
        'quantile': 0.10,
        'qauntile_vol': (1/3),
        'lookback': 6,
        'offset': 1,
        'order_frequency': 5,
        'cheat_on_open': False
    }

    def __init__(self):
        base.Strategy.__init__(self)
        self.count = 1
        self.rank = pd.Series()
        self.filter = []
        self.top = self.bottom = self.longs = self.shorts = self.closes = None
        self.order_valid = False

    def add_rank(self):

        # Ranking for Basic strategy
        #   Go long all worst losers, and short best winners

        for i, d in enumerate(self.datas):
            # Improvement 2:
            #   Delay lookback by 1 day
            prev = d.close.get(size=self.params.lookback, ago=self.params.offset)[0]
            pct_ret = (d.close[0] / prev) - 1
            self.rank.loc[i] = pct_ret

        quantile_top = self.rank.quantile(1 - self.params.quantile)
        self.top = list(self.rank[self.rank >= quantile_top].index)

        quantile_bottom = self.rank.quantile(self.params.quantile)
        self.bottom = list(self.rank[self.rank <= quantile_bottom].index)
        self.bottom_half = list(self.rank.nsmallest(int(len(self.datas) / 2.0)).index)

    def add_filter(self):

        # Improvement 1:
        #   Add a filter to remove large 1-day returns
        #   (Usually caused by news events)

        sd = pd.Series()
        for i, d in enumerate(self.datas):
            lookback = d.close.get(size=self.params.lookback, ago=self.params.offset)
            sd.loc[i] = np.std(lookback)

        quantile_std = sd.quantile(1 - self.params.qauntile_vol)
        self.filter = list(sd[sd < quantile_std].index)

        self.top = [t for t in self.top if t in self.filter]
        self.bottom = [b for b in self.bottom if b in self.filter]

    def process(self):
        self.add_rank()
        self.add_filter()

        self.longs = [d for (i, d) in enumerate(self.datas) if i in self.bottom]
        self.shorts = [d for (i, d) in enumerate(self.datas) if i in self.top]
        self.closes = [d for d in self.datas if (
            (d in self.bottom_half and d not in self.longs) or
            (d not in self.bottom_half and d not in self.shorts)
        )]

    def send_orders(self):
        for d in self.longs:
            split_target = 1.3 * self.params.target_percent / len(self.longs)
            self.order_target_percent(d, target=split_target)

        for d in self.shorts:
            split_target = -0.3 * self.params.target_percent / len(self.shorts)
            self.order_target_percent(d, target=split_target)

    def close_positions(self):
        for d in self.closes:
            self.close(d)

    def next(self):
        self.order_valid = (
            self.count > (self.params.lookback + self.params.offset) and
            self.count % self.params.order_frequency == 0
        )
        if self.order_valid:
            self.process()
            self.close_positions()
            self.send_orders()

        elif self.order_rejected:
            self.send_orders()
            self.order_rejected = False

        self.count += 1

    # def next_open(self):
    #     if self.order_valid:
    #         self.send_orders()

    #     self.count += 1
