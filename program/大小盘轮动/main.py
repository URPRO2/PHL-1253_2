import pandas as pd
import datetime
import ccxt
import time

# import talib
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', None)


def get_sma_diff(symbol, limit, timeframe):
    df = ex.fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=20)
    df = pd.DataFrame(df, dtype=float)
    df.rename(columns={0: 'candle_begin_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
    # sma = signal_sma(df, limit)[-1]
    # sma = talib.SMA(df['close'].values, limit)[-1]
    sma = df['close'].mean()

    df['diff'] = df['close'].pct_change(19)
    # ret = (df.iat[-1, 4] - sma) / sma
    return df['diff'].values[-1]


def get_sma_diff_max(ex, symbols, timeframe, limit):
    """
    获取20日涨幅最大的币种
    """
    data = []
    for symbol in symbols:
        diff = get_sma_diff(symbol, limit, timeframe)
        data.append([symbol, diff])
    df = pd.DataFrame(data, dtype=float, columns=['symbol', 'diff'])
    df.sort_values(by='diff', inplace=True, ascending=False)
    df.reset_index(drop=True,