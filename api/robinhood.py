import os
import json

import pandas as pd

from fast_arrow import StockMarketdata, OptionChain, Option
from fast_arrow import Client as ClientLegacy
from fast_arrow_auth import Client, User


class Robinhood:
    def __init__(self):
        username, password, device_token = self.setup()
        self.username = username
        self.password = password
        self.device_token = device_token

    def setup(self):
        config_path = os.path.join(os.path.dirname(__file__), '../config.local.json')
        username = ''
        password = ''
        device_token = None
        with open(config_path) as config_file:
            config = json.load(config_file)
            username = config['robinhood']['username']
            password = config['robinhood']['password']
            device_token = config['robinhood']['device-token']
        return (username, password, device_token)

    def login(self):
        self.client = Client(
            username=self.username,
            password=self.password,
            device_token=self.device_token)
        self.result = self.client.authenticate()
        self.user = User.fetch(self.client)

        print("Authenticated successfully = {}".format(self.result))
        print("Account Url = {}".format(self.client.account_url))
        print("Account Id = {}".format(self.client.account_id))

        print("Username = {}".format(self.user["username"]))
        print()

        # Set client to legacy version for further use
        auth_data = self.client.gen_credentials()
        self.client = ClientLegacy(auth_data)
        return self.client

    def get_quote(self, symbol):
        return StockMarketdata.quote_by_symbol(self.client, symbol)

    def get_option_chain(self, symbol, stock):
        stock_id = stock["instrument"].split("/")[-2]
        return OptionChain.fetch(self.client, stock_id, symbol)

    def get_next_3_exp_options(self, option_chain):
        option_chain_id = option_chain["id"]
        expiration_dates = option_chain['expiration_dates']

        next_3_expiration_dates = expiration_dates[0:3]

        ops = Option.in_chain(self.client, option_chain_id, expiration_dates=next_3_expiration_dates)
        ops = Option.mergein_marketdata_list(client, ops)
        return ops


if __name__ == '__main__':
    rh = Robinhood()
    client = rh.login()

    symbol = 'TLT'

    stock = rh.get_quote(symbol)

    print("TLT Options:")
    option_chain = rh.get_option_chain(symbol, stock=stock)
    options = rh.get_next_3_exp_options(option_chain)

    op_df = pd.DataFrame(options, columns=options[0].keys())
    op_df = op_df[abs(pd.to_numeric(op_df['strike_price']) - pd.to_numeric(stock['last_trade_price'])) <= 2]
    display_columns = {'expiration_date': 'exp', 'strike_price': 'strike',
                       'adjusted_mark_price': 'mark', 'bid_price': 'bid', 'ask_price': 'ask',
                       'break_even_price': 'break_even', 'open_interest': 'open_interest',
                       'volume': 'volume', 'chance_of_profit_long': 'profit_%_long',
                       'chance_of_profit_short': 'profit_%_short', 'delta': 'delta',
                       'implied_volatility': 'implied_vol'}
    op_df = op_df.sort_values(['expiration_date', 'strike_price']).rename(columns=display_columns)
    op_df = op_df[display_columns.values()]
    print("Data:")
    print(op_df)
