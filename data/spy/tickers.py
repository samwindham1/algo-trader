import os
import pandas as pd
import pandas_datareader.data as web

from datetime import datetime


class SpyTickers:
    def __init__(self):
        self.tickers = self.download()

    def download(self):
        print('Downloading S&P 500 members...')
        self.ticker_csv_path = os.path.join(os.path.dirname(__file__), 'tickers.csv')
        try:
            print('tickers.csv found. Nothing downloaded.')
            tickers = pd.read_csv(self.ticker_csv_path, header=None)[1]
        except FileNotFoundError:
            print('No tickers.csv file...')
            data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
            table = data[0]
            tickers = table.iloc[1:, 0].tolist()
            tickers = pd.Series([t.replace('.', '-') for t in tickers])
            tickers.to_csv(self.ticker_csv_path, header=False)
            print("Tickers downloaded and saved.")
        return tickers
