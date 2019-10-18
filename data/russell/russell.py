import os
import pandas as pd
import numpy as np

from ..info import info as info_tool


def small_cap():
    # get small-cap tickers
    ticker_csv_path = os.path.join(os.path.dirname(__file__), './small_cap.csv')
    df = pd.read_csv(ticker_csv_path).set_index('Ticker')

    # load info
    info = info_tool.load('./small_cap.p')

    # get columns
    column_csv_path = os.path.join(os.path.dirname(__file__), '../info/columns.csv')
    info_columns = pd.read_csv(column_csv_path, header=None, index_col=0)[1].rename('info_columns')

    # convert info into DataFrame
    info_df = pd.DataFrame.from_dict(info, orient='index')[list(info_columns)]

    # calculate extra fundamentals
    info_df['turnover'] = info_df['averageDailyVolume3Month'] / info_df['sharesOutstanding']
    info_df['debtToEquity'] = (pd.to_numeric(info_df['Total Liabilities']) /
                               pd.to_numeric(info_df["Total stockholders' equity"]))
    info_df['returnOnEquity'] = (pd.to_numeric(info_df['Net Income']) /
                                 pd.to_numeric(info_df["Total stockholders' equity"]))
    info_df['priceToRevenue'] = (pd.to_numeric(info_df['marketCap']) /
                                 pd.to_numeric(info_df['Total Revenue']))

    # filter low-liquid stocks
    df_filter = (
        info_df['marketCap'] > 100000
    ) & (
        info_df['averageDailyVolume3Month'] > info_df['averageDailyVolume3Month'].quantile(0.05)
    ) & (
        info_df['turnover'] < info_df['turnover'].quantile(.95)
    ) & (
        info_df['trailingAnnualDividendYield'] > 0
    ) & (
        info_df['trailingPE'] <= 20
    ) & (
        info_df['forwardPE'] <= 25
    ) & (
        info_df['epsForward'] > 0
    ) & (
        info_df['priceToBook'] <= 3
    ) & (
        info_df['debtToEquity'] <= 2
    ) & (
        info_df['returnOnEquity'] >= .1
    )

    info_df = info_df[df_filter]
    info_df.to_csv(os.path.join(os.path.dirname(__file__), 'small_cap_filtered.csv'))

    return info_df


if __name__ == '__main__':
    small_cap()
