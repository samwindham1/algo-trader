import unittest
from datetime import datetime
import pandas as pd

from .info import load_info, balance, cashflow, income, all_info

class TestInfo(unittest.TestCase):

    def test_load_info(self):
        df = load_info('BALANCE', 'AAPL')
        self.assertEqual(list(df.columns)[18], 'Total Assets')
        self.assertEqual(type(df), pd.DataFrame)

        df = load_info('CASHFLOW', 'AAPL')
        self.assertEqual(list(df.columns)[-1], 'Net Change in Cash')

        df = load_info('INCOME', 'AAPL')
        self.assertEqual(list(df.columns)[-2], 'Net Income')

        df = load_info('BALANCE', 'AAPL', datetime(2016, 1, 1))
        self.assertEqual(type(df), pd.Series)

    def test_balance(self):
        df = balance('AAPL')
        self.assertEqual(df.iloc[0]['Report Date'], '2000-06-30')
        self.assertEqual(df.iloc[0]['Total Assets'], 6803000000)

        s = balance('AAPL', datetime(2016, 1, 1))
        self.assertEqual(s['Report Date'], '2016-03-31')
        self.assertEqual(s['Total Assets'], 305277000000)

    def test_cashflow(self):
        df = cashflow('AAPL')
        self.assertEqual(df.iloc[0]['Report Date'], '2000-06-30')
        self.assertEqual(df.iloc[0]['Net Change in Cash'], -318000000)

        s = cashflow('AAPL', datetime(2016, 1, 1))
        self.assertEqual(s['Report Date'], '2016-03-31')
        self.assertEqual(s['Net Change in Cash'], 4825000000)

    def test_income(self):
        df = income('AAPL')
        self.assertEqual(df.iloc[0]['Report Date'], '2000-06-30')
        self.assertEqual(df.iloc[0]['Net Income'], 200000000)

        s = income('AAPL', datetime(2016, 1, 1))
        self.assertEqual(s['Report Date'], '2016-03-31')
        self.assertEqual(s['Net Income'], 10516000000)

    def test_all_info(self):
        df = all_info()
        self.assertEqual(len(df.Ticker.unique()), 2080)

        df = all_info('AAPL')
        self.assertEqual(len(df), 78)
