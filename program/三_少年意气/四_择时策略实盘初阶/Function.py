"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
择时策略实盘需要的相关函数
"""
import ccxt
import math
import time
import pandas as pd
from datetime import datetime, timedelta
import json
import requests
import time
import hmac
import hashlib
import base64
from urllib import parse
from multiprocessing import Pool
from functools import partial
from program.三_少年意气.四_择时策略实盘初阶.Config import *
from program.三_少年意气.四_择时策略实盘初阶.Signals import *


# =====okex交互函数
# ===通过ccxt、交易所接口获取合约账户信息
def ccxt_fetch_future_account(exchange, max_try_amount=5):
    """
    :param exchange:
    :param max_try_amount:
    :return:

 