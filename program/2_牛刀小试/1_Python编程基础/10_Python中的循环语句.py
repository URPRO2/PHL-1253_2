
"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- range函数
- for循环语句
- while循环语句

功能：本程序主要介绍python的循环语句。希望以后大家只要看这个程序，就能回想起相关的基础知识。
"""

# === range函数
# 产生一个类似于[0, 1, 2, 3, ...]这样的一个列表
# range的用法有：
# 1. range(N)：得到[0, 1, 2, 3, ..., N-1]
# 2. range(a, b)：得到[a, a+1, ..., b - 1]。这边要注意如果a>=b的话，得到的是[]
# 3. 第三种方法我们在有需要的时候给大家介绍，大家知道1和2就可以了，有兴趣可以在课程群内讨论。
# range(10)  # [0, 1, 2, ..., 9]
# print(range(10))  # 指代的是一个list但是这边不会直接输出
# print(list(range(10)))  # 强制转为list
# print(list(range(2, 6)))  # 强制转为list


# === 循环语句
"""
循环语句帮助我们做重复的事情。
理论上重复三遍以上的事情，我们就要考虑使用循环
"""

# === for循环语句介绍
# for循环是最常用的循环语句


# ·案例1：顺序循环输出一个list中的所有的元素
# for symbol in ['btcusdt', 'ethusdt', 'xrpusdt']:  # 其中symbol是变量名，可以任意取名
#     print(symbol)  # 使用tab进行缩进

# ·案例2：计算1+2+3+……+10
# sum_result = 0  # 用于存储计算的结果
# for number in range(10 + 1):
#     sum_result += number  # 此处需要使用tab按键进行缩进
#     print(number, sum_result)

# ·案例3：批量判断币的计价单位
# symbol_list = ['btcusdt', 'xrpbtc', 'xrpusdt', 'xrpeth', 'ethusdt', 'xrpbnb']
# for symbol in symbol_list:
#     if symbol.endswith('usdt'):
#         print(symbol, '以USDT计价')