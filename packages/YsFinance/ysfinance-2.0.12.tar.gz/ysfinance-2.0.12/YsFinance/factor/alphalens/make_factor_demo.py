import os
import warnings

import alphalens as al
from factor import *

warnings.filterwarnings("ignore")


# 以下都是实现的因子Demo

class Alpha005(Factor):
    # 因子的名称， 不能与基础因子冲突。
    name = 'alpha005'
    # 获取数据的最长时间窗口，返回的是日级别的数据。
    max_window = 10
    # 依赖的基础因子名称，包含 'open', 'close', 'low', 'high', 'volume', 'vwap', 'returns' 字段
    dependencies = ['open', 'close', 'vwap']

    def calc(self, data):
        return rank((data['open'] - (ts_sum(data['vwap'], 10) / 10))) * (-1 * abs(rank((data['close'] - data['vwap']))))


class ALPHA006(Factor):
    # 因子的名称， 不能与基础因子冲突。
    name = 'alpha006'
    # 获取数据的最长时间窗口，返回的是日级别的数据。
    max_window = 10
    # 依赖的基础因子名称，包含 'open', 'close', 'low', 'high', 'volume', 'vwap', 'returns' 字段
    dependencies = ['open', 'volume']

    def calc(self, data):
        df = -1 * correlation(data['open'], data['volume'], self.max_window)
        return df.replace([-np.inf, np.inf], 0).fillna(value=0)


class SMA5(Factor):
    # 因子的名称， 不能与基础因子冲突。
    name = 'sma5'
    # 获取数据的最长时间窗口，返回的是日级别的数据。
    max_window = 5
    # 依赖的基础因子名称，包含 'open', 'close', 'low', 'high', 'volume', 'vwap', 'returns' 字段
    dependencies = ['close']

    def calc(self, data):
        return data['close'].rolling(5).mean()


class EMA5(Factor):
    # 因子的名称， 不能与基础因子冲突。
    name = 'ema5'
    # 获取数据的最长时间窗口，返回的是日级别的数据。
    max_window = 5
    # 依赖的基础因子名称，包含 'open', 'close', 'low', 'high', 'volume', 'vwap', 'returns' 字段
    dependencies = ['close']

    def calc(self, data):
        return data['close'].ewm(com=9, span=5, min_periods=self.max_window).mean()


class WMA5(Factor):
    # 因子的名称， 不能与基础因子冲突。
    name = 'wma5'
    # 获取数据的最长时间窗口，返回的是日级别的数据。
    max_window = 5
    # 依赖的基础因子名称，包含 'open', 'close', 'low', 'high', 'volume', 'vwap', 'returns' 字段
    dependencies = ['close']

    def calc(self, data):
        return data['close'].rolling(self.max_window).apply(
            lambda x: x[::-1].cumsum().sum() * 2 / self.max_window / (self.max_window + 1))


if __name__ == '__main__':
    # 测试开始时间, 测试结束时间
    # start_date = datetime.datetime(2022, 8, 15)
    # end_date = datetime.datetime(2022, 9, 25)

    print(os.environ)

    start_date = 20211015
    end_date = 20220925

    # 沪深300股票池
    stocks = sd.get_index_stocks("000300")

    print(stocks)

    # 自定义因子
    factor_data = calc_factors(securities=stocks, factors=[ALPHA006()], start_date=start_date,
                               end_date=end_date)
    # factor_data = calc_factors(securities=stocks, factors=[Alpha005(), ALPHA006()], start_date=start_date,
    #                            end_date=end_date)

    # 需要转换成pd.MultiIndex结构
    print("*" * 200)
    print(factor_data)

    # multiIndexFactors = factor_data['alpha006']
    multiIndexFactors = factor_data

    print("*" * 200)
    print(multiIndexFactors)

    forwardPeriodPrices = sd.get_price(stocks, start_date=start_date, end_date=end_date,
                                       fields=['close'])

    forwardPeriodPrices = forwardPeriodPrices.pivot(index='date', columns='issue',
                                                    values='close')

    print("*" * 200)
    print(forwardPeriodPrices)

    # periods是计算未来1、5、10、15的收益率
    data = al.utils.get_clean_factor_and_forward_returns(factor=multiIndexFactors, prices=forwardPeriodPrices,
                                                         quantiles=5, periods=(1, 5, 10, 15), max_loss=1)

    print("*" * 200)
    print(data)

    sd_get_Analysis_results = al.tears.sd_get_Analysis_results(data, longshort=True, plot=True)

    print("*" * 200)
    print(sd_get_Analysis_results)

    sd_get_return_results = al.tears.sd_get_return_results(data,turnover_Data=None, longshort=True, plot=True)

    print("*" * 200)
    print(sd_get_return_results)
    # al.tears.create_full_tear_sheet(data)
