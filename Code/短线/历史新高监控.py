
import pandas as pd
import os, sys
import ccxt
import time
import datetime

if sys.platform != 'win32':
    sys.path.append('/root/coin2021')
import Code.base.Tool as tool
import Code.base.wechat as wechat
from Code.Function import *
from Code.config.configLoad import *
#  ======参数=======

wx = wechat.WeChat()


class CoinNewHighMgr:
    def __init__(self):
        self.ex = ccxt.binance()
        self.ex.apiKey = apiKey3266
        self.ex.secret = secret3266
        self.bias_pct = 0.01  # 低于这个阈值挂单
        if os.path.isfile('highPrice.csv'):
            self.df = pd.read_csv('highPrice.csv', encoding='gbk', index_col='symbol')
        else:
            self.df = self.onInitHighPrice(self.getSymbols())
            self.df.to_csv('highPrice.csv', encoding='gbk')

    def onInitHighPrice(self, symbolList):
        lst = []
        for symbol in symbolList:
            obj = self.ex.fetch_ohlcv(symbol, timeframe='3d', limit=1440)
            df = pd.DataFrame(obj, dtype=float)
            df[0] = pd.to_datetime(df[0], unit='ms')  # 整理时间
            max = df[2].max()
            last = df.iat[-1, 4]
            df.sort_values(by=[2], inplace=True)
            maxTime = df.iat[-1, 0]
            lst.append([symbol, max, maxTime])
            time.sleep(.3)
        df = pd.DataFrame(lst, columns=['symbol', 'max', 'maxTime'])
        df.set_index('symbol', inplace=True)
        return df

    def getSymbols(self):
        tickers = self.ex.fetch_tickers()