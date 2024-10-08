import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from .datatools import DataHandle
import statsmodels.api as sm
import scipy.stats as scist
from math import log
from joblib import Parallel,delayed


class StatReturns:
    """
    Input the returns series with freq-D, and get the statistics about the returns. If you input the benchmark returns series, you can get the alpha,beta and so on.

    Params: 
    - returns:DataFrame. Give the returns dataframe with day-freq
    - benchmark:Series. Give the benchmark asset returns series with day-freq. If you don't provide the data, you will not get the correlative analysis results.
    - start_date=None. The start date you analysis, if you do not provide, start date will be the returns data's start.
    - end_date=None. The end date you analysis, if you do not provide, end date will be the returns data's end.

    """
    def __init__(self,returns:DataFrame,benchmark:Series=None,start_date=None,end_date=None):
        if start_date is None:
            self._start_date = returns.index[0]
        else:
            self._start_date = start_date
        if end_date is None:
            self._end_date = returns.index[-1]
        else:
            self._end_date = end_date
        
        self._returns = returns.loc[start_date:end_date].copy()
        self._pnl = (1+self._returns).cumprod()
        if benchmark is not None:
            self._benchmark = benchmark.loc[start_date:end_date]
        else:
            self._benchmark = None


    def stat_frame(self,market:bool=False,window=90,q=0.05,rf=0):
        """
        Params:
        - market:bool=False. If market bool is True, you will get the market-correlative analysis, but ensure you provide the benchmark data.
        - window=90. Natual day number when you calculate the max drawdown, and it mutiply 21/30 as the trade day number.
        - q=0.05. VaR quantile. 
        - rf=0. Annualized risk free rate, this will be used when you calculate the sharpe ratio and linear regression.

        Results:Dataframe. With asset index and analysis project columns.

        Attentions:
        - 252 trading days a year.

        """
        means = self._returns.mean()*252
        stds = self._returns.std()*np.sqrt(252)
        sharpe_ratio = (means-rf)/stds
        max_drawdown = (1-self._pnl/(self._pnl.rolling(window=int(window*21/30)).max())).max() #每30天约为21个交易日，window为自然日
        VaR = self._returns.quantile(q)

        if not market:
            result = pd.concat([means,stds,sharpe_ratio,max_drawdown,VaR],axis=1)
            result.columns = ['mean','std','SR',f'mdd_{window}D',f'VaR_{q}']
            return result
        
        if self._benchmark is None:
            raise ValueError('You have not provide the benchmark returns.')
        
        alpha = []
        beta = []
        residual_std = []
        X,y = DataHandle.handle_nan_value_X_y(self._returns,self._benchmark,method='mfill')
        for col in self._returns.columns:
            params = np.polyfit(X[col],y,deg=1)
            be,al = params
            res = np.std(y-np.polyval(params,X[col]))
            beta.append(be)
            alpha.append(al*252)
            residual_std.append(res)
        beta = Series(beta,index = X.columns)
        alpha = Series(alpha, index = X.columns)-rf
        residual_std = Series(residual_std,index=X.columns)
        TR = (means-rf)/beta
        IR = alpha/residual_std/np.sqrt(252)
        result = pd.concat([means,stds,sharpe_ratio,max_drawdown,VaR,beta,alpha,TR,IR],axis=1)
        result.columns = ['mean','std','SR',f'mdd_{window}D',f'VaR_{q}','beta','alpha','TR','IR']
        result.index.name = 'asset'
        return result


def stat_returns(returns,benchmark=None,start_date=None,end_date=None,market=False,window=90,q=0.05,rf=0):
    stat = StatReturns(returns=returns,benchmark=benchmark,start_date=start_date,end_date=end_date)
    frame = stat.stat_frame(market=market,window=window,q=q,rf=rf)
    return frame

def stat_returns_by_period(returns,skip=100,benchmark=None,start_date=None,end_date=None,market=False,window=90,q=0.05,rf=0):
    result = []
    for k in range(0,len(returns.index),skip):
        df = returns.iloc[k:k+skip].copy()
        frame = stat_returns(df,benchmark,start_date=None,end_date=None,market=market,window=window,q=q,rf=rf)
        frame['start_date'] = df.index[0]
        frame['end_date'] = df.index[-1]
        result.append(frame)
    result = pd.concat(result)
    result.index.name = 'asset'
    result = result.reset_index().set_index(['end_date','asset']).sort_index()
    return result
        

