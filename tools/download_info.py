import os
import asyncio
import pandas as pd
from api import yahoo
from data.info import info


async def download_info(ticker):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, yahoo.get_info, ticker)


def download_all_info(tickers):
    # create new event loop
    event_loop = asyncio.new_event_loop()

    # create all co-routines and tasks
    coroutines = [download_info(t) for t in tickers]
    tasks = [event_loop.create_task(c) for c in coroutines]

    # run event loop concurrently
    print("Tasks created, running event loop:")
    event_loop.run_until_complete(asyncio.wait(tasks))

    # get results
    info_dict = {ticker: task.result() for (ticker, task) in zip(tickers, tasks)}
    event_loop.close()

    return info_dict


def save_info(info_dict):
    info.save(info_dict)


if __name__ == '__main__':
    ticker_csv_path = os.path.join(os.path.dirname(__file__), '../data/spy/tickers.csv')
    tickers = pd.read_csv(ticker_csv_path, header=None)[1]

    print('---- DOWNLOADING ----')
    info_dict = download_info(tickers)
    print('---- SAVING ----')
    save_info(info_dict)

    print('Done.')
