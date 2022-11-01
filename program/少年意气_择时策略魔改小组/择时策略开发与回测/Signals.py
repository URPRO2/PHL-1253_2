"""
《邢不行-2020新版|Python数字货币量化投资课程》
择时策略魔改研究小组（第1期）
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9585
本程序作者: 邢不行
"""
import pandas as pd
import numpy as np


# =====简单布林策略
# 策略
def signal_simple_bolling(df, para=[200, 2]):
    """
    :param df:
    :pa