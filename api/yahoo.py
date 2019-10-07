import pandas as pd
import yfinance as yf
from datetime import date


def get_daily(ticker, start=None):
    if start == None:
        return yf.download(ticker, period='max', interval='1d')
    else:
        return yf.download(ticker, start=start, end=date.today(), interval='1d')


def get_info(ticker):
    t = yf.Ticker(ticker)
    info_dict = t.info
    info = pd.DataFrame.from_dict(info_dict, orient='index').iloc[:, 0].rename('Info')

    try:
        balance_sheet = t.balance_sheet
        financials = t.financials
        cashflow = t.cashflow
    except IndexError as e:
        print('ERROR:', ticker)
        print(e)
        return info

    balance_sheet = balance_sheet.iloc[:, 0]
    financials = financials.iloc[:, 0]
    cashflow = cashflow.iloc[:, 0]

    return_info = pd.concat([info, balance_sheet, financials, cashflow], axis=0)
    print(ticker)
    return return_info
