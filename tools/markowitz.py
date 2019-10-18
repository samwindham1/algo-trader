import os
import argparse

import pandas as pd

from pypfopt import expected_returns
from pypfopt import risk_models
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices


def optimize(tickers, cash=1000, longshort=False):
    print(f'Cash: ${cash}')
    date_start = 20 * 6

    df = pd.DataFrame()
    for t in tickers:
        path = os.path.join(os.path.dirname(__file__), f'../data/price/{t}.csv')
        price = pd.read_csv(path, parse_dates=True, index_col='Date')['Adj Close'].rename(t)
        df[t] = price[-date_start:]

    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    # Optimise for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S, weight_bounds=((-1, 1) if longshort else (0, 1)))
    raw_weights = ef.max_sharpe()
    clean_weights = ef.clean_weights()

    latest_prices = get_latest_prices(df)
    da = DiscreteAllocation(raw_weights, latest_prices, total_portfolio_value=cash)
    allocation, leftover = da.lp_portfolio()

    print('\nWeights:', clean_weights)
    print('\nShares:', allocation)
    print(f'\n${leftover:.2f} leftover')

    ef.portfolio_performance(verbose=True)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-t', '--ticker', nargs='+')
    PARSER.add_argument('--cash', nargs=1, type=int)
    PARSER.add_argument('-ls', '--longshort', action="store_true")
    ARGS = PARSER.parse_args()

    CASH = ARGS.cash or [1000]

    if ARGS.ticker:
        optimize(ARGS.ticker, CASH[0], ARGS.longshort)
    else:
        TICKERS = ['TLT', 'FB', 'AAPL', 'AMZN', 'NFLX', 'GOOG']

        optimize(TICKERS, CASH[0], ARGS.longshort)
