"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
并行遍历参数，查看每个参数的结果
"""
import pandas as pd
from datetime import timedelta
from multiprocessing.pool import Pool
from datetime import datetime
from Signals import *
from Position import *
from Evaluate import *
pd.set_option('expand_frame_re