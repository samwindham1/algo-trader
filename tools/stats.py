import os
import argparse
from datetime import datetime

import numpy as np
import pandas as pd
import scipy
from scipy.stats import norm, laplace, t, levy_stable
from scipy.stats import kstest, chisquare

from . import fin_calc


def get_returns(data):
    total_returns = (data.iloc[-1] - data.iloc[0]) / data.iloc[0]
    annual_returns = (1 + total_returns) ** (255 / len(data)) - 1
    returns = fin_calc.log_returns(data)

    print('\n  Returns:')
    print(f'   - total:\t{round(total_returns * 100,2)}%')
    print(f'   - annual:\t{round(annual_returns * 100, 2)}%')

    return (returns, total_returns, annual_returns)


def get_moments(returns):
    moments = scipy.stats.describe(returns)

    print('\n  Moments:')
    print(f'   - mean:\t{round(moments.mean, 5)}')
    print(f'   - std:\t{round(np.sqrt(moments.variance), 5)}')
    print(f'   - skew:\t{round(moments.skewness, 5)}')
    print(f'   - kurt:\t{round(moments.kurtosis, 5)}')

    return moments


def get_simulations(returns):
    simulation_size = 100000

    sim_index = ['normal', 'laplace', 'student-t', 'levy-stable']
    sim_list = [norm, laplace, t, levy_stable]
    assert len(sim_index) == len(sim_list), 'Mismatch lengths'

    simulations = {}

    for name, sim in zip(sim_index, sim_list):
        fit_params = []
        if name == 'levy-stable':
            def pconv(
                alpha, beta, mu, sigma): return(
                    alpha, beta, mu - sigma * beta * np.tan(np.pi * alpha / 2.0), sigma)
            fit_params = pconv(*sim._fitstart(returns))
        else:
            fit_params = sim.fit(returns)

        rvs = pd.Series(sim.rvs(*fit_params, size=simulation_size))
        simulations[name] = {'sim': sim, 'rvs': rvs, 'params': fit_params}

    return simulations


def get_risk(returns, sims):
    print('\n  Risk:')
    confidence_level = .05

    var = fin_calc.var(returns, confidence_level)
    cvar = fin_calc.cvar(returns, var)

    risk_values = [[var, cvar]]

    # Calculate VAR and cVAR for each simulation
    for key in sims:
        rvs = sims[key]['rvs']
        sim_var = fin_calc.var(rvs, confidence_level)
        sim_cvar = fin_calc.cvar(rvs, sim_var)
        risk_values.append([sim_var, sim_cvar])

    risk_columns = ['VAR', 'cVAR']
    risk_df = pd.DataFrame(risk_values, columns=risk_columns, index=['historical', *sims.keys()])
    print(risk_df)
    return risk_df


def get_fit(data, sims):
    print('\n  Goodness of Fit: (p-value > 0.05)')

    for key in sims:
        sim = sims[key]
        ks = kstest(data, lambda x, s=sim: s['sim'].cdf(x, *s['params']))

        print(f'\t{key}: \t{ks.pvalue >= 0.05}\t(p-value {round(ks.pvalue, 5)})')


def get_stats(datas, verbose=False):
    for data in datas:
        print(f'--- {data.name} --- ({data.index[0].date()}, {data.index[-1].date()})')

        returns, total_returns, annual_returns = get_returns(data)
        get_moments(returns)
        if verbose:
            simulations = get_simulations(returns)
            get_risk(returns, simulations)
            get_fit(returns, simulations)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('tickers', nargs='+')
    PARSER.add_argument('-v', '--verbose', action="store_true")
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

    get_stats(DATA, verbose=ARGS.verbose)
