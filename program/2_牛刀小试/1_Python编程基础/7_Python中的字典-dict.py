
"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- 字典介绍
- 字典常见操作

功能：本程序主要介绍python的常用内置数据结果，如list、dict、str等。希望以后大家只要看这个程序，就能回想起相关的基础知识。
"""

# =====dict介绍
# 使用{}大括号就可以新建一个dict。[]
# dict_var = {}  # 这是一个空dict
# print(dict_var, type(dict_var))

# # 具有一系列成对的对象。一个叫做key，一个叫做value。其中的元素(包括key和value)不需要是同类型
# dict_var = {
#     'btc': '比特币',
#     'eth': '以太坊',
#     'xrp': '瑞波币'
# }  # 其中'btc'、'eth'、'xrp'就是key，'比特币'、'以太坊'、'瑞波币'就是相对应的value。
# print(dict_var)

# 字典是无顺序，key不可重复
# print(dict_var[0])  # 因为没有顺序，所以dict_var[0]并不能取出第0个位置的元素，此处会报错。
