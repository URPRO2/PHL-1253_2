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

# 获取最新的ticker数据，运行需