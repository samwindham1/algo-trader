import os
import pickle
import pandas as pd

PATHS = {
    'BALANCE': './us-balance-quarterly.csv',
    'CASHFLOW': './us-cashflow-quarterly.csv',
    'INCOME': './us-income-quarterly.csv'
}


def load(path='./info.p'):
    info_path = os.path.join(os.path.dirname(__file__), path)

    with open(info_path, 'rb') as f:
        info = pickle.load(f)
        return info


def save(info, path='./info.p'):
    info_path = os.path.join(os.path.dirname(__file__), path)
    with open(info_path, 'wb') as f:
        pickle.dump(info, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_file(info_type):
    return pd.read_csv(os.path.join(os.path.dirname(__file__), PATHS[info_type]), sep=';')


def load_info(info_type, ticker, date=None):
    data = load_file(info_type)
    t_data = data[data.Ticker == ticker]

    if date is None:
        return t_data
    else:
        row_label = (pd.to_datetime(t_data['Report Date']) > date).idxmax()
        return t_data.loc[row_label]


def balance(ticker, date=None):
    return load_info('BALANCE', ticker, date)


def all_balance(tickers=None):
    data = load_file('BALANCE')
    if tickers:
        return data[data.Ticker.isin(tickers)]
    return data


def cashflow(ticker, date=None):
    return load_info('CASHFLOW', ticker, date)


def income(ticker, date=None):
    return load_info('INCOME', ticker, date)


def all_info(ticker=None):
    if ticker is None:
        info = pd.concat([load_file('BALANCE'), load_file('CASHFLOW'), load_file('INCOME')], axis=1)
        return info.loc[:, ~info.columns.duplicated()]
    else:
        info = pd.concat([balance(ticker), cashflow(ticker), income(ticker)], axis=1)
        return info.loc[:, ~info.columns.duplicated()]
