import os
import argparse
from datetime import date
import pandas as pd

from api import yahoo


def save_ticker(ticker):
    historical = yahoo.get_daily(ticker)
    historical.to_csv(os.path.join(os.path.dirname(__file__), '../data/price/{ticker}.csv'.format(ticker=ticker)))


def save_all(tickers):
    group_size = 10
    for i in range(0, len(tickers), group_size):
        ticker_group = list(tickers)[i: i + group_size]
        print(ticker_group)
        historical = yahoo.get_daily_async(ticker_group)
        for ticker in ticker_group:
            first_valid = historical[ticker][historical[ticker].notnull().any(axis=1)].index[0]
            historical[ticker].loc[first_valid:].to_csv(os.path.join(
                os.path.dirname(__file__),
                '../data/price/{ticker}.csv'.format(ticker=ticker)))


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-t', '--ticker', nargs='+')
    ARGS = PARSER.parse_args()

    if ARGS.ticker:
        if len(ARGS.ticker) > 1:
            save_all(ARGS.ticker)
        else:
            save_ticker(ARGS.ticker[0])
    else:
        TICKER_CSV_PATH = os.path.join(os.path.dirname(__file__), '../data/spy/tickers.csv')
        TICKERS = pd.read_csv(TICKER_CSV_PATH, header=None)[1]

        save_all(TICKERS)
        save_ticker('SPY')
        save_ticker('RSP')
