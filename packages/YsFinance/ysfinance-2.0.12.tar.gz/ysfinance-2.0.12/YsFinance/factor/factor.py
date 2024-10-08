import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import empyrical as ep
from .alphalens.tears import sd_get_Analysis_results
from .alphalens.utils import get_clean_factor_and_forward_returns
import warnings

# from ..dataget import pro


warnings.filterwarnings("ignore")

def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def decay(df, window, mode='linear', exp_f=1, NaToZero=False):
    """
    加权衰减函数，用于减少换手，时序函数，常用即放于此处
    线性加权:x[date]*window + x[date-1]*(window-1) + x[date-2]*(window-2) + x[date-3]*(window-3)...
    指数加权0<exp_f<1:x[date] + x[date-1]*exp_f^1 + x[date-2]*exp_f^2 + x[date-3]**exp_f^3...
    """

    if mode == 'linear':
        weight = np.array(range(1, window+1))
    elif mode == 'exp':
        weight = np.array(range(window-1, -1, -1))
        weight = exp_f**weight
    elif mode == 'exp2':
        weight = 2 ** (-((window - np.linspace(1, window, window) + 1) / (window/2)))
    else:
        raise ValueError('请确认加权模式')

    if NaToZero:
        nr = rolling_window(~np.isnan(df.values.T), window).copy()
        sum_w = df.copy()
        sum_w[:] = np.NaN
        sum_w.iloc[window-1:] = np.dot(nr, weight).T
        sum_w = sum_w.replace(0, np.nan)
        df = df.fillna(0)
    else:
        sum_w = weight.sum()

    r = rolling_window(df.values.T, window).copy()
    res = df.copy()
    res[:] = np.NaN
    res.iloc[window-1:] = np.dot(r, weight).T

    res = res/sum_w
    return res

def filter_stock_byDate(close, filterdays_pre, filterdays_end):
    """
    按上市和退市时间标记可用时间为1，不可用为nan
    Parameters
    ----------
    close : 带有date和issue的时间序列.
    filterdays_pre : 上市filterdays_pre之后置标记
    filterdays_end : 退市filterdays_pre之前置标记

    Returns
    -------
    date,issue,filterFlag

    """
    close = close.astype('float64')
    close[close < 0.01] = np.nan
    filterFlag_pre = close.shift(filterdays_pre)
    filterFlag_pre.iloc[:filterdays_pre] = close.iloc[0]
    filterFlag_end = close.shift(-filterdays_end)
    filterFlag_end.iloc[-filterdays_end:] = close.iloc[-1]

    filterFlag = close*np.nan
    filterFlag[close.notna()] = 1
    filterFlag[filterFlag_pre.isna()] = np.nan
    filterFlag[filterFlag_end.isna()] = np.nan

    return filterFlag



START_DATE = '19900101'
END_DATE = '20900101'



def wash_daily_price_factor(daily,factor,start_date=None,end_date=None, is_limit=True):
    """根据具有date, issue, close, adj, is_limit_buy, is_limit_sell的DataFrame清洗价格和因子"""
    if start_date is None:
        start_date = START_DATE
    if end_date is None:
        end_date = END_DATE
    
    daily = daily[(daily['date'] >= start_date) & (daily['date'] <= end_date)]
    daily['close_adj'] = daily['close']*daily['adj'] 
    close = daily.pivot(index='date', columns='issue', values='close_adj').sort_index()
    close.columns.name = 'asset'
    
    # 上市日期限制
    filterFlag = filter_stock_byDate(close, 90, 90)
    factor = factor * filterFlag    
    
    # 涨跌停限制
    if is_limit:
        is_limit_buy = daily.pivot(index='date', columns='issue', values='is_limit_buy')
        is_limit_sell = daily.pivot(index='date', columns='issue', values='is_limit_sell')

        factor[is_limit_buy == 1] = np.nan  # 涨停不选
        factor[is_limit_sell == 1] = np.nan   # 跌停不选
    
    factor = factor.stack().rename('factor').dropna()
    factor.index.names = ['date','asset']
    return close,factor 

