from . import BaseStrategy as base
import numpy as np


class WeightedHold(base.Strategy):
    params = (
        ('kwargs', None),
        ('target_percent', 0.99),
    )

    def __init__(self):
        base.Strategy.__init__(self)

        if self.params.kwargs:
            self.params.weights = [float(w) for w in self.params.kwargs]
        else:
            self.params.weights = [1 for d in self.datas]

        w_pos = [w for w in self.params.weights if w >= 0]
        w_neg = [w for w in self.params.weights if w < 0]
        self.weights = [(w / sum(w_pos)) if w in w_pos else (-w / sum(w_neg)) for w in self.params.weights]

    def buy_and_hold(self):
        for i, d in enumerate(self.datas):
            split_target = self.params.target_percent * self.weights[i]
            self.order_target_percent(d, target=split_target)

    def next(self):
        self.buy_and_hold()
