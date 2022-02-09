import os
import pandas as pd


def print_err(message, note=None):
    if note:
        print('!!!', message, note)
    else:
        print('!!!', message)


def validate(tickers):
    for ticker in tickers:
        try:
            d = pd.read_csv(DATA_PATH + ticker + '.csv', index_col=0, parse_dates=True)
            write_data = False
            if len(d) < 2:
                print_err(ticker, '(empty)')

            if (d.dtypes == object).any():
                print_err(ticker, '(bad dtype)')

            if (abs(d['Adj Close']) <= 1E-8).any():
                print_err(ticker, '(0 Adj Close)')
                zero_values = abs(d['Adj Close']) <= 1E-8
                print(d.loc[zero_values])
                d.loc[zero_values, 'Adj Close'] = d.loc[zero_values, 'Close']
                write_data = True

            if d.isnull().any(axis=1).any():
                print_err(ticker, '(null)')
                d = d.interpolate(method='time')
                write_data = True

            if write_data:
                print_err('writing...')
                d.to_csv(DATA_PATH + ticker + '.csv')

        except Exception as e:
            print_err(e)
    print('done.')


if __name__ == '__main__':
    print('loading files...')
    DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/price/')
    FILE_LIST = os.listdir(DATA_PATH)
    TICKERS = [f[:-4] for f in FILE_LIST if os.path.isfile(os.path.join(DATA_PATH, f))]

    print('loaded.')
    print('validating data...')
    validate(TICKERS)
