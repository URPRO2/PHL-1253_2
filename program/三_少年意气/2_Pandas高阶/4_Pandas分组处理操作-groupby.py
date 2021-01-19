"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 本节课程内容
- groupby操作
- 计算大小
- 获取指定group
- 常见函数
- group内部计算
- 遍历group
"""

import pandas as pd

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

# =====导入数据
df = pd.read_csv(r'C:\Users\Simons\Desktop\xbx_coin_2020\data\cls-3.2BITFINEX-1H-data-20180124.csv', skiprows=1)


# =====groupby常用操作汇总
# 根据'candle_begin_time'进行group，将相同'交易日期'的行放入一个group，
# print(df.groupby('candle_begin_time'))  # 生成一个group对象。不会做实质性操作，只是会判断是否可以根据该变量进行groupby

# group后可以使用相关函数，size()计算每个group的行数
# print(df.groupby('candle_begin_time').size())  # 每小时交易的币的个数
# 根据'symbol'进行group，将相同'symbol'的行放入一个group，
# print(df.groupby('symbol').size())  # 每个币交易的小时数


# 获取其中某一个group
# print(df.