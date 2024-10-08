import pandas as pd
import numpy as np
from pandas import DataFrame,Series
from datetime import datetime, timedelta

# from .dataget import sd, pro
from .stockcalendar import CALENDAR_TOOL, STOCKBASIC
from .data_statistics import stat_returns

##### 退市前90天和上市后90天，价格置空
def filter_stock_byDate(prices, filterdays_pre=90, filterdays_end=90):
    prices = prices.copy(deep=True)
    assets = prices.columns
    list_date = pd.to_datetime(STOCKBASIC['list_date'].loc[assets])
    delist_date = pd.to_datetime(STOCKBASIC['delist_date'].loc[assets].fillna('20800101'))
    for asset in assets:
        ld = list_date.loc[asset]
        dd = delist_date.loc[asset]
        ld += timedelta(filterdays_pre)
        dd -= timedelta(filterdays_end)
        prices[asset].loc[(prices.index < ld) | (prices.index > dd)] = np.nan
    return prices

### 根据权重表和0，1的买卖限制表重新调整为实际交易/持仓权重
def filter_weights_byLimit(weights, is_limit_buy, is_limit_sell):
    weights = weights.fillna(0)
    is_limit_buy = is_limit_buy.reindex(weights.index).fillna(0)
    is_limit_sell = is_limit_sell.reindex(weights.index).fillna(0)
    for i in range(len(weights.index)):
        if i != 0:
            chg = weights.iloc[i] - weights.iloc[i-1]
            lim_buy = is_limit_buy.iloc[i]
            lim_sell = is_limit_sell.iloc[i]
            chg.loc[(chg > 0) & (lim_buy>0)] = 0
            chg.loc[(chg < 0) & (lim_sell>0)] = 0
            weights.iloc[i] = weights.iloc[i-1] + chg
        else:
            chg = weights.iloc[i]
            lim_buy = is_limit_buy.iloc[i]
            lim_sell = is_limit_sell.iloc[i]
            chg.loc[(chg > 0) & (lim_buy>0)] = 0
            chg.loc[(chg < 0) & (lim_sell>0)] = 0
            weights.iloc[i] = chg
    return weights
    
    
