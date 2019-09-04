# Import the backtrader platform
import backtrader as bt

from . import BaseStrategy as base


class LeveragedEtfPair(base.Strategy):
    params = {}

    def __init__(self):
        base.Strategy.__init__(self)

    def next(self):
        if self.order:
            # Skip if order is pending
            return

        if not self.position:
            # Buy logic
            print('Buy')

        else:
            # Sell logic
            print('Sell')
