import os
import pandas as pd
from datetime import date, datetime, timedelta
import dateutil.parser

from api import yahoo
from tools.log import log


def get_last_date(file_path):
    with open(file_path, 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        last_line = f.readline().decode()
        return datetime.strptime(last_line[:10], '%Y-%m-%d').date()


def update_ticker(ticker):
    file_path = os.path.join(os.path.dirname(__file__), '../data/price/{ticker}.csv'.format(ticker=ticker))
    last_date = None
    try:
        last_date = get_last_date(file_path)
    except OSError as e:
        print('!!! Read error.')
        log.log(type(e).__name__, e)
    except ValueError as e:
        print('!!! Invalid date format.')
        log.log(type(e).__name__, e)

    if last_date == date.today() - timedelta(days=1):
        return

    if last_date != None:
        historical = yahoo.get_daily(ticker, last_date)
        historical = historical[historical.index > last_date.strftime('%Y-%m-%d')]
        historical.to_csv(file_path, mode='a', header=False)
    else:
        historical = yahoo.get_daily(ticker, last_date)
        historical.to_csv(file_path)


def update_all(tickers):
    for i, ticker in enumerate(tickers):
        print(i, '-', ticker)
        update_ticker(ticker)


if __name__ == '__main__':
    ticker_csv_path = os.path.join(os.path.dirname(__file__), '../data/spy/tickers.csv')
    tickers = pd.read_csv(ticker_csv_path, header=None)[1]

    update_all(tickers)
    update_ticker('SPY')  # S&P index
    update_ticker('RSP')  # S&P index (equal-weighted)
    update_ticker('%5ETNX')  # 10y treasury bond yield
