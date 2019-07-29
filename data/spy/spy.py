import os
import pandas as pd
import pandas_datareader.data as web

from concurrent import futures
from datetime import datetime

from tickers import SpyTickers

# get tickers from wikipedia
spyTickers = SpyTickers().download()
