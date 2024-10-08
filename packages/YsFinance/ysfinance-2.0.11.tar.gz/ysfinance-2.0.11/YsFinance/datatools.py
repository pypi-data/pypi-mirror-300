import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from typing import Iterable


def drop_duplicated_index(a:pd.Series):
    """去除重复索引的行"""
    return a[~a.index.duplicated()]

def drop_highcorr(df:DataFrame,gap=0.7):
    """
    删除高相关性因子，因子名为columns
    
    Return: 剩余因子名列表
    """
    corr = df.corr()
    while True:
        l = len(corr)
        index = corr.index
        for i in range(l-1):
            for j in range(i+1,l):
                loc = index[i]
                col = index[j]
                # print((i,j,loc,col))
                v = corr[col].loc[loc]
                if v > gap:
                    corr = corr.drop(index=[loc],columns=[loc])
                    break
            if len(corr) != l:
                break
        if len(corr) == l:
            break
    return list(corr.index)


class DataHandle:

    @staticmethod
    def handle_nan_value(c,method='drop'):
        """c: Series|Dataframe"""
        l = len(c)
        if method == 'drop':
            c = c.dropna()
            if len(c)/l < 0.5:
                print('You have too many None value, please check your data.')
        
        elif method == 'ffill':
            c = c.ffill().dropna()

        elif method == 'bfill':
            c = c.bfill().dropna()
        
        elif method == 'mfill':
            c = c.fillna(c.mean())
        
        elif method == 'fill0':
            c = c.fillna(0)
        
        else:
            raise ValueError('method should be drop, ffill, bfill, mfill, fill0.')
        
        return [c[col] for col in c.columns]

    @staticmethod
    def handle_nan_value_series(data:Iterable[Series],method='drop'):
        """
        This function is to handle the nan value and align index for two Series data with similar index, you can pick the different methed to deal with.

        Params:
        - data:Iterable[Series], you should input two Seriers at least.

        - method:
            drop: drop the nan value.
            ffill: ffill the nan value.
            bfill: bfill the nan value.
            mfill: use the mean value to fill the nan value.
            fill0: use 0 to fill the nan value.
        
        - Return: Iterable[Series]
        """
        c:DataFrame = pd.concat(data,axis=1)
        l = len(c)
        if method == 'drop':
            c = c.dropna()
            if len(c)/l < 0.5:
                print('You have too many None value, please check your data.')
        
        elif method == 'ffill':
            c = c.ffill().dropna()

        elif method == 'bfill':
            c = c.bfill().dropna()
        
        elif method == 'mfill':
            c = c.fillna(c.mean())
        
        elif method == 'fill0':
            c = c.fillna(0)
        
        else:
            raise ValueError('method should be drop, ffill, bfill, mfill, fill0.')
        
        return [c[col] for col in c.columns]
        

    @staticmethod
    def handle_nan_value_X_y(X:DataFrame,y:Series,method='drop'):
        """
        This function is to handle the nan value and align index for X and y, you can pick the different methed to deal with.

        Params:
        - X:DataFrame
        - y:Series

        - method: pick a method to deal with the X data.
            drop: drop the nan value.
            ffill: ffill the nan value.
            bfill: bfill the nan value.
            mfill: use the mean value to fill the nan value.
            fill0: use 0 to fill the nan value.
        
        Return: (X_,y_)

        Warning: use 'y' as the columns name, you should ensure 'y' is not in X.columns.
        """

        if 'y' in X.columns:
            raise ValueError(' str(y) should not in X.columns')
        
        l = len(X)

        if method == 'drop':
            X_ = X.dropna().copy()
            if len(X_)/l < 0.5:
                print('You have too many None value, please check your data.')
        
        elif method == 'ffill':
            X_ = X.ffill().dropna().copy()

        elif method == 'bfill':
            X_ = X.bfill().dropna().copy()
        
        elif method == 'mfill':
            X_ = X.fillna(X.mean()).copy()
        
        elif method == 'fill0':
            X_ = X.fillna(0).copy()
        
        else:
            raise ValueError('method should be drop, ffill, bfill, mfill, fill0.')
        
        y_ = y.copy()
        y_.name = 'y'
        data = pd.concat([y_,X_],axis=1).dropna()
        y_ = data['y']
        X_ = data.drop(columns=['y'])
        
        return (X_,y_)
    
    @staticmethod
    def meanize(data:DataFrame):
        return data - data.mean(numeric_only=True)
    
    @staticmethod
    def normalize(data:DataFrame):
        return (data - data.mean(numeric_only=True))/data.std(numeric_only=True)
    
    @staticmethod
    def shrink_extreme_value(data: pd.DataFrame):
        rate = 0.05
        lower = data.quantile(rate)
        upper = data.quantile(1 - rate)

        if isinstance(data, pd.DataFrame):
            axis_value = 1
        elif isinstance(data, pd.Series):
            axis_value = 0
        else:
            raise ValueError("Unsupported data type. Use DataFrame or Series.")

        return data.clip(lower=lower, upper=upper, axis=axis_value)
    
    @staticmethod
    def normalize_and_shrink(data:DataFrame):
        nor = DataHandle.normalize(data)
        nor_shr = DataHandle.shrink_extreme_value(nor)
        return nor_shr.values
    
    @staticmethod
    def multi_index_meanize(data:DataFrame,level=[0]):
        return data.groupby(level=level).transform(DataHandle.meanize)
    
    @staticmethod
    def multi_index_normalize(data:DataFrame,level=[0]):
        return data.groupby(level=level).transform(DataHandle.normalize)
    
    @staticmethod
    def multi_index_shrink(data:DataFrame,level=[0]):
        return data.groupby(level=level).transform(DataHandle.shrink_extreme_value)
    
    @staticmethod
    def group_normalize(data:DataFrame, group:dict):
        return None
        mean = data.groupby(by=group).mean(numeric_only=True)
        std = data.groupby(by=group).std(numeric_only=True)
        return (data-mean)/std
    
    @staticmethod
    def linear_wash(factor:DataFrame, q=0.8, rate=None, err=500):
        """
        factor: pd.DataFrame, 通过除以每列abs0.8分位点的值做线性变换, 若变换后的值仍大于10则视为异常值,替换为空缺值
        """
        l = len(factor)
        if rate is None:
            
            q = np.abs(factor).quantile(q)
        else:
            q = np.abs(factor.iloc[:int(l*rate)]).quantile(q)
        lf = factor/q
        linear_wash_factor = DataFrame(np.where(np.abs(lf)>err,np.nan,lf),index=lf.index,columns=lf.columns)
        return linear_wash_factor
    
    @staticmethod
    def log_wash(factor:DataFrame):
        """
        
        Parmas:
        -factor: pd.DataFrame. 
        
        Return:
        -pd.DataFrame.
        
        Attention:
        - 注意这里没有对空缺值做额外处理.
        
        """
        abs_factor = np.abs(factor)
        logwash_factor = DataFrame(np.where(factor>0,np.log(1+abs_factor),-np.log(1+abs_factor)))
        logwash_factor.index = abs_factor.index
        logwash_factor.columns = abs_factor.columns
        return logwash_factor
    
    
    

#######################################################################################################################################################################################################


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

def dataframe_to_order(df:pd.DataFrame):
    result = []
    isna = np.where(df.isna(),np.nan,1)
    for i in range(len(df)):
        v = df.iloc[i].values
        order_v = order_array(v)
        result.append(order_v)
    result = np.vstack(result)*isna
    return DataFrame(result,index=df.index,columns=df.columns)
    


def value_to_sort_rate(amt:pd.DataFrame,lower=0.5,upper=1,penalty=2):
    """按照每行的值，变成序并压缩为处于lower->upper的rate, penalty为惩罚系数,即指数上的数值,默认为平方项，随着penalty增加，对小序的惩罚增加
    
    -math: l + (u-l)*(argsort/max(argsort))**p
    
    """
    amt_order = dataframe_to_order(amt)
    return lower + (upper-lower)*amt_order.divide(amt_order.max(axis=1),axis=0)**2