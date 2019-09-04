import backtrader as bt


class Strategy(bt.Strategy):
    """
    Wrapper for `bt.Strategy` to log orders and perform other generic tasks.
    """

    def __init__(self):
        bt.Strategy.__init__(self)
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.order_rejected = False

    def log(self, txt, date=None):
        date = date or self.data.datetime.date(0)
        print('{}, {}'.format(date.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enought cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, {:.2f}, Cost: {:.2f}, Comm {:.2f}'.format(
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            if order.issell():
                self.log('SELL EXECUTED, {:.2f}, Cost: {:.2f}, Comm {:.2f}'.format(
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm))

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
            # print(order)
            self.log('Cash: {:.2f}, Order: {:.2f}'.format(self.broker.get_cash(),
                                                          order.price * order.size))
            self.order_rejected = True

        # Write down: no pending order
        self.order = None
