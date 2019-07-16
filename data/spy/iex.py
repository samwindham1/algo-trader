import json
import os
import requests
from urllib.parse import urlparse

IEX_TOKEN = ''
API_ENDPOINT = ''

config_path = os.path.join(os.path.dirname(__file__), '../../config.local.json')
with open(config_path) as config_file:
    config = json.load(config_file)
    IEX_TOKEN = config['iex-cloud-api-token-test']
    # set to sandbox, use real endpoint once configured
    API_ENDPOINT = config['iex-api-endpoint-sandbox']


def dailyHistorical(ticker, range):
    print('Retrieving data for: {0}'.format(ticker))
    url = API_ENDPOINT + '/stock/' + ticker + '/chart/' + range
    resp = requests.get(urlparse(url).geturl(), params={
        'token': IEX_TOKEN,
        'chartCloseOnly': True
    })
    if resp.status_code == 200:
        return resp.json()
    raise Exception('Response %d - ' % resp.status_code, resp.text)
