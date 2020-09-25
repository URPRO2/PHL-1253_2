
"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 本节课程内容
- 注释
- print函数介绍
- 代码执行顺序
- 代码中的换行
- 代码中的空格
- 数字
- 字符串
- 布尔值
- 空值
- 变量名称
- 算术运算
- 比较运算
- 布尔运算

希望以后大家只要看这个程序，就能回想起相关的知识。
"""

# === 注释：python中不会运行的文字（或者说代码）
# 在每一行的开头，加上#，是对该行进行单行注释
# print('hello bitcoin')  # 行末注释，在一句程序的末尾，一般用来解释这句话。注意空格。

# · PyCharm快捷键：control + / 多行同时注释或取消注释（mac上是command + /）。
# 尝试同时取消注释或注释下面三行代码
# print('hello bitcoin')
# print('hello bitcoin')
# print('hello bitcoin')


# === print函数介绍：输出内容的重要工具
# print用于在终端上，也就是下面弹窗中，输出内容的工具，学名是全局函数
# print()  # 输出一个空行
# print(1)  # 输出一个1
# print(1, 2)  # 输出一个1和2
# print(1, 2, 3)  # 理论上是可以输出无限个元素，你给多少它终端上就输出多少


# === 代码执行顺序：按照我们写的顺序，依次执行
# print(2)
# print(3)
# print(1)
# 大家可以自己课后调整一下顺序，运行一下，感受一下


# === 代码中的换行
"""
1.空行是没有含义的，不会有任何的输出，也不影响代码的逻辑
2.不空行代码会报错
3.适当的空行可以对我们的代码进行排版
"""
# · 空行
# print(1)
#
# print(2)

# · 不空行会报错
# print(1)print(2)

# · 排版
# 你现在看到的示例代码就是，结合注释，可以相得益彰

# === 代码中的空格
# · 有的空格会产生报错
# print( 1)

# · 有的空格不会产生报错
# print( '邢不行')


# === 数字（integer，float）：int，float，以及一些特定场景下的表达方式
# · int类型的整数
# btc_total = 21000000  # 整数，比如比特币的总量是21000000
# print(btc_total, type(btc_total))  # type()函数的作用是输出变量的类型

# · float类型的浮点数
# btc_price = 8802.51  # 浮点数，btc在我备课的时候是8,802.51美金一个
# print(btc_price, type(btc_price))
# price_change = .0158  # 浮点数，在我备课时比特币最近24H涨幅为1.58%，小数点之前的0可以省略，.0158和0.0158是一样的。
# print(price_change, type(price_change))
# okb_price_change = -0.0031  # 负数的表示方式，在我备课的时候，OKB最近24H跌幅为-0.31%
# print(okb_price_change, type(okb_price_change))

# · 很大的数字，科学记数法
# market_capital = 1.6E11  # 市值，可以使用科学技术发来表示很大的数字，备课时BTC总市值为USD 160,641,814,194
# print(market_capital, type(market_capital))


# === 字符串（string）：str：python中的文字的表达