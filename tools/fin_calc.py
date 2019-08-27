import numpy as np
import pandas as pd
import scipy.stats as stats
from datetime import datetime, timedelta


def log_returns(data):
    return np.log(data).diff().iloc[1:]


def calc_beta(x_name, window, returns_data):
    window_inv = 1.0 / window

    x_sum = returns_data[x_name].rolling(window, min_periods=window).sum()
    y_sum = returns_data.rolling(window, min_periods=window).sum()

    xy_sum = returns_data.mul(returns_data[x_name], axis=0).rolling(window, min_periods=window).sum()
    xx_sum = np.square(returns_data[x_name]).rolling(window, min_periods=window).sum()

    xy_cov = xy_sum - window_inv * y_sum.mul(x_sum, axis=0)
    x_var = xx_sum - window_inv * np.square(x_sum)

    betas = xy_cov.divide(x_var, axis=0)[window - 1:]
    betas.columns.name = None
    return betas


# alpha = return - risk_free - beta * (market - risk_free)
def calc_alpha(returns, market_returns, risk_free_returns, beta):
    returns_over_risk_free = returns.subtract(risk_free_returns, axis=0)
    market_over_risk_free = market_returns - risk_free_returns
    beta_market_risk_free = beta.multiply(market_over_risk_free, axis=0)

    alpha = returns_over_risk_free - beta_market_risk_free.values
    return alpha


def get_ndays_return(daily_returns, ndays=22):
    ndays_returns = (1 + daily_returns).rolling(ndays, min_periods=ndays).apply(np.prod, raw=True) - 1
    return ndays_returns.iloc[ndays-1:]


def top_alpha(stocks, market, risk_free, window, top_n_count=0):
    assert(stocks.shape[0] == market.shape[0] and market.shape[0] == risk_free.shape[0]
           ), 'inputs do not have same shape: {} {} {}'.format(stocks.shape[0], market.shape[0], risk_free.shape[0])

    # calculate betas for all stocks
    market_name = 'market_returns'
    market = market.rename(market_name)
    returns_data = pd.concat([market, stocks], axis=1)
    betas = calc_beta(market_name, window, returns_data).drop(market_name, axis=1)

    # calculate n-day returns for each date
    stocks_nday_returns = get_ndays_return(stocks, window)
    market_nday_returns = get_ndays_return(market, window)
    risk_free_nday_returns = get_ndays_return(risk_free, window)

    # calculate alpha
    alpha = calc_alpha(stocks_nday_returns, market_nday_returns, risk_free_nday_returns, betas)

    return alpha.iloc[-1].nlargest(top_n_count) if top_n_count > 0 else alpha.sort(ascending=False)


if __name__ == '__main__':
    # do nothing
    print('fin_calc imported')
