import datetime
import os.path
import argparse
import importlib
import dateutil.parser

import pandas as pd
import numpy as np

# Import the backtrader platform
import backtrader as bt
from backtrader import TimeFrame
from .util import commission, observers, analyzers
from .util import universe as universe_util


def clean_tickers(tickers, start, end):
    data_path = os.path.join(os.path.dirname(__file__), '../data/price/')
    out_tickers = []

    for ticker in tickers:
        d = pd.read_csv(data_path + ticker + '.csv', index_col=0, parse_dates=True)
        if not (d.tail(1).index[0] < start or
                d.head(1).index[0] > end):
            out_tickers.append(ticker)
        else:
            print('Data out of date range:', ticker)

    return out_tickers


def run_strategy(strategy, tickers=None, start='1900-01-01', end='2100-01-01', cash=100000.0,
                 verbose=False, plot=False, plotreturns=False, universe=None, exclude=[],
                 kwargs=None):
    start_date = dateutil.parser.isoparse(start)
    end_date = dateutil.parser.isoparse(end)

    tickers = tickers if (tickers or universe) else ['SPY']
    if universe:
        u = universe_util.get(universe)()
        tickers = [a for a in u.assets if a not in exclude]

    tickers = clean_tickers(tickers, start_date, end_date)

    module_path = f'.algos.{strategy}'
    module = importlib.import_module(module_path, 'backtest')
    strategy = getattr(module, strategy)

    cerebro = bt.Cerebro(
        stdstats=not plotreturns,
        cheat_on_open=strategy.params.cheat_on_open
    )

    # Add a strategy
    cerebro.addstrategy(strategy, verbose=verbose)

    # Set up data feed
    for ticker in tickers:
        datapath = os.path.join(os.path.dirname(__file__), f'../data/price/{ticker}.csv')
        data = bt.feeds.YahooFinanceCSVData(
            dataname=datapath,
            fromdate=start_date,
            todate=end_date,
            reverse=False,
            adjclose=False,
            plot=not plotreturns)

        cerebro.adddata(data)

    # Set initial cash amount and commision
    cerebro.broker.setcash(cash)
    # ib_comm = commission.IBCommision()
    # cerebro.broker.addcommissioninfo(ib_comm)

    # Add obervers
    if plotreturns:
        cerebro.addobserver(observers.Value)

    # Add analyzers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio,
                        riskfreerate=strategy.params.riskfreerate,
                        timeframe=TimeFrame.Days,
                        annualize=True)
    cerebro.addanalyzer(analyzers.Sortino,
                        riskfreerate=strategy.params.riskfreerate,
                        timeframe=TimeFrame.Days,
                        annualize=True)
    cerebro.addanalyzer(bt.analyzers.Returns)
    cerebro.addanalyzer(bt.analyzers.DrawDown)
    cerebro.addanalyzer(bt.analyzers.PositionsValue)
    cerebro.addanalyzer(bt.analyzers.GrossLeverage)

    # Run backtest
    results = cerebro.run(preload=False)

    # Print results
    start_value = cash
    end_value = cerebro.broker.getvalue()
    print('Starting Portfolio Value:\t{:.2f}'.format(cash))
    print('Final Portfolio Value:\t\t{:.2f}'.format(end_value))

    # Get analysis results
    drawdown = results[0].analyzers.drawdown.get_analysis()['max']['drawdown']
    cagr = results[0].analyzers.returns.get_analysis()['rnorm100']
    sharpe = results[0].analyzers.sharperatio.get_analysis()['sharperatio']
    sortino = results[0].analyzers.sortino.get_analysis()['sortino']
    positions = results[0].analyzers.positionsvalue.get_analysis()
    avg_positions = np.mean([sum(d != 0.0 for d in i) for i in positions.values()])
    leverage = results[0].analyzers.grossleverage.get_analysis()
    avg_leverage = np.mean([abs(i) for i in leverage.values()])

    sharpe = 'None' if sharpe is None else round(sharpe, 5)
    print('ROI:\t\t{:.2f}%'.format(100.0 * ((end_value / start_value) - 1.0)))
    analyzer_results = []
    analyzer_results.append('Max Drawdown:\t{:.2f}'.format(drawdown))
    analyzer_results.append('CAGR:\t\t{:.2f}'.format(cagr))
    analyzer_results.append('Sharpe:\t\t{}'.format(sharpe))
    analyzer_results.append('Sortino:\t{:.5f}'.format(sortino))
    analyzer_results.append('Positions:\t{:.5f}'.format(avg_positions))
    analyzer_results.append('Leverage:\t{:.5f}'.format(avg_leverage))
    print('\n'.join(analyzer_results))

    # Plot results
    if plot:
        cerebro.plot()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('strategy', nargs=1)
    PARSER.add_argument('-t', '--tickers', nargs='+')
    PARSER.add_argument('-u', '--universe', nargs=1)
    PARSER.add_argument('-x', '--exclude', nargs='+')
    PARSER.add_argument('-s', '--start', nargs=1)
    PARSER.add_argument('-e', '--end', nargs=1)
    PARSER.add_argument('--cash', nargs=1, type=int)
    PARSER.add_argument('-v', '--verbose', action='store_true')
    PARSER.add_argument('-p', '--plot', action='store_true')
    PARSER.add_argument('--plotreturns', action='store_true')
    PARSER.add_argument('-k', '--kwargs', nargs='+')
    ARGS = PARSER.parse_args()
    ARG_ITEMS = vars(ARGS)

    # Parse multiple tickers / kwargs
    TICKERS = ARG_ITEMS['tickers']
    KWARGS = ARG_ITEMS['kwargs']
    EXCLUDE = ARG_ITEMS['exclude']
    del ARG_ITEMS['tickers']
    del ARG_ITEMS['kwargs']
    del ARG_ITEMS['exclude']

    # Remove None values
    STRATEGY_ARGS = {k: (v[0] if isinstance(v, list) else v) for k, v in ARG_ITEMS.items() if v}
    STRATEGY_ARGS['tickers'] = TICKERS
    STRATEGY_ARGS['kwargs'] = KWARGS

    if EXCLUDE:
        STRATEGY_ARGS['exclude'] = [EXCLUDE] if len(EXCLUDE) == 1 else EXCLUDE

    run_strategy(**STRATEGY_ARGS)
