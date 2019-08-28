import datetime
import os.path
import sys
import argparse

# Import the backtrader platform
import backtrader as bt


class TestStrategy(bt.Strategy):
    def next(self):
        if not self.getposition(self.data).size:
            self.order_target_percent(self.data, target=1.0)


def buyAndHold(ticker, start_date, end_date, amount=10000.0, verbose=False):
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Set up data feed
    datapath = os.path.join(os.path.dirname(__file__), '../data/price/{ticker}.csv'.format(ticker=ticker))
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=start_date,
        todate=end_date,
        reverse=False)
    cerebro.adddata(data)

    # Add analyzers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.0)
    cerebro.addanalyzer(bt.analyzers.Returns)
    cerebro.addanalyzer(bt.analyzers.DrawDown)

    # Set initial cash amount
    cerebro.broker.setcash(amount)

    if verbose:
        print('Starting Portfolio Value:\t{:.2f}'.format(cerebro.broker.getvalue()))

    # Run backtest
    results = cerebro.run()

    end_value = cerebro.broker.getvalue()
    if verbose:
        print('Final Portfolio Value:\t\t{:.2f}'.format(end_value))

    # Get results
    dd = results[0].analyzers.drawdown.get_analysis()['max']['drawdown']
    cagr = results[0].analyzers.returns.get_analysis()['rnorm100']
    sharpe = results[0].analyzers.sharperatio.get_analysis()['sharperatio']

    return (end_value, dd, cagr, sharpe)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--ticker', nargs=1)
    parser.add_argument('-s', '--start', nargs=1, type=int)
    parser.add_argument('-e', '--end', nargs=1, type=int)
    args = parser.parse_args()

    start_value = 100000.0
    start_date = datetime.datetime(args.start[0], 1, 1) if args.start else datetime.datetime(1900, 1, 1)
    end_date = datetime.datetime(args.end[0], 1, 1) if args.end else datetime.datetime(2100, 1, 1)

    ticker = args.ticker[0] if args.ticker else 'SPY'
    print('Buy and Hold:', ticker)

    end_value, dd, cagr, sharpe = buyAndHold(ticker, start_date=start_date,
                                             end_date=end_date, amount=start_value, verbose=True)

    sharpe = sharpe is None and 'None' or round(sharpe, 3)
    print('ROI:\t\t{:.2f}%'.format(100.0 * ((end_value / start_value) - 1.0)))
    print('Max Drawdown:\t{:.2f}%\nCAGR:\t\t{:.2f}%\nSharpe:\t\t{}'.format(dd, cagr, sharpe))
