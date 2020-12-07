
import datetime
import base64
import hmac
from hashlib import sha256
import time
import math
import json
import requests
from urllib import parse
import pandas as pd

from configLoad import *
import Signals
import okex.Trade_api as Trade
tradeAPI = Trade.TradeAPI(apiKey, secret, password, False, '1')

# baseUrl = 'http://www.okex.com/' # 服务器用这个域名
baseUrl = 'http://www.okex.vip/'


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
}

session = requests.session()  # 利用session记录每次请求的cookie，加快请求获取数据速度


def getPrivateHeaders(requestPath, requestMethod):
    """
    okex sign生成方式：
    OK-ACCESS-SIGN的请求头是对timestamp + method + requestPath + body字符串（+表示字符串连接），以及SecretKey，
    使用HMAC SHA256方法加密，通过Base-64编码输出而得到的。

    如：sign=CryptoJS.enc.Base64.Stringify(CryptoJS.HmacSHA256(timestamp + 'GET' + '/users/self/verify', SecretKey))

    其中，timestamp的值与OK-ACCESS-TIMESTAMP请求头相同，为ISO格式，如2020-12-08T09:08:57.715Z。
    :param urlAddress:
    :param requestMethod: 'GET/POST'
    :return:
    """
    timestamp = str(datetime.datetime.utcnow().replace(microsecond=0).isoformat()) + '.715Z'
    headers = {
        'Content-Type':'application/json',
        'OK-ACCESS-KEY': apiKey,
        'OK-ACCESS-SIGN': get_hmac_sha256(timestamp + requestMethod + requestPath, secret),
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': password,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'x-simulated-trading': '1'  # 模拟盘需要加这个参数，实盘得去掉该参数
    }
    return headers


# ===通过交易所V5接口获取合约账户信息
def fetch_future_account(max_try_amount=5):
    """
    :param max_try_amount:最大尝试次数
    :return:

    逐仓：

        1.账户权益=账户余额+逐仓仓位账户余额+所有合约的已实现盈亏+所有合约的未实现盈亏

        2.可用保证金=账户余额+逐仓仓位账户余额+本合约已实现盈亏- 当前仓位的持仓所需保证金 - 挂单冻结保证金

    """
    for _ in range(max_try_amount):
        try:
            getFuturePositionUrl = baseUrl+'api/v5/account/balance?ccy=USDT'
            future_info = session.get(getFuturePositionUrl, headers=getPrivateHeaders('/api/v5/account/balance?ccy=USDT', 'GET'), timeout=3).json()['data']
            # 交易的是usdt本位保证金合约，因此这里用统一账户的usdt保证金余额来做可用保证金
            # isoEq		美金层面逐仓仓位权益
            # availEq	可用保证金

            for ccyMsg in future_info[0].get('details'):
                if ccyMsg.get('ccy') == 'USDT':
                    # 返回两个值，账户总权益和可用保证金
                    return float(ccyMsg.get('disEq', 0)), float(ccyMsg.get('availEq', 0))
            # 如果没查询到那么就返回0
            return 0,0
        except Exception as e:
            print('通过ccxt的通过futures_get_accounts获取所有合约账户信息，失败，稍后重试：\n', e)
            time.sleep(medium_sleep_time)

    _ = '通过ccxt的通过futures_get_accounts获取所有合约账户信息，失败次数过多，程序Raise Error'
    send_dingding_and_raise_error(_)


def fetch_future_position(max_try_amount=5):
    """
    :param exchange:
    :param max_try_amount:
    :return:
    本程序使用okex3中“交割合约API”、“所有合约持仓信息”接口，获取合约账户所有合约的持仓信息。

    """
    for _ in range(max_try_amount):
        try:
            getFuturePositionUrl = baseUrl+'api/v5/account/positions#instType=FUTURES'
            future_info = \
            session.get(getFuturePositionUrl, headers=getPrivateHeaders('/api/v5/account/positions', 'GET'),
                         timeout=3).json()['data']
            return future_info
        except Exception as e:
            print('通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败，稍后重试。失败原因：\n', e)
            time.sleep(medium_sleep_time)

    _ = '通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败次数过多，程序Raise Error'
    send_dingding_and_raise_error(_)


