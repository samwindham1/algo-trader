import pandas as pd
import yfinance as yf
from datetime import date


def get_daily(ticker, start=None):
    if start == None:
        return yf.download(ticker, period='max', interval='1d')
    else:
        return yf.download(ticker, start=start, end=date.today(), interval='1d')


def get_info(ticker):
    return yf.Ticker(ticker).info
