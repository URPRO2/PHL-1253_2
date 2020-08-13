"""
自动更新 期现价差
"""
import pandas
import time
import datetime
import ccxt

time_interval = 5  # 数据抓取间隔时间
diff_target = 0.08  # 目标开仓期现价差 0.08代表8%价差
exchange = ccxt.binance()
symbols = exchange.dapiPublicGetExchangeInfo()['symbols']  # 币本位所有交易对

quarterly_symbols_ID = []  # 初始化当季交易对
for symbol in symbols:
    if '06' in symbol['symb