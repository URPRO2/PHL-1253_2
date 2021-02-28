"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
介绍如何将策略信号signal，转换成实际持仓pos
"""
import pandas as pd
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# ===导入数据
df = pd.read_hdf('/Users/xingbuxingx/Desktop/数字货币量化课程/2020版数字货币量化投资课程/xbx_coin_2020/data/signals.h5', key='df')


# ===由signal计算出实际的每天持有仓位
# 在产生signal的k线结束的时候，进行买入
df['signal'].fillna(method='ffill', inplace=True)
df['signal'].fillna(value=0, inplace=True)  # 将初始行数的signal补全为0
df['pos'] = df['signal'].shift()
df['pos'].fillna(value=0, inplace=True)  # 将初始行数