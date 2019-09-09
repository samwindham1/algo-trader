import backtrader as bt


class Value(bt.Observer):
    alias = ('Value',)
    lines = ('value',)

    plotinfo = dict(plot=True, subplot=True)

    def next(self):
        self.lines.value[0] = self._owner.broker.getvalue()
