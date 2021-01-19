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
df = pd.read_csv(r'C:\Users\Simons\Desktop\xbx_coin_2020\data\cls-3.2BITFINEX-1H-data-