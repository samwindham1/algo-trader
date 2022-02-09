import os
import argparse

import pandas as pd
import numpy as np

import scipy
from scipy import stats

import statsmodels
from statsmodels.tsa.stattools import adfuller

from matplotlib import pyplot as plt


from tools import fin_calc


def hurst_exp(d):
    lags = range(2, 100)

    # Calculate the array of the variances of the lagged differences
    tau = [np.sqrt(np.std(d.diff(lag))) for lag in lags]

    # Use a linear fit to estimate the Hurst Exponent
    poly = np.polyfit(np.log(lags), np.log(tau), 1)

    # Return the Hurst exponent from the polyfit output
    return poly[0]*2.0


def variance_ratio(ts, lag=2):
    """
    Returns the variance ratio test result
    """
    # make sure we are working with an array, convert if necessary
    ts = np.asarray(ts)

    # Apply the formula to calculate the test
    n = len(ts)
    mu = sum(ts[1:n] - ts[:n-1]) / n
    m = (n - lag + 1) * (1 - lag / n)
    b = sum(np.square(ts[1:n] - ts[:n-1] - mu)) / (n - 1)
    t = sum(np.square(ts[lag:n] - ts[:n - lag] - lag * mu)) / m
    return t / (lag * b)


def main(tickers):
    df = load_data(tickers[0], tickers[1]).iloc[-1000:]

    a = df[tickers[0]]
    b = df[tickers[1]]

    # a_returns = fin_calc.log_returns(a)
    # b_returns = fin_calc.log_returns(b)

    series = a - b

    h = hurst_exp(np.log(series))
    print('Hurst:\t\t', h)

    vr = variance_ratio(np.log(series), 2)
    print('Var Ratio:\t', vr)

    ylag = np.roll(series, 1)
    ylag[0] = 0
    ydelta = series.diff(1)
    ydelta[0] = 0

    beta, _ = np.polyfit(ydelta, ylag, 1)
    halflife = -np.log(2) / beta
    print('Half Life:\t', halflife)

    # start = 0
    # end = len(df)

    # mean = stationary.iloc[start:end].mean()

    # plt.plot(list(df.index)[start:end], (stationary - mean).iloc[start:end])
    # plt.plot(list(df.index)[start:end], (df.ziv + df.vxx).iloc[start:end])
    # plt.plot([0 for x in range(end-start)])

    # plt.tight_layout()
    # plt.show()

    # adf, pval, lag, n, crit, icbest = adfuller(stationary - mean, maxlag=1)
    # print('adf:\t', adf)
    # print('pval:\t', pval)
    # print('lag:\t', lag)
    # print('crit:')
    # print(crit)


def load_data(ticker_a, ticker_b):
    a_path = os.path.join(os.path.dirname(__file__), f'../data/price/{ticker_a}.csv')
    a = pd.read_csv(a_path, index_col=0)['Adj Close'].rename(ticker_a)

    b_path = os.path.join(os.path.dirname(__file__), f'../data/price/{ticker_b}.csv')
    b = pd.read_csv(b_path, index_col=0)['Adj Close'].rename(ticker_b)

    df = pd.DataFrame({
        ticker_a: a,
        ticker_b: b
    }).dropna()

    return df


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('tickers', nargs=2)
    ARGS = PARSER.parse_args()

    main(ARGS.tickers)
