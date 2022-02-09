import os
import pandas as pd


class Universe:
    def __init__(self, assets=None):
        self.assets = assets

    def _read_csv(self, path):
        ticker_csv_path = os.path.join(os.path.dirname(__file__), path)
        tickers = pd.read_csv(ticker_csv_path, header=None)[1]
        return list(tickers)


class SP500(Universe):
    def __init__(self):
        tickers = self._read_csv('../../data/spy/tickers.csv')
        exclude = self._read_csv('../../data/info/exclude.csv')
        tickers = [t for t in tickers if t not in exclude]
        super().__init__(tickers)


class FAANG(Universe):
    def __init__(self):
        tickers = ['FB', 'AAPL', 'AMZN', 'NFLX', 'GOOG']
        super().__init__(tickers)


class SP500_TECH(Universe):
    def __init__(self):
        tickers = self._read_csv('../../data/spy/sp500-tech.csv')
        exclude = self._read_csv('../../data/info/exclude.csv')
        tickers = [t for t in tickers if t not in exclude]
        super().__init__(tickers)


class SP100(Universe):
    def __init__(self):
        tickers = self._read_csv('../../data/spy/sp100.csv')
        exclude = self._read_csv('../../data/info/exclude.csv')
        tickers = [t for t in tickers if t not in exclude]
        super().__init__(tickers)


def get(universe):
    return UNIVERSE_DICT[universe]


UNIVERSE_DICT = {
    'sp500': SP500,
    'faang': FAANG,
    'sp500_tech': SP500_TECH,
    'sp100': SP100
}
