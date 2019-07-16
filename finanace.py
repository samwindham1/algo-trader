import os
import json
import pandas as pd

from api.yahoo import YahooFinanceHistory

ticker_csv_path = os.path.join(os.path.dirname(__file__), 'data/spy/tickers.csv')
tickers = pd.read_csv(ticker_csv_path, header=None)[1]

aapl = YahooFinanceHistory('AAPL').get_quote()

print(aapl.head())
aapl.to_csv(os.path.join(os.path.dirname(__file__), 'data/spy/historical/aapl.csv'))
