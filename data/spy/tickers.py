import os
import pandas as pd
import pandas_datareader.data as web

from datetime import datetime


class SpyTickers:
    def __init__(self):
        self.tickers = self.download()

    def download(self):
        self.ticker_csv_path = os.path.join(os.path.dirname(__file__), 'tickers.csv')
        try:
            tickers = pd.read_csv(self.ticker_csv_path, header=None)[1]
        except FileNotFoundError:
            data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
            table = data[0]
            tickers = pd.Series(table[1:][0].tolist())
            tickers.to_csv(self.ticker_csv_path)
            print("Tickers downloaded and saved.")
        return tickers
