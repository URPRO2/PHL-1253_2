"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

介绍数字货币如何自动交易
"""
import ccxt
import time

# ===获取行情数据
# 申明okex交易所
# exchange = ccxt.okex3()

# 获取最新的ticker数据，运行需要翻墙，btc、ltc
# data = exchange.fetchTicker(symbol='BTC/USDT')
# 获取最新的K线数据：日线、小时线
# data = exchange.fetch_ohlcv(symbol='BTC/USDT', timeframe='1h', limit=50)  # '1h'，'1d'

# 获取币安交易所的相关数据
# exchange = ccxt.binance()
# data = exchange.fetchTicker(symbol='BTC/USDT')

# ===下单交易
# 申明币安交易所
exchange = ccxt.binance()
# 填写API秘钥
exchange.apiKey = ''
exchange.secret = ''

# 获取账户余额
balance = exchange.fetch_balance()

# 限价单卖出：交易对、买卖数量、价格。如何买？
# order_info = exchange.create_limit_sell_order('BTC/USDT', 0.01, 13000)

# 撤单
# order_info = exchange.cancel_order(id='486207276', symbol='BTC/USDT')

# ===完整案例程序1：反复下单、撤单
# while True:
#     order_info = exchange.create_limit_sell_order('BTC/USDT', 0.01, 14000)
#     print('下单完成')
#     time.sleep(2)
#     order_info = exchange.cancel_order(id=order_info['id'], symbol='BTC/USDT')
#     print('撤单完成')
#     time.sleep