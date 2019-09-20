import numpy as np
import pandas as pd

from . import BaseStrategy as base


class EqualVolatility(base.Strategy):
    """
    Given a set of equities, balance volatilities monthly.
    """

    params = {
        'rebalance_days': 21,
        'target_percent': 0.95,
        'lookback': 21
    }

    def __init__(self):
        base.Strategy.__init__(self)

    def rebalance(self):
        vols = []
        for d in self.datas:
            returns = pd.Series(d.close.get(size=self.params.lookback))
            returns = np.log(returns).diff().iloc[1:]
            vol = returns.std()
            vols.append(vol)
        vols = np.array(vols)

        order_sort = []
        weights = []
        for v, d in zip(vols, self.datas):
            weight = (1.0 / v) / sum(1.0 / vols)
            weights.append(weight)
            position = self.getposition(d)
            position_value = position.size * position.price
            order_target = self.params.target_percent * weight * self.broker.get_value()
            order_sort.append(order_target - position_value)

        for s, d, w in sorted(zip(order_sort, self.datas, weights), key=lambda pair: pair[0]):
            self.order_target_percent(d, self.params.target_percent * w)

    def next(self):
        if self.order:
            # Skip if order is pending
            return

        # Rebalance portfolio
        if len(self) % self.params.rebalance_days == 0:
            self.rebalance()

        # Retry order on next day if rejected
        elif self.order_rejected:
            self.rebalance()
            self.order_rejected = False
