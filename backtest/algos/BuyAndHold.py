from . import BaseStrategy as base


class BuyAndHold(base.Strategy):
    def next(self):
        if not self.getposition(self.data).size:
            self.order_target_percent(self.data, target=0.99)