class StatTtest:
    def __init__(self,X:Series,y:Series,method):
        data = pd.concat([X,y],axis=1).dropna()
        data.columns = ['X','y']
        self.data = data
        self.X = data['X']
        self.y = data['y']
        self.degree = len(self.data.index)
        self.method = method
    
    def reg_coef(self):
        if len(self.X) != len(self.y):
            raise ValueError("X,y should have the same dimension")
        if self.method == 'OLS':
            X = sm.add_constant(self.data['X'].values)
            y = self.data['y'].values
            model = sm.OLS(y,X).fit()
            beta = model.params[1]
            sr = model.bse[1]
            return (beta, beta/sr)
        if self.method == 'RLM':
            X = sm.add_constant(self.data['X'].values)
            y = self.data['y'].values
            model = sm.RLM(y,X).fit()
            beta = model.params[1]
            sr = model.bse[1]
            return (beta, beta/sr)
        if self.method == 'QR':
            X = sm.add_constant(self.data['X'].values)
            y = self.data['y'].values
            model = sm.QuantReg(y,X).fit(max_iter=3000)
            beta = model.params[1]
            sr = model.bse[1]
            return (beta, beta/sr)
        raise ValueError("method should be OLS, RLM or QR")
    
    def t_test(self,alpha=0.05):
        """返回系数是否大于0，是否显著大于0和小于0的bool值列表"""
        beta, t_value = self.reg_coef()
        bool_lst = [beta>0]
        if t_value > scist.t.ppf(1-alpha,df=self.degree-2):
            bool_lst.append(True)
        else:
            bool_lst.append(False)
        if t_value < scist.t.ppf(alpha,df=self.degree-2):
            bool_lst.append(True)
        else:
            bool_lst.append(False)
        return bool_lst
    

def order_array(value:np.ndarray):
    v = np.array(value)
    if len(v.shape) > 1:
        raise ValueError
    l = len(v)
    order_lst = [0 for i in range(l)]
    argsort = np.argsort(v)
    for i in range(l):
        order_lst[argsort[i]] = i 
    return np.array(order_lst)

class TabelRegression:
    """提供一个DataFrame, columns[0]=y, columns[1:]=X, index(level=0)=date, index(level=1)=asset"""
    
    def __init__(self,df:pd.DataFrame, n_jobs=12) -> None:
        self.df = df.dropna()
        self.y = self.df[df.columns[0]]
        self.X = self.df[df.columns[1:]]
        self.dates = self.df.index.get_level_values(0).unique()
        self.n_jobs = n_jobs
    
    def corr(self):
        return self.df.groupby(level=0).corr(method='spearman').groupby(level=1).mean()
    
    def mean(self, df):
        return df.groupby(level=0).mean()
    
    def std(self, df):
        return df.groupby(level=0).std()
    
    def linear_regression(self):
        
        def work_func(date,X,y):
            X = sm.add_constant(X)
            model = sm.OLS(y,X).fit()
            resid = model.resid
            params = model.params
            return (resid,params)

        
        results = Parallel(n_jobs=self.n_jobs)(delayed(work_func)(date,self.X.loc[date].values,self.y.loc[date].values) for date in self.dates)
        params = [np.array(p) for _,p in results if p is not None]
        resids = [np.array(r) for r,_ in results if r is not None]
        #### 注意如果你的模型某些日期有常数列，会导致参数确实一位，parmas无法stack，谨慎检查
        # params = pd.DataFrame(np.vstack(params),index=self.dates)
        resids = pd.DataFrame(np.hstack(resids),index=self.df.index)
        return (params,resids)
    
    def order_regression(self):
        def work_func(date,X,y):
            X = X.T
            result = []
            for i in range(len(X)):
                result.append(order_array(X[i]))
            X = np.vstack(result).T
            X = X/len(X)
            y = order_array(y)/len(y)
            X = sm.add_constant(X)
            model = sm.OLS(y,X).fit()
            resid = model.resid
            params = model.params
            return (resid,params)
        
        results = Parallel(n_jobs=self.n_jobs)(delayed(work_func)(date,self.X.loc[date].values,self.y.loc[date].values) for date in self.dates)
        params = [np.array(p) for _,p in results if p is not None]
        resids = [np.array(r) for r,_ in results if r is not None]
        #### 注意如果你的模型某些日期有常数列，会导致参数确实一位，parmas无法stack，谨慎检查
        # params = pd.DataFrame(np.vstack(params),index=self.dates)
        resids = pd.DataFrame(np.hstack(resids),index=self.df.index)
        return (params,resids)
            
            
  