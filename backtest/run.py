import datetime
import os.path
import argparse
import importlib

# Import the backtrader platform
import backtrader as bt
from .util.commission import IBCommision


def run_strategy(strategy, ticker=None, start=1900, end=2100,
                 cash=100000.0, verbose=False, plot=False):
    start_date = datetime.datetime(start, 1, 1)
    end_date = datetime.datetime(end, 1, 1)

    ticker = ticker if ticker else 'SPY'

    module_path = f'.algos.{strategy}'
    module = importlib.import_module(module_path, 'backtest')
    strategy = getattr(module, strategy)

    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(strategy)

    # Set up data feed
    datapath = os.path.join(os.path.dirname(__file__), '../data/price/{ticker}.csv'.format(ticker=ticker))
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=start_date,
        todate=end_date,
        reverse=False)

    cerebro.adddata(data)

    # Set initial cash amount and commision
    cerebro.broker.setcash(cash)
    ib_comm = IBCommision()
    cerebro.broker.addcommissioninfo(ib_comm)

    # Add analyzers
    if verbose:
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.035)
        cerebro.addanalyzer(bt.analyzers.Returns)
        cerebro.addanalyzer(bt.analyzers.DrawDown)

    # Run backtest
    results = cerebro.run()

    start_value = cash
    end_value = cerebro.broker.getvalue()
    print('Starting Portfolio Value:\t{:.2f}'.format(cash))
    print('Final Portfolio Value:\t\t{:.2f}'.format(end_value))

    # Plot results
    if plot:
        cerebro.plot()

    # Get results
    if verbose:
        drawdown = results[0].analyzers.drawdown.get_analysis()['max']['drawdown']
        cagr = results[0].analyzers.returns.get_analysis()['rnorm100']
        sharpe = results[0].analyzers.sharperatio.get_analysis()['sharperatio']

        sharpe = 'None' if sharpe is None else round(sharpe, 3)
        print('ROI:\t\t{:.2f}%'.format(100.0 * ((end_value / start_value) - 1.0)))
        print('Max Drawdown:\t{:.2f}%\nCAGR:\t\t{:.2f}%\nSharpe:\t\t{}'.format(drawdown, cagr, sharpe))


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('strategy', nargs=1)
    PARSER.add_argument('-t', '--ticker', nargs=1)
    PARSER.add_argument('-s', '--start', nargs=1, type=int)
    PARSER.add_argument('-e', '--end', nargs=1, type=int)
    PARSER.add_argument('--cash', nargs=1, type=int)
    PARSER.add_argument('-v', '--verbose', action="store_true")
    PARSER.add_argument('-p', '--plot', action="store_true")
    ARGS = PARSER.parse_args()

    # Remove None Values
    STRATEGY_ARGS = {}
    for arg, val in vars(ARGS).items():
        if val:
            STRATEGY_ARGS[arg] = val[0] if isinstance(val, list) else val

    run_strategy(**STRATEGY_ARGS)
