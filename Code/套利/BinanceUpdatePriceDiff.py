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
    if '06' in symbol['symbol']:  # 目标合约时间 06代表6月当季
        quarterly_symbols_ID.append(symbol['symbol'])  # 获取币本位当季交易对
print(quarterly_symbols_ID)
while True:
    quarterly_symbols_price_list = []  # 初始化当季交易对的价格信息列表
    markPrice_indexPrice = exchange.dapiPublicGetPremiumIndex()  # 获取所有币本位合约的价格信息
    for price in markPrice_indexPrice:
        if price['symbol'] in quarterly_symbols_ID:
            quarterly_symbols_price_dict = price
            quarterly_symbols_price_dict['diff'] = (float(price['markPrice']) - float(price['indexPrice'])) / float(
                price['indexPrice'])  # (期货价格-现货价格)/现货价格
            quarterly_symbols_price_list.append(quarterly_symbols_price_dict)  # 获取当季交易对的价格信息
    df = pandas.DataFrame(quarterly_symbols_price_list)[['symbol', 'diff', 'markPrice', 'indexPrice']].sort_values(
        'diff')
    print(