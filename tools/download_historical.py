import os
import pandas as pd
import argparse

from api import yahoo


def save_ticker_historical(ticker):
    historical = yahoo.get_daily(ticker)
    historical.to_csv(os.path.join(os.path.dirname(__file__), '../data/price/{ticker}.csv'.format(ticker=ticker)))


def save_all_historical(tickers):
    for i, ticker in enumerate(tickers):
        print(i, '-', ticker)
        save_ticker_historical(ticker)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--ticker', nargs='+')
    args = parser.parse_args()

    if args.ticker:
        save_all_historical(args.ticker)
    else:
        ticker_csv_path = os.path.join(os.path.dirname(__file__), '../data/spy/tickers.csv')
        tickers = pd.read_csv(ticker_csv_path, header=None)[1]

        save_all_historical(tickers)
        save_ticker_historical('SPY')
        save_ticker_historical('RSP')
