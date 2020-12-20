from .client import Client
from .consts import *


class AccountAPI(Client):

    def __init__(self, api_key, api_secret_key, passphrase, use_server_time=False, flag='1'):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag)

    # Get Balance
    def get_account(self, ccy=''):
        params = {}
        if ccy:
            params['ccy'] = ccy
        return self._request_with_params(GET, ACCOUNT_INFO, params)

    # Get Positions
    def get_positions(self, instType='', instId=''):
        params = {'instType': instType, 'instId': instId}
        return self._request_with_params(GET, POSITION_INFO, params)

    # Get Bills Details (recent 7 days)
    def get_bills_detail(self, instType='', ccy='', mgnMode='', ctType='', type='', subType='', after='', before='',
                         limit=''):
        params = {'instType': instType, 'ccy': ccy, 'mgnMode': mgnMode, 'ctType': ctType, 'type': type,
                  'subType': subType, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, BILLS_DETAIL, params)

    # Get Bills Details (recent 3 months)
    def get_bills_details(self, instType='', ccy='', mgnMode='', ctType='', type='', subType='', after='', before='',
                          limit=''):
        params = {'instType': instType, 'ccy': ccy, 'mgnMode': mgnMode, 'ctType': ctType, 'type': type,
                  'subType': subType, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, BILLS_ARCHIVE, params)

    # Get Account Configuration
    def get_account_config(self):
        return self._request_without_params(GET, ACCOUNT_CONFIG)

    # Get Account Configuration
    def get_position_mode(self, posMode):
        params = {'posMode': posMode}
        return self._request_with_params(POST, POSITION_MODE, params)

    # Get Account Configuration
    def set_leverage(self, lever, mgnMode, instId='', ccy='', posSide=''):
        params = {'lever': lever, 'mgnMode': mgnMode, 'instId': instId, 'ccy': ccy, 'posSide': posSide}
        return self._request_with_params(POST, SET_LEVERAGE, params)

    # Get Maximum Tradable Size For Instrument
    def get_maximum_trade_size(self, instId, tdMode, ccy='', px=''):
        params = {'instId': instId, 'tdMode': tdMode, 'ccy': ccy, 'px': px}
        return self._request_with_params(GET, MAX_TRADE_SIZE, params)

    # Get Maximum Available Tradable Amount
    def get_max_avail_size(self, instId, tdMode, ccy='', reduceOnly=''):
        params = {'instId': instId, 'tdMode': tdMode, 'ccy': ccy, 'reduceOnly': reduceOnly}
        return self._request_with_params(GET, MAX_AVAIL_SIZE, params)

    # Increase / Decrease margin
    def Adjustment_margin(self, instId, posSide, type, amt):
        params = {'instId': instId, 'posSide': posSide, 'type': type, 'amt': amt}
        return self._request_with_params(