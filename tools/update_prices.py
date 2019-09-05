import os
import argparse
from datetime import date, datetime, timedelta

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

    if last_date is not None:
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
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-t', '--ticker', nargs='+')
    ARGS = PARSER.parse_args()

    if ARGS.ticker:
        update_all(ARGS.ticker)
    else:
        DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/price/')
        FILE_LIST = os.listdir(DATA_PATH)
        TICKERS = [f[:-4] for f in FILE_LIST if os.path.isfile(os.path.join(DATA_PATH, f))]

        update_all(TICKERS)