class QuickBackTestor:
    def __init__(self, start_date, end_date, prices, filter_stock=False, is_limit_buy=None, is_limit_sell=None):
        self.start_date = start_date
        self.end_date = end_date
        if filter_stock:
            self._prices = filter_stock_byDate(prices, filterdays_pre=90,filterdays_end=90)
        else:
            self._prices = prices
        self._returns = self._prices.pct_change().fillna(0)
        self._commission = None
        self._trade_dates = CALENDAR_TOOL.trade_date_in_range(self.start_date, self.end_date)
        self._results = {"strategy_rewards": None,"weights": None, "turn":None, "strategy_feeadj_rewards":None}
        self._is_limit_buy = is_limit_buy
        self._is_limit_sell = is_limit_sell
        
    # def gen_is_limit(self,is_limit_buy=None,is_limit_sell=None):
    #     if is_limit_buy is None:
    #         self._is_limit_buy = pro.is_limit_buy(assets=self._prices.columns,start_date=self.start_date,end_date=self.end_date)
    #         print("Gen is_limit_buy succeed")
    #     else:
    #         self._is_limit_buy = is_limit_buy
    #     if is_limit_sell is None:
    #         self._is_limit_sell = pro.is_limit_sell(assets=self._prices.columns,start_date=self.start_date,end_date=self.end_date)
    #         print("Gen is_limit_sell succeed")
    #     else:
    #         self._is_limit_sell = is_limit_sell
    #     return None
        
        
    def _rewards_in_range(self, start_position, start_date, end_date):
        returns_slice = self._returns.loc[start_date:end_date].copy(deep=True)[start_position.index]
        # construct the imaginary returns:
        # short a stock is equal to long the stock that is purely negatively correlated with the prime stock
        returns_slice.iloc[:, np.where(start_position < 0)[0]] *= -1 
        start_position = np.abs(start_position)
        returns_slice.iloc[0] = 0
        pnls = (returns_slice + 1).cumprod()
        pnl = pnls.dot(start_position)
        rewards = pnl.pct_change()
        return rewards.iloc[1:]
    
    def ave_backtest(self):
        return (1+self._returns).cumprod().mean(axis=1)
 
    def run_backtest(self, strategy: pd.DataFrame, is_limit=True, fee=0.002):
            
        if not set(strategy.loc[self.start_date:self.end_date].index).issubset(set(self._trade_dates)):
            raise ValueError("the index of strategy must be a trade date")
        
        if strategy.isna().sum().sum() > 0:
            raise ValueError("the elements of startegy should not be nan")

        
        ### 限制买卖，需要提供买卖限制表
        if is_limit:
            if self._is_limit_buy is None or self._is_limit_sell is None:
                raise ValueError("you need to provide the is_limit_sell and buy frame")

            strategy = filter_weights_byLimit(strategy,self._is_limit_buy,self._is_limit_sell)

        strategy = strategy.loc[self.start_date:self.end_date]
        if strategy.index[-1] != pd.to_datetime(self.end_date):
            strategy.loc[pd.to_datetime(self.end_date)] = 0
    
        rebalance_dates = strategy.index.to_list()
        dates = list(zip(rebalance_dates[:-1], rebalance_dates[1:]))
        results = []

        for start_date, end_date in dates:

            result = self._rewards_in_range(strategy.loc[start_date], start_date, end_date)
            results.append(result)
        self._results["strategy_rewards"] = pd.concat(results).reindex(self._trade_dates).fillna(0)
        self._results["strategy"] = strategy.drop(strategy.index[-1])
        self.turnover_rate()
        self.fee_adjust_rewards(fee)
        return self._results["strategy_rewards"]
    
    # def run_backtests(self, strategies: Iterable[pd.DataFrame]):
    #     """run multiple backtests
    #     The strategies should be aligned in the same format

    #     Parameters
    #     ----------
    #     strategies : Iterable[pd.DataFrame]
    #         _description_
    #     """
    #     _strategies = []
    #     for strategy in strategies:
    #         _strategies.append(strategy.loc[self.start_date:self.end_date])
    #     sample_strategy = _strategies[0]
    #     if not set(sample_strategy.index).issubset(set(self._trade_dates)):
    #         raise ValueError("the index of strategy must be a trade date")
        
    #     if sample_strategy.isna().sum().sum() > 0:
    #         raise ValueError("the elements of startegy should not be nan")
        
    #     rebalance_dates = sample_strategy.index.to_list()
    #     dates = list(zip(rebalance_dates[:-1], rebalance_dates[1:]))
    #     results = [] 
    #     for start_date, end_date in dates:
    #         current_strategy = pd.concat([strategy.loc[start_date] for strategy in strategies], axis=1, ignore_index=True)
    #         result = self._rewards_in_range(current_strategy, start_date, end_date)
    #         results.append(result)
    #     self._results["strategy_rewards"] = pd.concat(results).reindex(self._trade_dates).fillna(0)  
    #     return self._results["strategy_rewards"]

    def turnover_rate(self):
        weights = self._results['strategy']
        turn = np.abs(weights - weights.shift(1)).sum(axis=1).fillna(1)
        self._results['turn'] = turn
        if turn.max() > 2:
            print("the max turnover is {} in {}, check your codes.".format(turn.max(),turn.idxmax()))
        return self._results['turn']

    def reset(self):
        self._results = {"strategy_rewards": None,"weights": None, "turn":None, "strategy_fee_adj_rewards":None}
    
    def fee_adjust_rewards(self, fee=0.002):
        self._results['strategy_fee_adj_rewards'] = self._results['strategy_rewards'] - fee*self._results['turn'].reindex(self._results['strategy_rewards'].index).fillna(0)
        return self._results['strategy_fee_adj_rewards']
    
    def summary(self, benchmark=None):
        returns = pd.concat([self._results['strategy_rewards'], self._results['strategy_fee_adj_rewards']],axis=1)
        returns.columns = ['strategy','strategy_with_fee']
        stat_r = stat_returns(returns,benchmark)
        return stat_r