def update_symbol_info(symbol_info, symbol_config):
    """
        :param exchange:
        :param max_try_amount:
        :return:

        没考虑到同时持有反方向合约时候的错误情况
        """
    isoEquity,_ = fetch_future_account()  # 获取当前的账户权益信息
    # 将账户信息和symbol_info合并

    symbol_info['账户权益'] = isoEquity

    futurePositionMsgList = fetch_future_position()
    # futurePositionMsgDf.index = futurePositionMsgDf['instId']

    if futurePositionMsgList:
        # 去除无关持仓：账户中可能存在其他合约的持仓信息，这些合约不在symbol_config中，将其删除。
        for symbol in symbol_config.keys():
            for futureMsg in futurePositionMsgList:
                # 如果目标持仓合约的代码和返回实际持仓代码信息一致，那么我们将数据读入进来
                # ['账户权益', '持仓方向', '持仓量', '持仓收益率', '持仓收益', '持仓均价', '当前价格', '最大杠杆']
                if symbol_config[symbol].get('instrument_id') == futureMsg.get('instId'):
                    # 账户持仓量
                    symbol_info.loc[symbol, '持仓量'] = futureMsg.get('pos')

                    # 最大杠杆
                    symbol_info.loc[symbol, '最大杠杆'] = futureMsg.get('lever')

                    # 当前价格
                    symbol_info.loc[symbol, '当前价格'] = futureMsg.get('last')

                    # 持仓均价
                    symbol_info.loc[symbol, '持仓均价'] = futureMsg.get('avgPx')

                    # 持仓收益
                    symbol_info.loc[symbol, '持仓收益'] = futureMsg.get('upl')

                    # 持仓收益率
                    symbol_info.loc[symbol, '持仓收益'] = futureMsg.get('upl')

                    # 持仓方向，如果同时持有两个方向的合约那么，程序报错

                    symbol_info.loc[symbol, '持仓收益率'] = futureMsg.get('uplRatio')

                    # 账户持仓量
                    posSide = 1 if futureMsg.get('posSide') == 'long' else -1
                    # 如果已经持有同种合约的仓位，那么程序可能存在问题，程序报错退出程序
                    if type(symbol_info.loc[symbol, '持仓方向']) == type(1):
                        print('同时持有两份相同合约，请检查程序！')
                        exit()
                    symbol_info.loc[symbol, '持仓方向'] = posSide
        symbol_info['持仓方向'].fillna(value=0, inplace=True)

    else:
        # 当future_position为空时，将持仓方向的控制填充为0，防止之后判定信号时出错
        symbol_info['持仓方向'].fillna(value=0, inplace=True)

    return symbol_info


# ===通过V5api获取K线数据
def fetch_candle_data( symbol, time_interval, limit, max_try_amount=5):
    """
    本程序使用ccxt的fetch_ohlcv()函数，获取最新的K线数据，用于实盘
    :param exchange:
    :param symbol:
    :param time_interval:
    :param limit:
    :param max_try_amount:
    :return:
    """
    for _ in range(max_try_amount):
        try:
            # 获取数据
            klineUrl = baseUrl+'api/v5/market/candles?instId={symbol}&bar={bar}&limit={limit}'.format(
                symbol=symbol, bar=time_interval,limit = limit)
            data = session.get(klineUrl,headers=headers,timeout=1).json()['data']
            # 整理数据
            df = pd.DataFrame(reversed(data), dtype=float)
            df.rename(columns={0: 'MTS', 1: 'open', 2: 'high',
                               3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
            df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')
            df['candle_begin_time_GMT8'] = df['candle_begin_time'] + datetime.timedelta(hours=8)
            df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]
            return df
        except Exception as e:
            print('获取fetch_ohlcv获取合约K线数据，失败，稍后重试。失败原因：\n', e)
            time.sleep(short_sleep_time)

    _ = '获取fetch_ohlcv合约K线数据，失败次数过多，程序Raise Error'
    send_dingding_and_raise_error(_)
