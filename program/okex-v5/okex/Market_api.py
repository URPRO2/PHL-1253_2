from .client import Client
from .consts import *


class MarketAPI(Client):

    def __init__(self, api_key, api_secret_key, passphrase, use_server_time=False, flag='1'):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag)

    # Get Tickers
    def get_tickers(self, instType, uly=''):
        params = {'instType': instType, 'uly': uly}
        return self._request_with_params(GET, TICKERS_INFO, params)

    # Get Ticker
    def get_ticker(self, instId):
        params = {'instId': instId}
        return self._request_with_params(GET, TICKER_INFO, params)

    # Get Index Tickers
    de