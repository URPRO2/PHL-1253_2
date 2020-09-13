"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

介绍数字货币定投的简单策略
"""
import pandas as pd  # 第三方库，专门用于数据分析，处理表格数据
pd.set_option('expand_frame_repr', False)  # 照抄即可，不求甚解


# ===读取数据
df = pd.read_csv('EOSUSD_1D.csv',  # 此处为数据文件地址，请自行修改为本电脑的地址
                 skiprows=1,  # 跳过第一行数据
                 )
# print(df)  # 将数据打印出来查看，head，sample，
df = df[['candle_begin_time', 'close']]  # 选取特定的几列

# ===选取时间段
# df = df[df['candle_begi