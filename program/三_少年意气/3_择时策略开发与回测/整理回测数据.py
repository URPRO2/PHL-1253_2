"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
介绍如何批量导入一个文件夹中的所有数据
"""
import pandas as pd
import glob
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# 获取数据的路径
path = r'C:\Users\jan\Documents\GitHub\coin2021\data\spot'  # 改成电脑本地的地址
path_list = glob.glob(path + "/*/*.csv")  # python自带的库，获得某文件夹中所有csv文件的路径

# 筛选出指定币种和指定时间
symbol = 'BTC-USDT_5m'
path_list = list(filter(lambda x: symbol in x, path_list))

# 导入数据
df_list = []
for path in sorted(path_list):
    print(path)
    df = pd.read_csv(path, 