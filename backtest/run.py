import datetime
import os.path
import argparse
import importlib

# Import the backtrader platform
import backtrader as bt
from backtrader import TimeFrame
from .util import commission, observers, analyzers


def run_strategy(strategy, tickers=None, start=1900, end=2100,
                 cash=100000.0, verbose=False, plot=False, plotreturns=False):
    start_date = datetime.datetime(start, 1, 1)
    end_date = datetime.datetime(end, 1, 1)

    tickers = tickers if tickers else ['SPY']

    module_path = f'.algos.{strategy}'
    module = importlib.import_module(module_path, 'backtest')
    strategy = getattr(module, strategy)

    cerebro = bt.Cerebro(stdstats=not plotreturns)

    # Add a strategy
    cerebro.addstrategy(strategy)

    # Set up data feed
    for ticker in tickers:
        datapath = os.path.join(os.path.dirname(__file__), f'../data/price/{ticker}.csv')
        data = bt.feeds.YahooFinanceCSVData(
            dataname=datapath,
            fromdate=start_date,
            todate=end_date,
            reverse=False,
            plot=not plotreturns)

        cerebro.adddata(data)

    # Set initial cash amount and commision
    cerebro.broker.setcash(cash)
    ib_comm = commission.IBCommision()
    cerebro.broker.addcommissioninfo(ib_comm)

    # Add obervers
    if plotreturns:
        cerebro.addobserver(observers.Value)

    # Add analyzers
    if verbose:
        cerebro.addanalyzer(bt.analyzers.SharpeRatio,
                            riskfreerate=0.035, timeframe=TimeFrame.Days, annualize=True)
        cerebro.addanalyzer(analyzers.Sortino,
                            riskfreerate=0.035, timeframe=TimeFrame.Days, annualize=True)
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

    # Get analysis results
    if verbose:
        drawdown = results[0].analyzers.drawdown.get_analysis()['max']['drawdown']
        cagr = results[0].analyzers.returns.get_analysis()['rnorm100']
        sharpe = results[0].analyzers.sharperatio.get_analysis()['sharperatio']
        sortino = results[0].analyzers.sortino.get_analysis()['sortino']

        sharpe = 'None' if sharpe is None else round(sharpe, 5)
        print('ROI:\t\t{:.2f}%'.format(100.0 * ((end_value / start_value) - 1.0)))
        analyzer_results = []
        analyzer_results.append('Max Drawdown:\t{:.2f}'.format(drawdown))
        analyzer_results.append('CAGR:\t\t{:.2f}'.format(cagr))
        analyzer_results.append('Sharpe:\t\t{}'.format(sharpe))
        analyzer_results.append('Sortino:\t{:.5f}'.format(sortino))
        print('\n'.join(analyzer_results))


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('strategy', nargs=1)
    PARSER.add_argument('-t', '--tickers', nargs='+')
    PARSER.add_argument('-s', '--start', nargs=1, type=int)
    PARSER.add_argument('-e', '--end', nargs=1, type=int)
    PARSER.add_argument('--cash', nargs=1, type=int)
    PARSER.add_argument('-v', '--verbose', action="store_true")
    PARSER.add_argument('-p', '--plot', action="store_true")
    PARSER.add_argument('--plotreturns', action="store_true")
    ARGS = PARSER.parse_args()
    ARG_ITEMS = vars(ARGS)
    STRATEGY_ARGS = {}

    # Parse multiple tickers
    STRATEGY_ARGS['tickers'] = ARG_ITEMS['tickers']
    del ARG_ITEMS['tickers']

    # Remove None Values
    for arg, val in ARG_ITEMS.items():
        if val:
            STRATEGY_ARGS[arg] = val[0] if isinstance(val, list) else val

    run_strategy(**STRATEGY_ARGS)
