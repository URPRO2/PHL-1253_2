
"""
# 课程内容
计算策略信号的函数
"""
import pandas as pd
import numpy as np
import talib


def signal_sma(df,limitNum):
    """
    计算均线