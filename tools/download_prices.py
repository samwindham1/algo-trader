import os
import argparse
import pandas as pd

from api import yahoo


def save_ticker(ticker):
    historical = yahoo.get_daily(ticker)
    historical.to_csv(os.path.join(os.path.dirname(__file__), '../data/price/{ticker}.csv'.format(ticker=ticker)))


def save_all(tickers):
    for i, ticker in enumerate(tickers):
        print(i, '-', ticker)
        save_ticker(ticker)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-t', '--ticker', nargs='+')
    ARGS = PARSER.parse_args()

    if ARGS.ticker:
        save_all(ARGS.ticker)
    else:
        TICKER_CSV_PATH = os.path.join(os.path.dirname(__file__), '../data/spy/tickers.csv')
        TICKERS = pd.read_csv(TICKER_CSV_PATH, header=None)[1]

        save_all(TICKERS)
        save_ticker('SPY')
        save_ticker('RSP')
