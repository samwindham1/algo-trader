# Import the backtrader platform
import numpy as np

from . import BaseStrategy as base


class PairSwitching(base.Strategy):
    """
    Use as data two oposing equities or ETFs

    :data: 2 datafeeds
    """

    params = {
        'rebalance_days': 21,
        'target_percent': 0.95,
        'lookback': 60
    }

    def __init__(self):
        base.Strategy.__init__(self)
        assert len(self.datas) == 2, "Exactly 2 datafeeds needed for this strategy!"

    def switch(self):
        prev0 = self.data0.close[-self.params.lookback]
        prev1 = self.data1.close[-self.params.lookback]

        # Calculate n-day returns
        return0 = np.log(self.data0.close[0]) - np.log(prev0)
        return1 = np.log(self.data1.close[0]) - np.log(prev1)

        if return0 > return1:
            self.order_target_percent(data=self.data1, target=0)
            self.order_target_percent(data=self.data0, target=self.params.target_percent)
        else:
            self.order_target_percent(data=self.data0, target=0)
            self.order_target_percent(data=self.data1, target=self.params.target_percent)

    def next(self):
        if self.order:
            # Skip if order is pending
            return

        if (len(self) - 1) % self.params.rebalance_days == 0:
            self.switch()

        # Retry order on next day if rejected
        elif self.order_rejected:
            self.switch()
            self.order_rejected = False
