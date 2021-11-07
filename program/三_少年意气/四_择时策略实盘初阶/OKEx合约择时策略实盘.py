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
pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


# 测试时ccxt版本为1.27.28。若不是此版本，可能会报错，可能性很低。print(ccxt.__version__)可以查看ccxt版本。

# =====配置运行相关参数=====

# =执行的时间间隔
time_interval = '15m'  # 目前支持5m，15m，30m，1h，2h等。得okex支持的K线才行。最好不要低于5m

# =钉钉
# 在一个钉钉群中，可以创建多个钉钉机器人。
# 建