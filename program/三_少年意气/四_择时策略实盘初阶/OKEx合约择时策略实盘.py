"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
介绍择时策略实盘
"""
import ccxt
from time import sleep
import pandas as pd
from datetime import datetime
from program.三_少年意气.四_择时策略实盘初阶.Function import *
from program.三_少年意气.四_择时策略实盘初阶.Config import *
pd.set_option('display.max_