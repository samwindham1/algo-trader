import os
import pandas as pd
import pandas_datareader.data as web

from concurrent import futures
from datetime import datetime

import iex

from tickers import SpyTickers

# get tickers from wikipedia
spyTickers = SpyTickers().download()

# set up dates (5 years ago to today)
end = datetime.now()
start = datetime(end.year - 5, end.month, end.day)
bad = []


def getHistorical(ticker):
    data = iex.dailyHistorical(ticker, '5y')
    df = pd.DataFrame(data)
    df.to_csv(f"data/spy/historical/{ticker}.csv")

###
# Runs historical download concurrently.
# Currently configured for test data.
# !!!!! IMPORTANT !!!!!
# check configuration to ensure test data and not production data ($$$)
###
# with futures.ThreadPoolExecutor(50) as executer:
#     res = executer.map(getHistorical, list(tickers))
