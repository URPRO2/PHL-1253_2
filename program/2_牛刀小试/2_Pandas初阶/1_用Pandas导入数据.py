"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- 原始数据介绍
- 如何使用pandas导入数据
- DataFrame数据结构介绍
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

# =====导入数据
df = pd.read_csv(
    # 该参数为数据在电脑中的路径，
    # 要注意字符串转义符号 \ ，可以使用加r变为raw string或者每一个进行\\转义
    filepath_or_buffer=r'../../../data/OKEX_20200302_5T.csv',
    # 编码格式，不同的文件有不同的编码方式，一般文件中