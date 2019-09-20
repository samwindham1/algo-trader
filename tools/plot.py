import os
import argparse
from datetime import datetime

import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
from matplotlib import pyplot as plt


def plot(data, plot_returns=False):
    if plot_returns:
        data = _log_returns(data)

    plt.clf()
    for y in data:
        print(y.name)
        plt.plot(y, label=y.name)

    plt.legend()
    plt.tight_layout()
    plt.show()


def _log_returns(data):
    log_d = []
    for d in data:
        r = np.log(d).diff()
        r.iloc[0] = 0.0
        r = np.cumprod(r + 1) - 1
        log_d.append(r)
    return log_d


if __name__ == '__main__':
    register_matplotlib_converters()  # Suppress Pandas warning

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('tickers', nargs='+')
    PARSER.add_argument('-r', '--returns', action="store_true")
    PARSER.add_argument('-s', '--start', nargs=1, type=int)
    PARSER.add_argument('-e', '--end', nargs=1, type=int)
    ARGS = PARSER.parse_args()

    TICKERS = ARGS.tickers

    START = ARGS.start or [1900]
    END = ARGS.end or [2100]
    START_DATE = datetime(START[0], 1, 1)
    END_DATE = datetime(END[0], 1, 1)

    DATA = []
    for ticker in TICKERS:
        datapath = os.path.join(os.path.dirname(__file__), f'../data/price/{ticker}.csv')
        ticker_data = pd.read_csv(datapath, index_col='Date', parse_dates=True)['Adj Close'].rename(ticker)
        DATA.append(ticker_data.loc[START_DATE: END_DATE])

    plot(DATA, plot_returns=ARGS.returns)
