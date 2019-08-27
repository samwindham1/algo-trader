# import sys
# sys.path.append('..')

import os
import pickle
import pandas as pd
from api import yahoo
from data.info import info


def download_info(ticker):
    return yahoo.get_info(ticker)


def download_all_info(tickers):
    info_dict = {}
    for i, ticker in enumerate(tickers):
        print(i, '-', ticker)
        info_t = download_info(ticker)
        info_dict[ticker] = info_t
    return info_dict


def save_info(info_dict):
    info.save(info_dict)


if __name__ == '__main__':
    ticker_csv_path = os.path.join(os.path.dirname(__file__), '../data/spy/tickers.csv')
    tickers = pd.read_csv(ticker_csv_path, header=None)[1]

    print('---- DOWNLOADING ----')
    info_dict = download_info(tickers)
    print('---- SAVING ----')
    save_info(info_dict)

    print('Done.')