def analysis(factor,prices,is_limit_buy,is_limit_sell,benchmark, quantiles,plot=False, periods=(1,3,5,10),mode='longonly'):
    """
    因子分析
    :param start_datetime开始时间
    :param end_datetime结束时间
    :param factor_data因子数据
    :param price_data量价数据
    """

    if mode=='longonly':
        print("*" * 50 + '\n' + '------输出做多收益模式指标')
    if mode=='benchmark':
        print("*" * 50 + '\n' + '------输出对标超额收益模式指标')
    if mode=='longshort':
        print("*" * 50 + '\n' + '------输出多空收益模式指标')

    factorRtndata = get_clean_factor_and_forward_returns(factor=factor, 
                                                         prices=prices,
                                                         quantiles=quantiles,
                                                         periods=periods, 
                                                         max_loss=0.1, 
                                                         benchmark=benchmark)
    results = sd_get_Analysis_results(factorRtndata, ana_mode=mode, plot=plot)
    print('Alphalens Complete')

    def sd_get_Nav_results(factor, prices, is_limit_buy, is_limit_sell,num=100, bench=None):
        factor = factor.unstack().sort_index()
        close = prices.replace([0, np.inf, -np.inf], np.nan)
        close = close.loc[close.index >= max(factor.index.min(), close.index.min())]
        close = close.loc[close.index <= min(factor.index.max(), close.index.max())]
        # ret = price_data['ret'].reindex_like(close).replace([np.nan, np.inf, -np.inf], 0)
        ret = close.pct_change(fill_method=None).replace([np.nan, np.inf, -np.inf], 0)
        is_limit_buy = is_limit_buy.reindex_like(close).fillna(1).astype(int)
        is_limit_sell = is_limit_sell.reindex_like(close).fillna(1).astype(int)
        factor = factor.reindex_like(close).astype('float64')
        if bench is None:
            benchmark = pd.Series(data=0, index=close.index)
        else:
            benchmark = bench.reindex(close.index).pct_change(fill_method=None).fillna(0)
        # %
        final_Report = dict()
        final_Report['weights'] = close.fillna(0)*0
        final_Report['dailyResults'] = pd.DataFrame(index=close.index)
        final_Report['dailyResults'].loc[:, 'dailyreturn'] = 0
        final_Report['dailyResults'].loc[:, 'dailyturnover'] = 0

        weight = final_Report['weights'].iloc[0, :].fillna(0)
        for d in range(len(close.index)):
            pre_date = close.index[d-1] if d > 0 else 0
            date = close.index[d]

            con_buylimit = is_limit_buy.loc[date] == 1
            con_selllimit = is_limit_sell.loc[date] == 1
            con_noexists = close.loc[date] < 0.01
            con_trade = (~ con_selllimit) & (~ con_buylimit) & (~ con_noexists)

            score = factor.loc[date]
            # score[~con_trade] = np.nan
            score = score[con_trade]
            score = score.dropna()
            # score = score.rename('score')
            pre_weight = final_Report['weights'].loc[pre_date].fillna(0).rename('weight') if d > 0 else final_Report['weights'].loc[date].fillna(0).rename('weight')
            pre_weight = pre_weight[pre_weight > 0.0001]

            n = int(min(num, np.floor(len(score)/1+0.5)))
            score = score.nlargest(n)
            weight = final_Report['weights'].loc[pre_date] if d > 0 else final_Report['weights'].loc[date]
            pre_weight = weight
            if len(score) > 0:
                weight = pre_weight*0
                weight[score.index] = 1/len(score)

            weight[con_selllimit] = np.maximum(weight[con_selllimit], pre_weight[con_selllimit])
            weight[con_buylimit] = np.minimum(weight[con_buylimit], pre_weight[con_buylimit])
            weight[con_selllimit & con_buylimit] = pre_weight[con_selllimit & con_buylimit]
            weight[con_noexists] = 0
            if weight[con_trade].sum() > 0.001:
                weight[con_trade] = weight[con_trade]*max(0, (1-weight[con_buylimit | con_buylimit].sum()))
            else:
                weight[con_trade] = 0

            final_Report['dailyResults'].loc[date, 'dailyreturn'] = np.sum(
                pre_weight*ret.loc[date])-benchmark.loc[date]
            final_Report['dailyResults'].loc[date, 'dailyturnover'] = sum(
                abs(weight-pre_weight))
            final_Report['weights'].loc[date] = weight
        final_Report['dailyResults']['dailyreturnAFTfees'] = final_Report['dailyResults']['dailyreturn'] - \
            final_Report['dailyResults']['dailyturnover']/2*0.0013
        if bench is None:
            final_Report['dailyResults']['return'] = (1+final_Report['dailyResults']['dailyreturn']).cumprod()
            final_Report['dailyResults']['returnAFTfees'] = (1+final_Report['dailyResults']['dailyreturnAFTfees']).cumprod()
        else:
            final_Report['dailyResults']['return'] = final_Report['dailyResults']['dailyreturn'].cumsum()
            final_Report['dailyResults']['returnAFTfees'] = final_Report['dailyResults']['dailyreturnAFTfees'].cumsum()

        Summary_table = pd.DataFrame()
        trading_days = len(close)
        Summary_table.loc['Annualized Return(%)', 'value'] = final_Report['dailyResults']['return'] .iloc[-1]/trading_days*243*100
        Summary_table.loc['Annualized ReturnAE(%)', 'value'] = final_Report['dailyResults']['returnAFTfees'] .iloc[-1]/trading_days*243*100
        Summary_table.loc['max_drawdown(%)', 'value'] = ep.max_drawdown(final_Report['dailyResults']['dailyreturnAFTfees'])*100
        Summary_table.loc['SharpeRatio', 'value'] = ep.sharpe_ratio(final_Report['dailyResults']['dailyreturnAFTfees'])
        Summary_table.loc['WinP20', 'value'] = (final_Report['dailyResults']['dailyreturnAFTfees'].rolling(20).sum() >= 0).sum()/(trading_days-20)
        Summary_table.loc['WinP60', 'value'] = (final_Report['dailyResults']['dailyreturnAFTfees'].rolling(60).sum() >= 0).sum()/(trading_days-60)
        Summary_table.loc['Mean turnover', 'value'] = final_Report['dailyResults']['dailyturnover'].mean()/2
        Summary_table.loc['Mean position', 'value'] = final_Report['weights'].sum(axis=1).mean()
        final_Report['Summary_table'] = Summary_table
        plotdata = pd.merge(final_Report['dailyResults']['return'],
                            final_Report['dailyResults']['returnAFTfees'], left_index=True, right_index=True)

        if bench is None:

            mean_quant_rateret_byYear = (final_Report['dailyResults']['dailyreturn'].add(1).groupby(final_Report['dailyResults']['dailyreturn'].index.get_level_values('date').to_period('A')).prod()**(
                243/final_Report['dailyResults']['dailyreturn'].add(1).groupby(final_Report['dailyResults']['dailyreturn'].index.get_level_values('date').to_period('A')).count())).add(-1)
            mean_quant_rateret_byYear_ae = (final_Report['dailyResults']['dailyreturnAFTfees'].add(1).groupby(final_Report['dailyResults']['dailyreturnAFTfees'].index.get_level_values('date').to_period('A')).prod()**(
                243/final_Report['dailyResults']['dailyreturnAFTfees'].add(1).groupby(final_Report['dailyResults']['returnAFTfees'].index.get_level_values('date').to_period('A')).count())).add(-1)
        else:
            mean_quant_rateret_byYear = final_Report['dailyResults']['dailyreturn'].groupby(final_Report['dailyResults']['dailyreturn'].index.get_level_values('date').to_period('A')).mean()*243
            mean_quant_rateret_byYear_ae = final_Report['dailyResults']['dailyreturnAFTfees'].groupby(final_Report['dailyResults']['dailyreturnAFTfees'].index.get_level_values('date').to_period('A')).mean()*243

        returns_table_byYear = pd.DataFrame()
        returns_table_byYear["Return(%)"] = (mean_quant_rateret_byYear * 100).round(2)
        returns_table_byYear["ReturnAE(%)"] = (mean_quant_rateret_byYear_ae * 100).round(2)
        returns_table_byYear["SR"] = \
            final_Report['dailyResults']['dailyreturnAFTfees'].groupby(final_Report['dailyResults']['dailyreturnAFTfees'].index.get_level_values('date').to_period('A'), group_keys=False).apply(ep.sharpe_ratio).round(2)
        returns_table_byYear["mdd(%)"] = \
            final_Report['dailyResults']['dailyreturnAFTfees'].groupby(final_Report['dailyResults']['dailyreturnAFTfees'].index.get_level_values('date').to_period('A'), group_keys=False).apply(ep.max_drawdown).round(4) * 100

        final_Report['returns_table_byYear'] = returns_table_byYear
        return final_Report, plotdata

    results_nav, plotdata_nav = sd_get_Nav_results(factor, prices, is_limit_buy,is_limit_sell,100, benchmark)
    results['results_nav'] = results_nav
    return results



