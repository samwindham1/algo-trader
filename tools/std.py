import os
import argparse
import pandas as pd
import numpy as np


def std(ticker, length=250, usereturns=False):
    path = os.path.join(os.path.dirname(__file__), f'../data/price/{ticker}.csv')
    price = pd.read_csv(path, parse_dates=True, index_col='Date')['Adj Close'].rename('Price')
    s = price

    if usereturns:
        s = np.log(price).diff().iloc[1:]

    print(f'{ticker} ${price.iloc[-1]} ({length})' + (' [Using Returns]' if usereturns else ''))
    print('std:\t\t', round(s.iloc[-length:].std(), 5))


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('ticker', nargs=1)
    PARSER.add_argument('--length', nargs=1, type=int)
    PARSER.add_argument('-r', '--usereturns', action="store_true")
    ARGS = PARSER.parse_args()
    ARG_ITEMS = vars(ARGS)

    # Run
    STD_ARGS = {k: (v[0] if isinstance(v, list) else v) for k, v in ARG_ITEMS.items() if v is not None}

    # Run function with parsed arguments
    std(**STD_ARGS)
