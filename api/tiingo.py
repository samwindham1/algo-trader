from datetime import date
from pandas_datareader import DataReader


class Tiingo:

    def __init__(self, tickers):
        self.Initialize(tickers)

    def Initialize(self, tickers):
        self.startDate = date(2018, 1, 1)
        self.endDate = date(2018, 12, 31)
        self.tickers = tickers