class SingleFactorAnalysis:
    """
    prices: DataFrame, index = date, columns = asset
    factor: Series, Multiindex, level_0 = date, level_1 = asset
    is_limit_buy: prices like
    is_limit_sell: prices like
    benchmark: str|Series
    
    results:
        results = {}
        results['keyResults'] = keyResults_table:DataFrame
        results['ret_Data'] = ret_Data:dict
            'returns_table': 分组收益率统计量
            'ret_quant_daily': 分组日收益序列
            'ret_spread_quant_daily': 不同频率多空收益
            'ret_quant_daily_ae': 费后分组日收益
            'ret_spread_quant_daily_ae': 费后多空收益
            'cum_ret': 累计分组收益
            'ret_wide': 1D分组日收益
            'cum_ret_ae': 累计费后分组收益
            'ret_wide_ae': 1D费后分组日收益
            'returns_table_byYear':收益率结果按年统计
            'quantile_return':分组年化收益
            'quantile_return_ae':费后分组年化收益
        results['turnover_Data'] = turnover_Data:dict
            'turnover_table': 统计回测区间内总的分组换手率
            'quantile_turnover': 具体到某天的分组换手率
        results['IC_Data'] = IC_Data:DataFrame
    """
    
    def __init__(self,start_date,end_date,factor,prices,is_limit_buy,is_limit_sell,benchmark=None,period=(1,3,5,10),quantiles=None):
        self._start_date = start_date
        self._end_date = end_date
        self._factor = factor.loc[start_date:end_date]
        self._prices = prices
        self._is_limit_buy = is_limit_buy
        self._is_limit_sell = is_limit_sell
        self._benchmark = benchmark
        self._period = period
        if quantiles is None:
            quantiles = int(factor.groupby(level='date').count().mean()/(100)+0.5)
        self._quantiles=quantiles
        self.result = {}    
    def longonly_mode(self):
        if 'longonly' in self.result.keys():
            return self.result['longonly']
        self.result['longonly'] = analysis(self._factor,
                                           self._prices,
                                           self._is_limit_buy,
                                           self._is_limit_sell,
                                           quantiles=self._quantiles,
                                           benchmark=None,
                                           periods=self._period)
        return self.result['longonly']
    
    def benchmark_mode(self):
        if 'bench' in self.result.keys():
            return self.result['bench']
        if self._benchmark is None:
            raise ValueError("Need to provide benchmark price data")
        # if isinstance(self._benchmark, str):
        #     benchmark = pro.index_daily(self._benchmark)['close']
        # else:
        #     benchmark = self._benchmark
            
        self.result['bench'] = analysis(self._factor,
                                        self._prices,
                                        self._is_limit_buy,
                                        self._is_limit_sell,
                                        quantiles=self._quantiles,
                                        periods=self._period,
                                        benchmark=self._benchmark,
                                        mode='benchmark')
        return self.result['bench']
    
    def longshort_mode(self):
        if 'longshort' in self.result.keys():
            return self.result['longshort']
        self.result['longshort'] = analysis(self._factor,
                                           self._prices,
                                           self._is_limit_buy,
                                           self._is_limit_sell,
                                           quantiles=self._quantiles,
                                           benchmark=None,
                                           periods=self._period)
        return self.result['longshort']    

    
    