import math
import numpy as np

from backtrader import Analyzer, TimeFrame
from backtrader.analyzers import TimeReturn


class Sortino(Analyzer):
    params = (
        ('timeframe', TimeFrame.Years),
        ('compression', 1),
        ('riskfreerate', 0.01),
        ('factor', None),
        ('convertrate', True),
        ('annualize', False),
    )

    RATEFACTORS = {
        TimeFrame.Days: 252,
        TimeFrame.Weeks: 52,
        TimeFrame.Months: 12,
        TimeFrame.Years: 1,
    }

    def __init__(self):
        super(Sortino, self).__init__()
        self.ret = TimeReturn(
            timeframe=self.p.timeframe,
            compression=self.p.compression)
        self.ratio = 0.0

    def stop(self):
        returns = list(self.ret.get_analysis().values())

        rate = self.p.riskfreerate

        factor = None
        if self.p.timeframe in self.RATEFACTORS:
            # Get the conversion factor from the default table
            factor = self.RATEFACTORS[self.p.timeframe]

        if factor is not None:
            # A factor was found
            if self.p.convertrate:
                # Standard: downgrade annual returns to timeframe factor
                rate = pow(1.0 + rate, 1.0 / factor) - 1.0
            else:
                # Else upgrade returns to yearly returns
                returns = [pow(1.0 + x, factor) - 1.0 for x in returns]

        if len(returns):
            # Sortino Ratio = (R - T) / TDD
            #   R = Avg Returns
            #   T = Target (risk-free rate)
            #   TDD = Downside Risk
            ret_free_avg = np.mean(returns) - rate
            tdd = math.sqrt(np.mean([min(0, r - rate)**2 for r in returns]))

            try:
                ratio = ret_free_avg / tdd

                if factor is not None and \
                        self.p.convertrate and self.p.annualize:

                    ratio = math.sqrt(factor) * ratio
            except (ValueError, TypeError, ZeroDivisionError):
                ratio = None

        else:
            # no returns
            ratio = None

        self.ratio = ratio

    def get_analysis(self):
        return dict(sortino=self.ratio)
