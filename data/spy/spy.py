import os
import pandas as pd
import pandas_datareader.data as web

from concurrent import futures
from datetime import datetime

from data.spy.tickers import SpyTickers


if __name__ == '__main__':
    # get tickers from wikipedia
    spyTickers = SpyTickers()
