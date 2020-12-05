"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
获取各个交易所的账户持仓数据
"""
import pandas as pd
import ccxt
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# =====okex交易所
# ===创建交易所
exchange = ccxt.okex3()  # 此处是okex第三代api接口，所以是okex3
exchange.apiKey = ''
exchange.secret = ''
exchange.password