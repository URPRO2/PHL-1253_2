import pandas as pd
import ccxt
import time
import datetime
from dateutil.relativedelta import relativedelta


# df['candle_begin_time_GMT8'] = pd.to_datetime(df['candle_begin_time'], unit='ms') + timedelta(hours=8)  # 北京时间
# df.drop(columns=['candle_begin_time'], inplace=True)
# df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]

# print(df)


def updateSymbolData(ex, symbol, timeframe, startTime, endTime):
    dfList = []
    while startTime < endTime:
        data = ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=2000, since=ex.pars