import abc
from functools import reduce

import numpy as np
import pandas as pd
import sunlandsdatasdk as sd


# region Auxiliary functions
def returns(df):
    return df.rolling(2).apply(lambda x: x.iloc[-1] / x.iloc[0]) - 1


def ts_sum(df, window=10):
    """
    Wrapper function to estimate rolling sum.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series min over the past 'window' days.
    """
    return df.rolling(window).sum()


def sma(df, window=10):
    """
    Wrapper function to estimate SMA.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series min over the past 'window' days.
    """
    return df.rolling(window).mean()


def stddev(df, window=10):
    """
    Wrapper function to estimate rolling standard deviation.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series min over the past 'window' days.
    """
    return df.rolling(window).std()


def correlation(x, y, window=10):
    """
    Wrapper function to estimate rolling corelations.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series min over the past 'window' days.
    """
    return x.rolling(window).corr(y)


def covariance(x, y, window=10):
    """
    Wrapper function to estimate rolling covariance.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series min over the past 'window' days.
    """
    return x.rolling(window).cov(y)


def rolling_rank(na):
    """
    Auxiliary function to be used in pd.rolling_apply
    :param na: numpy array.
    :return: The rank of the close value in the array.
    """
    return rankdata(na, method='min')[-1]


def ts_rank(df, window=10):
    """
    Wrapper function to estimate rolling rank.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series rank over the past window days.
    """
    return df.rolling(window).apply(rolling_rank)


def rolling_prod(na):
    """
    Auxiliary function to be used in pd.rolling_apply
    :param na: numpy array.
    :return: The product of the values in the array.
    """
    return np.prod(na)


def product(df, window=10):
    """
    Wrapper function to estimate rolling product.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series product over the past 'window' days.
    """
    return df.rolling(window).apply(rolling_prod)


def ts_min(df, window=10):
    """
    Wrapper function to estimate rolling min.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series min over the past 'window' days.
    """
    return df.rolling(window).min()


def ts_max(df, window=10):
    """
    Wrapper function to estimate rolling min.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series max over the past 'window' days.
    """
    return df.rolling(window).max()


def delta(df, period=1):
    """
    Wrapper function to estimate difference.
    :param df: a pandas DataFrame.
    :param period: the difference grade.
    :return: a pandas DataFrame with today’s value minus the value 'period' days ago.
    """
    return df.diff(period)


def delay(df, period=1):
    """
    Wrapper function to estimate lag.
    :param df: a pandas DataFrame.
    :param period: the lag grade.
    :return: a pandas DataFrame with lagged time series
    """
    return df.shift(period)


def rank(df):
    """
    Cross sectional rank
    :param df: a pandas DataFrame.
    :return: a pandas DataFrame with rank along columns.
    """
    return df.rank(axis=1, method='min', pct=True)
    # return df.rank(pct=True)


def scale(df, k=1):
    """
    Scaling time serie.
    :param df: a pandas DataFrame.
    :param k: scaling factor.
    :return: a pandas DataFrame rescaled df such that sum(abs(df)) = k
    """
    return df.mul(k).div(np.abs(df).sum())


def ts_argmax(df, window=10):
    """
    Wrapper function to estimate which day ts_max(df, window) occurred on
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: well.. that :)
    """
    return df.rolling(window).apply(np.argmax) + 1


def ts_argmin(df, window=10):
    """
    Wrapper function to estimate which day ts_min(df, window) occurred on
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: well.. that :)
    """
    return df.rolling(window).apply(np.argmin) + 1


def decay_linear(df, period=10):
    """
    Linear weighted moving average implementation.
    :param df: a pandas DataFrame.
    :param period: the LWMA period
    :return: a pandas DataFrame with the LWMA.
    """
    # Clean data
    if df.isnull().values.any():
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)
        df.fillna(value=0, inplace=True)
    na_lwma = np.zeros_like(df)
    na_lwma[:period, :] = df.iloc[:period, :]
    na_series = df.as_matrix()

    divisor = period * (period + 1) / 2
    y = (np.arange(period) + 1) * 1.0 / divisor
    # Estimate the actual lwma with the actual close.
    # The backtest engine should assure to be snooping bias free.
    for row in range(period - 1, df.shape[0]):
        x = na_series[row - period + 1: row + 1, :]
        na_lwma[row, :] = (np.dot(x.T, y))
    return pd.DataFrame(na_lwma, index=df.index, columns=['CLOSE'])


class Factor(abc.ABC):
    """
    因子定义抽象基类，自定义因子类必须继承它，实现calc方式
    """
    # 因子的名称， 不能与基础因子冲突。
    name = ''
    # 获取数据的最长时间窗口，返回的是日级别的数据。
    max_window = 1
    # 依赖的基础因子名称，包含 'open', 'close', 'low', 'high', 'volume', 'vwap', 'returns' 字段
    dependencies = []

    @abc.abstractmethod
    def calc(self, data):
        """
        计算因子值，子类必须实现

        :param data 是pandas.DataFrame对象, 行索引是datetime.datetime对象; 列是dependencies中数据
        :return 返回pandas.DataFrame或pandas.Series, 行索引是datetime.datetime对象, 列是股票标的, 值数据是因子值
        """
        pass


def calc_factors(securities, factors, start_date, end_date, frequency='daily', fq='pre'):
    """
    计算一支或者多只股票的多个因子

    :param securities 一支证券代码或者一个证券代码的list
    :param factors 因子实例，Factor()子类实例可遍历序列
    :param start_date 字符串或者 datetime.datetime/datetime.date 对象, 开始时间
    :param end_date 格式同上, 结束时间, 默认是'2015-12-31', 包含此日期.
    :param frequency 单位时间长度, 几天或者几分钟, 现在支持'Xd','Xm', 'daily'(等同于'1d'), 'minute'(等同于'1m'), X是一个正整数, 分别表示X天和X分钟
    :param fq 'pre',
    :return 返回pandas.DataFrame对象, 行索引是pandas.MultiIndex二级, 一级是datetime.datetime对象, 二级是股票标的; 列索引是因子名称列表; 值数据是对应因子值
    """
    # 获取聚宽JoinQuant标的行情数据，需要切换的接口
    # todo 需要切换到尚德自定义的接口，获取数据
    price = sd.get_price(securities, start_date=start_date, end_date=end_date,
                      fields=["date","issue", "market", "time", "quoteType", "preclose" ,"open","high","low","close","numTrades","volume","value","adj"])

    # 因子日收益率 =(T+1收盘价/T收盘价) - 1
    price['returns'] = price['close'] / price['preclose'] - 1
    price['avg'] = price['value'] / price['volume']

    # 计算因子所需数据与结构：开盘价，收盘价，最低价，最高价，成交量，成交均价，日收益率
    data = price.pivot(index='date', columns='issue',
                       values=['open', 'close', 'low', 'high', 'volume', 'avg', 'returns'])


    data.rename(columns={"avg": "vwap"}, inplace=True)

    factor_results = []

    for factor in factors:
        if issubclass(factor.__class__, Factor):
            sub_data = data[factor.dependencies]
            factor_data = factor.calc(sub_data)
            factor_data = pd.DataFrame(factor_data).stack()
            factor_data.name = factor.name
            factor_results.append(factor_data)
        else:
            print(f"{factor.__class__} is not subclass of factor.Factor")

    multi_factor_result = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True),
                                 factor_results)
    # multi_factor_result = multi_factor_result.unstack()
    return multi_factor_result
