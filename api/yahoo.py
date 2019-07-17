import pandas as pd
import yfinance as yf


def get_daily(ticker):
    return yf.download(ticker, period="max", interval="1d")
