# import sys
# sys.path.append('..')

import os
import pickle
import pandas as pd
from api import yahoo
from data.info import info


def save_info(tickers):
    info_dict = {}
    for i, ticker in enumerate(tickers):
        print(i, '-', ticker)
        info_t = yahoo.get_info(ticker)
        info_dict[ticker] = info_t

    print('---- SAVING ----')
    info.save(info_dict)
    print('Done.')


if __name__ == '__main__':
    ticker_csv_path = os.path.join(os.path.dirname(__file__), '../data/spy/tickers.csv')
    tickers = pd.read_csv(ticker_csv_path, header=None)[1]

    save_info(tickers)
