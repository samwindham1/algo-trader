import pandas as pd
import numpy as np
from . import BaseStrategy as base


class MeanReversion(base.Strategy):
    params = {
        'target_percent': 0.95,
        'riskfreerate': 0,
        'quantile': 0.10,
        'npositions': 25,
        'quantile_std': 0.10,
        'quantile_vol': 1.0,
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
        self.values = []

    def add_rank(self):

        # Ranking for Basic strategy
        #   Go long all worst losers, and short best winners

        for i, d in enumerate(self.datas):
            if len(d) < self.params.lookback + self.params.offset:
                continue

            if i not in self.filter:
                continue

            # Improvement 2:
            #   Delay lookback by 1 day

            prev = d.close.get(size=self.params.lookback, ago=self.params.offset)[0]
            pct_ret = (d.close[0] / prev) - 1
            self.rank.loc[i] = pct_ret

        if self.params.npositions > 0:
            self.top = list(self.rank.nlargest(self.params.npositions).index)
            self.bottom = list(self.rank.nsmallest(self.params.npositions).index)
        else:
            quantile_top = self.rank.quantile(1 - self.params.quantile)
            self.top = list(self.rank[self.rank >= quantile_top].index)

            quantile_bottom = self.rank.quantile(self.params.quantile)
            self.bottom = list(self.rank[self.rank <= quantile_bottom].index)

    def add_filter(self):

        # Filter function to filter out datas from current timestep

        sd = pd.Series()
        vol = pd.Series()
        for i, d in enumerate(self.datas):
            if len(d) < self.params.lookback + self.params.offset:
                continue

            # Improvement 1:
            #   Add a filter to remove large 1-day returns
            #   (Usually caused by news events)
            lookback = d.close.get(size=self.params.lookback, ago=self.params.offset)
            returns = np.diff(np.log(lookback))[1:]
            sd.loc[i] = np.std(returns)

            # Improvement 3:
            #   Add filter to remove all high-volatility stocks
            lookback = d.close.get(size=min(126, len(d)), ago=self.params.offset)
            returns = np.diff(np.log(lookback))[1:]
            vol.loc[i] = np.std(lookback)

        quantile_std = sd.quantile(1 - self.params.quantile_std)
        quantile_vol = vol.quantile(1 - self.params.quantile_vol)
        sd = list(sd[sd <= quantile_std].index)
        vol = list(vol[vol <= quantile_vol].index)

        self.filter = list(set(sd) | set(vol))
        # self.filter = sd

    def process(self):
        self.add_filter()
        self.add_rank()

        self.longs = [d for (i, d) in enumerate(self.datas) if i in self.bottom]
        self.shorts = [d for (i, d) in enumerate(self.datas) if i in self.top]
        self.closes = [d for d in self.datas if (
            (d not in self.longs) and
            (d not in self.shorts)
        )]

    def send_orders(self):
        for d in self.longs:
            if len(d) < self.params.lookback + self.params.offset:
                continue

            split_target = 1 * self.params.target_percent / len(self.longs)
            self.order_target_percent(d, target=split_target)

        for d in self.shorts:
            if len(d) < self.params.lookback + self.params.offset:
                continue

            split_target = -1 * self.params.target_percent / len(self.shorts)
            self.order_target_percent(d, target=split_target)

    def set_kelly_weights(self):
        value = self.broker.get_value()
        self.values.append(value)

        kelly_lookback = 20

        if self.count > kelly_lookback:
            d = pd.Series(self.values[-kelly_lookback:])
            r = d.pct_change()

            mu = np.mean(r)
            std = np.std(r)
            if std == 0.0:
                return

            f = (mu)/(std**2)
            if f == np.nan:
                return
            self.params.target_percent = max(0.2, min(2.0, f / 2.0))
            print(self.params.target_percent)

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

        self.set_kelly_weights()
        self.count += 1

    def prenext(self):
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

        self.set_kelly_weights()
        self.count += 1

    # def next_open(self):
    #     if self.order_valid:
    #         self.send_orders()

    #     self.count += 1
