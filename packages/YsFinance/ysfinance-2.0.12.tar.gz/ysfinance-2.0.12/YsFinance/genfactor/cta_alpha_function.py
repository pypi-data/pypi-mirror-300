import numpy as np
import pandas as pd
from tqdm import tqdm
import copy as copy
import math
from collections import Counter
from sklearn.linear_model import LinearRegression

# 注：所有data1均为dataframe格式，不是series，不是series

def stable_place(xx):
    """
    划分成若干等长区间，计算各值所处的区间中值，返回众数
    :param xx:
    :return:
    """
    try:
        ranges=0.005
        top=xx.max()
        buttom=xx.min()
        denominator=xx.mean()
        n=math.ceil((top-buttom)/denominator/ranges)+1
        ran=np.linspace(buttom,top,n)
        x=copy.deepcopy(xx.values)
        for num in range(len(x)):
            y=x[num]
            for i in range(len(ran)-1):
                down=ran[i]
                up=ran[i+1]
                if (y>=down)&(y<up):
                    x[num]=(up+down)/2
                    break
        count=Counter(x)
        result=count.most_common(1)[0][0]
    except:
        result=0
    return result

####################时间序列####################
def Ts_Single_Rate(data1,n):
    """
    计算data1中每一列在时序上的变化百分比，基数为n前数

    注：会有大数出现
    Parameters
    ----------
    data1: Dataframe
    n:

    Return
    ----------
    result: Dataframe
    """
    result = data1.pct_change(periods = n).fillna(0)
    result = result.replace({np.inf: np.nan, -np.inf: np.nan})
    return result

def Ts_Single_AccRate(data1,n):
    """
    计算data1中每一列在时序上的变化百分比，
    基数为n前数，计算至今每一期的变化率，并求和，Acc: accumulate
    Parameters
    ----------
    data1: Dataframe
    n:

    Return
    ----------
    result: Dataframe
    """
    result = data1.rolling(n,min_periods=2).sum()/data1.shift(n) - n
    result = result.replace({np.inf: np.nan, -np.inf: np.nan})

    return result

def Ts_Shape_Compare(data1,data2,n):
    """
    对比data1与data2中每一列的值，回溯n期，统计n期内data2大于data1的次数

    Parameters
    ----------
    data1: Dataframe
    data2: Dataframe
    n:

    Return
    ----------
    result: Dataframe
    """
    data1_values=data1.values
    data2_values=data2.values
    result = pd.DataFrame(data1_values < data2_values, index=data1.index, columns=data1.columns).\
        rolling(n,min_periods=2).sum()
    result = result.replace({np.inf: np.nan, -np.inf: np.nan})
    return result

def Ts_Increase_Times_Discontinuous(data1,n):
    """
    回溯期n，计算是增长的次数

    Parameters
    ----------
    data1: Dataframe
    n:

    Return
    ----------
    result: Dataframe
    """
    result = (data1.diff() > 0).rolling(n,min_periods=2).sum()
    result = result.replace({np.inf: np.nan, -np.inf: np.nan})

    return result

def Ts_Decrease_Times_Discontinuous(data1,n):
    """
    回溯期n，计算是增长的次数

    Parameters
    ----------
    data1: Dataframe
    n:

    Return
    ----------
    result: Dataframe
    """
    result = (data1.diff() < 0).rolling(n,min_periods=2).sum()
    result = result.replace({np.inf: np.nan, -np.inf: np.nan})

    return result

def Ts_Unchanged_Times_Discontinuous(data1,n):
    """
    回溯期n，计算是增长的次数

    Parameters
    ----------
    data1: Dataframe
    n:

    Return
    ----------
    result: Dataframe
    """
    result = (data1.diff() == 0).rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isinf(result), np.nan)

    return result

def Ts_Single_Jump(data1, n):
    """
    回溯期n，期间出现不同值的次数

    Parameters
    ----------
    data1: Dataframe
    n:

    Return
    ----------
    result: Dataframe
    """

    result = data1.rolling(n,min_periods=2).apply(lambda x: len(x.unique()))
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isinf(result), np.nan)
    return result

def Ts_Single_StablePoint(data1,n):
    result = data1.rolling(n,min_periods=2).apply(stable_place)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isinf(result), np.nan)
    return result

## todo 计算中的参数设定存疑
def Ts_Single_Sharpee(data1,n):
    """
    回溯期n，夏普除以标准差

    Parameters
    ----------
    data1: Dataframe
    n:

    Return
    ----------
    result: Dataframe
    """
    rolling_mean = data1.rolling(n,min_periods=2).mean()
    rolling_std = data1.rolling(n,min_periods=2).std(ddof=0)** (3/2)
    result = rolling_mean / rolling_std * np.sqrt(250/n)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isinf(result), np.nan)

    return result

def Ts_Single_Sharp(data1,n):
    """
    回溯期n，夏普

    Parameters
    ----------
    data1: Dataframe
    n:

    Return
    ----------
    result: Dataframe
    """
    rolling_mean = data1.rolling(n,min_periods=2).mean()
    rolling_std = data1.rolling(n,min_periods=2).std(ddof = 0)
    result = rolling_mean / rolling_std * np.sqrt(250/n)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isinf(result), np.nan)

    return result

def Ts_Single_UpTrendRatio(data1,n):
    if n==1:
        result=copy.deepcopy(data1)
    else:
        result=np.full(data1.shape,np.nan)
        data1_values=data1.values
        start=n-1
        end=data1.shape[0]
        parameters=n-1
        for i in tqdm(range(start,end)):
            temp=data1_values[i-n+1:i+1,:]
            total_trend=((temp[-1]-temp[1])>0).astype(int)
            # 向量化运算
            count = np.nansum(np.diff(temp,axis = 0) >0 ,axis = 0)
            #
            rough_trend=count/parameters
            result[i,:]=total_trend*rough_trend

        where_are_inf = np.isinf(result)

        result[where_are_inf] = np.nan
        result[np.isnan(data1)] = np.nan
        result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_DownTrendRatio(data1,n):
    if n==1:
        result=copy.deepcopy(data1)
    else:
        result=np.full(data1.shape,np.nan)
        data1_values=data1.values
        start=n-1
        end=data1.shape[0]
        parameters=n-1
        for i in tqdm(range(start,end)):
            temp=data1_values[i-n+1:i+1,:]
            total_trend=((temp[-1]-temp[1])<0).astype(int)
            #
            count = np.nansum(np.diff(temp, axis=0) < 0, axis=0)
            #
            rough_trend=count/parameters
            result[i,:]=total_trend*rough_trend

        where_are_inf = np.isinf(result)

        result[where_are_inf] = np.nan
        result[np.isnan(data1)] = np.nan
        result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

# 计算均值等方法略有差异，效率未能提升，多列使用矩阵运算较快。
# def Ts_Single_AutoCorrelation(data1,n,lag=1):
#     result = data1.rolling(n,min_periods=2).apply(lambda x:x.autocorr(lag = lag))
#     result = result.where(~np.isinf(result), np.nan)
#   
#     result = result.where(~np.isinf(result), np.nan)
#     return result
def Ts_Single_AutoCorrelation(data1,n,lag=1):
    #lag=1
    data1_values=data1.values
    result=np.full(data1.shape, np.nan)
    start=lag+n-1
    end=data1.shape[0]
    result = []
    for i in range(start):
        result.append(np.full(data1.shape[1],np.nan))
    for i in tqdm(range(start,end)):
        temp1 = data1_values[i-(n-1):i+1,:]
        temp2 = data1_values[i-(n-1)-lag:i+1-lag,:]
        
        num = np.nanmean(((temp1 - np.nanmean(temp1,axis = 0))*(temp2-np.nanmean(temp2,axis = 0))),axis = 0)
        den = (np.nanstd(temp1,axis = 0 )*np.nanstd(temp2,axis = 0))
        den = np.where(den == 0, np.nan, den)
        result.append(num/den)
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    result = result.replace({np.inf: np.nan, -np.inf: np.nan})
    return result

def Ts_Single_AutoCorrelation1(data1,n):
    lag=1
    data1_values=data1.values
    result=np.full(data1.shape, np.nan)
    start=lag+n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        temp1 = data1_values[i-(n-1):i+1,:]
        temp2 = data1_values[i-(n-1)-lag:i+1-lag,:]
        result[i,:] = np.nanmean(((temp1 - np.nanmean(temp1,axis = 0))*(temp2-np.nanmean(temp2,axis = 0))),axis = 0)/((np.nanstd(temp1,axis = 0 )*np.nanstd(temp2,axis = 0)))
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    result = result.replace({np.inf: np.nan, -np.inf: np.nan})
    return result

def Ts_Single_ExpSmooth1(data1,n):
    alpha=0.7
    if n==1:
        result=copy.deepcopy(data1)
    else:
        wt = np.append((1 - alpha) ** (n - 1), (1 - alpha) ** np.arange(0, n - 1)[::-1] * alpha)
        result=np.zeros(data1.shape)
        data1_values=data1.values
        start=n
        end=data1.shape[0]
        for i in tqdm(range(start,end)):
            temp=data1_values[i-n+1:i+1,:]
            result[i,:]= np.dot(wt,temp)

        where_are_inf = np.isinf(result)

        result[where_are_inf] = np.nan
        result[np.isnan(data1)] = 0
        result = pd.DataFrame(result, index=data1.index, columns=data1.columns)
    return result

def Ts_Single_PositiveN(data1,n):
    positive_mark = data1 > 0
    result = positive_mark.rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Ts_Single_RSI(data1,n):
    data_pos = data1.where(data1 > 0, 0)
    data_abs = np.abs(data1)
    result = data_pos.rolling(n,min_periods=2).sum() / data_abs.rolling(n,min_periods=2).sum() * 100
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Ts_Single_Min(data1,n):
    result = data1.rolling(n,min_periods=2).min()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Ts_Single_Max(data1,n):
    result = data1.rolling(n,min_periods=2).max()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Ts_Single_Mean(data1,n):
    result = data1.rolling(n,min_periods=2).mean()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Ts_Single_Sum(data1,n):
    result = data1.rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Ts_Single_Multiply(data1,n):
    result = data1 * data1.shift(n)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Ts_Single_Divide(data1,n):
    result = data1 / data1.shift(n)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Ts_Single_Delay(data1,n):
    result = data1.shift(n)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Ts_Single_Delta(data1,n):
    result = data1.diff(periods = n)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Ts_Single_Plus(data1,n):
    result = data1 - data1.shift(n)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Ts_Single_Stddev(data1,n):
    result = data1.rolling(n,min_periods=2).std(ddof = 0)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

# todo skew和kurt略有不同，大差不差
def Ts_Single_Skewness(data1,n):
    result = data1.rolling(n,min_periods=2).skew()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Ts_Single_Kurtosis(data1,n):
    result = data1.rolling(n,min_periods=2).kurt()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

## todo TS 尚未改进

def Ts_Increase_Times_Continuous(data1,n):
    """
    回溯期n，最大连续增长的次数

    未能优化
    """
    data1_values=data1.values
    result=np.zeros(data1.shape)
    start=n
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        df=[]
        data_temp=data1_values[i-n:i+1,]
        count_times=np.zeros(data1.shape[1])
        for j in range(1,n+1):
            symbol=(data_temp[j]>data_temp[j-1])
            count_times+=symbol.astype(int)
            df.append(copy.deepcopy(count_times))
            count_times[~symbol]=0
        result[i,:]+=np.max(df,axis=0)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

# def Ts_Increase_Times_Continuous(data1,n):
#     """
#     回溯期n，最大连续增长的次数
#
#     Parameters
#     ----------
#     data1: Dataframe
#     n:
#
#     Return
#     ----------
#     result: Dataframe
#     """
#
#     def longest_continuous_one(x):
#         max_count = 0
#         count = 0
#         for i in x:
#             if i == 1:
#                 count += 1
#             else:
#                 max_count = max(max_count, count)
#                 count = 0
#         max_count = max(max_count, count)
#         return max_count
#     result = (data1.diff()>0).rolling(n,min_periods=2)
#     result = result.apply(longest_continuous_one)
#     result = result.where(~np.isinf(result), np.nan)
#   
#     result = result.where(~np.isinf(result), np.nan)
#     return result

def Ts_Decrease_Times_Continuous(data1,n):
    data1_values=data1.values
    result=np.zeros(data1.shape)
    start=n
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        df=[]
        data_temp=data1_values[i-n:i+1,]
        count_times=np.zeros(data1.shape[1])
        for j in range(1,n+1):
            symbol=(data_temp[j]<data_temp[j-1])
            count_times+=symbol.astype(int)
            df.append(copy.deepcopy(count_times))
            count_times[~symbol]=0
        result[i,:]+=np.max(df,axis=0)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Unchanged_Times_Continuous(data1,n):
    data1_values=data1.values
    result=np.zeros(data1.shape)
    start=n
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        df=[]
        data_temp=data1_values[i-n:i+1,]
        count_times=np.zeros(data1.shape[1])
        for j in range(1,n+1):
            symbol=(data_temp[j]==data_temp[j-1])
            count_times+=symbol.astype(int)
            df.append(copy.deepcopy(count_times))
            count_times[~symbol]=0
        result[i,:]+=np.max(df,axis=0)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_ExpSmooth2(data1,n):
    alpha=0.7
    beta=0.7
    if n==1:
        result=copy.deepcopy(data1)
    else:
        result=np.zeros(data1.shape)
        data1_values=data1.values
        start=n
        end=data1.shape[0]
        for i in tqdm(range(start,end)):
            temp=data1_values[i-n+1:i+1,:]
            temp1=temp[0,:]
            semp1=np.zeros(data1_values.shape[1])
            for j in range(1,n):
                temp0=copy.deepcopy(temp1)
                temp1=(1-alpha)*(temp1+semp1)+(alpha)*(temp[j])
                semp1=beta*(temp1-temp0)+(1-beta)*semp1
            result[i,:]=temp1

        where_are_inf = np.isinf(result)

        result[where_are_inf] = np.nan
        result[np.isnan(data1)] = np.nan
        result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_Pressure(data1,n):
    data1_values=data1.values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        temp1=copy.deepcopy(data1_values[i-n+1:i+1,:])
        matrix=(temp1>=temp1[-1,:]).astype(int)
        mul=temp1*matrix
        mul[mul==0]=np.nan
        result[i,:]=np.nanmedian(mul,axis=0)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_Support(data1,n):
    data1_values=data1.values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        temp1=copy.deepcopy(data1_values[i-n+1:i+1,:])
        matrix=(temp1<=temp1[-1,:]).astype(int)
        mul=temp1*matrix
        mul[mul==0]=np.nan
        result[i,:]=np.nanmedian(mul,axis=0)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_UpBoll(data1,n,k):
    data1_values=data1.values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        temp1=copy.deepcopy(data1_values[i-n+1:i+1,:])
        result[i,:]=data1_values[i,:]+np.nanstd(temp1,axis=0)*k
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_DownBoll(data1,n,k):
    data1_values=data1.values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        temp1=copy.deepcopy(data1_values[i-n+1:i+1,:])
        result[i,:]=data1_values[i,:]-np.nanstd(temp1,axis=0)*k
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_AroonUp(data1,n):
    data1_values=data1.values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        temp1=copy.deepcopy(data1_values[i-n+1:i+1,:])
        result[i,:]=(n-np.argmax(temp1,axis=0))/n*100
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_AroonDown(data1,n):
    data1_values=data1.values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        temp1=copy.deepcopy(data1_values[i-n+1:i+1,:])
        result[i,:]=(n-np.argmin(temp1,axis=0))/n*100
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result


def Ts_Single_Prod(data1,n):
    data1_values=data1.values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        result[i,:]=np.nanprod(data1_values[i-(n-1):i+1,],0)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_Percentile(data1,n,percent):
    #percent=15
    data1_values=data1.values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        result[i,:]=np.percentile(data1_values[i-(n-1):i+1,],percent,axis=0)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_Percentile_Inv(data1,n):
    data1_values=data1.values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        for j in range(data1.shape[1]):
            try:
                result[i,j]=(np.where(np.sort(data1_values[i-(n-1):i+1,j])==data1_values[i,j])[0][0]+1)/n
            except:
                pass
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Markov_Distance(data1,n):
    if n==1:
        result=copy.deepcopy(data1)
    else:
        data1_values=copy.deepcopy(data1.values)
        result=np.full(data1.shape,np.nan)
        start=n-1
        end=data1.shape[0]
        for i in tqdm(range(start,end)):
            temp=data1_values[i-n+1:i+1,]
            temp[np.isnan(temp)]=0
            Sigma=np.cov(temp)
            Value=np.linalg.det(Sigma)
            if (Value==0)|(math.isnan(Value)):
                result[i,:]=0
            else:
                Sigma_Inv=np.linalg.inv(Sigma)
                A=data1_values[i-n+1:i+1,]
                B=np.nanmean(data1_values[i-n+1:i+1,],axis=1)
                AB_DIFF=A-np.tile(B,(data1.shape[1],1)).T
                MAT=AB_DIFF.T.dot(Sigma_Inv).dot(AB_DIFF)
                result[i,:]=np.sqrt(MAT.diagonal())

        where_are_inf = np.isinf(result)

        result[where_are_inf] = np.nan
        result[np.isnan(data1)] = np.nan
        result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

####################横截面####################
def Cs_Single_UpZeroLimit(data1):
    result = data1.where(data1 >= 0 , 0)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isinf(result), np.nan)
    return result

def Cs_Single_DownZeroLimit(data1):
    result = data1.where(data1 <= 0 , 0)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isinf(result), np.nan)
    return result

def Cs_ZScore(data1):
    mean_row = np.nanmean(data1,axis = 1)
    std_row = np.nanstd(data1,axis = 1)
    result = data1.subtract(mean_row,axis = 0).divide(std_row,axis =0)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isinf(result), np.nan)
    return result

def Cs_RankScale(data1):
    result=data1[data1!=0].rank(axis=1)
    result = result.divide(np.nanmax(result,axis = 1),axis = 0).values
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    # result[result == 0] = np.nanmean(result[result != 0],axis = 1)
    for i in range(result.shape[0]):
        temp=result[i,:]
        temp[temp==0]=np.nanmean(temp[temp!=0])
        result[i,:]=temp

    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_DeepScale(data1):
    z_score = data1.subtract( np.nanmean(data1,axis = 1),axis = 0).\
        divide(np.nanstd(data1,axis = 1),axis = 0)
    result = z_score.subtract(np.nanmin(z_score,axis =1 ),axis = 0).\
        divide(np.nanmax(z_score,axis = 1)-np.nanmin(z_score,axis = 1),axis = 0)
    result = result.where(~np.isinf(result), np.nan)

    return result

def Cs_Instant_Increase(data1,ranges):
    result = (np.abs(data1.divide( data1.shift(1))) >= ranges).astype(int)
    # result = np.abs(data1).divide(data1.shift(1))
    result = result.where(~np.isinf(result), np.nan)

    return result

def Cs_Instant_Decrease(data1,ranges):
    result = (np.abs(data1.divide( data1.shift(1))) <= ranges).astype(int)
    result = result.where(~np.isinf(result), np.nan)

    return result

# ===min_periods取1=====
def Cs_Single_RankSD(data1,n):
    result = data1[data1!=0].rank(axis=1)
    result = result.rolling(n,min_periods = 1).std(ddof = 0)
    result = result.where(~np.isinf(result), np.nan)

    return result

def Cs_Single_RankMean(data1,n):
    result = data1[data1!=0].rank(axis=1)
    result = result.rolling(n,min_periods=1).mean()
    result = result.where(~np.isinf(result), np.nan)

    return result

## todo CS 尚未改进
def Cs_Single_Rank(data1):
    result=copy.deepcopy(data1[data1!=0].rank(axis=1).values)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    for i in range(result.shape[0]):
        temp=result[i,:]
        temp[temp==0]=np.nanmean(temp[temp!=0])
        result[i,:]=temp
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_Single_Correlation(data1,n):
    # 时序上每一列与所有列均值的相关系数
    if n==1:
        result=copy.deepcopy(data1)
    else:
        data1_values=data1.values
        result=np.full(data1.shape, np.nan)
        result = data1.values.copy()
        start=n-1
        end=data1.shape[0]
        for i in tqdm(range(start,end)):
            M=np.nanmean(data1_values[i-n+1:i+1,],axis=1)
            temp1 = np.tile(M,(data1.shape[1],1)).T
            temp2 = data1_values[i-(n-1):i+1,:]
            result[i,:]=np.nanmean(((temp1 - np.nanmean(temp1,axis = 0))*(temp2-np.nanmean(temp2,axis = 0))),axis = 0)/((np.nanstd(temp1,axis = 0 )*np.nanstd(temp2,axis = 0)))
      
        where_are_inf = np.isinf(result)
      
        result[where_are_inf] = np.nan
        result[np.isnan(data1)] = np.nan
        result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result
        

####################自身运算####################
def Self_Sign(data1):
    result = np.sign(data1)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Self_Negative(data1):
    result=-copy.deepcopy((data1))
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1), np.nan)
    return result

def Self_Inv(data1):
    result=copy.deepcopy(1/data1)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    return result

def Self_Abs(data1):
    result=data1.abs()
    result = result.where(~np.isinf(result), np.nan)
    return result

def Self_Log(data1):
    try:
        result=copy.deepcopy(np.log(data1))

        where_are_inf = np.isinf(result)
    
        #result[where_are_inf] = np.nan
        #result[np.isnan(data1)] = np.nan
    except:
        result=copy.deepcopy(np.log(data1))
    return result

def Self_Sqrt(data1):
    result=copy.deepcopy(np.sqrt(data1))
    result = result.where(~np.isinf(result), np.nan)

    return result

def Self_Sin(data1,n):
    result=copy.deepcopy(np.sin(data1/n/np.pi))
    result = result.where(~np.isinf(result), np.nan)

    return result

def Self_Cos(data1,n):
    result=copy.deepcopy(np.cos(data1/n/np.pi))
    result = result.where(~np.isinf(result), np.nan)

    return result

def Self_Tan(data1,n):
    result=copy.deepcopy(np.tan(data1/n/np.pi))
    result = result.where(~np.isinf(result), np.nan)

    return result

def Self_Power(data1,n):
    result=copy.deepcopy(data1**n)
    result = result.where(~np.isinf(result), np.nan)

    return result

def Self_SignPower(data1,n):
    result=np.sign(data1)*np.power(data1,n)
    result = result.where(~np.isinf(result), np.nan)

    return result

# def test1(data1):
#     result=copy.deepcopy(data1)
#   
#     where_are_inf = np.isinf(result)
#   
#     result[where_are_inf] = np.nan
#     result[np.isnan(data1)] = np.nan
#     return result
#
# def test2(data1):
#     result = data1# copy.deepcopy(data1)
#     result = result.where(~np.isinf(result), np.nan)
#   
#     result = result.where(~np.isinf(result), np.nan)
#     return result

def Self_SignPower_Inv(data1,n):
    result=np.sign(data1)*np.power(data1,1/n)
    result = result.where(~np.isinf(result), np.nan)

    return result

####################Compound Function####################
def Ts_Single_Max_Minus_Min(data1,n):
    rolling_max = data1.rolling(n,min_periods=2).max()
    rolling_min = data1.rolling(n,min_periods=2).min()
    result = rolling_max - rolling_min
    result = result.where(~np.isinf(result), np.nan)

    return result

def Ts_Single_Max_Plus_Min(data1,n):
    rolling_max = data1.rolling(n,min_periods=2).max()
    rolling_min = data1.rolling(n,min_periods=2).min()
    result = rolling_max + rolling_min
    result = result.where(~np.isinf(result), np.nan)

    return result

def Ts_Single_Max_Multiply_Min(data1,n):
    rolling_max = data1.rolling(n,min_periods=2).max()
    rolling_min = data1.rolling(n,min_periods=2).min()
    result = rolling_max * rolling_min
    result = result.where(~np.isinf(result), np.nan)

    return result

def Ts_Single_Max_Divide_Min(data1,n):
    rolling_max = data1.rolling(n,min_periods=2).max()
    rolling_min = data1.rolling(n,min_periods=2).min()
    result = rolling_max / rolling_min
    result = result.where(~np.isinf(result), np.nan)

    return result

def Ts_Single_Amplitude(data1,n):
    rolling_max = data1.rolling(n,min_periods=2).max()
    rolling_min = data1.rolling(n,min_periods=2).min()
    result = ((rolling_max - rolling_min) / rolling_min).abs()
    result = result.where(~np.isinf(result), np.nan)

    return result

def Ts_Single_Half_Decay(data1,n):
    result=np.full(data1.shape,np.nan)
    data1_values=data1.values
    start=n-1
    end=data1.shape[0]
    wt = [(1/2)**i for i in range(n,0,-1)]
    for i in tqdm(range(start,end)):
        result[i,:]=np.dot(wt ,data1_values[i-n+1:i+1,])
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_Log_Decay(data1,n):
    result=np.full(data1.shape,np.nan)
    data1_values=data1.values
    start=n-1
    end=data1.shape[0]
    wt = np.array( [np.log(i + 2) for i in range(n)] )
    wt = wt / np.sum(wt)
    for i in tqdm(range(start,end)):
        result[i,:]=np.matmul(wt,data1_values[i-n+1:i+1,])
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_Linear_Decay(data1,n):
    result=np.full(data1.shape,np.nan)
    data1_values=data1.ffill().values
    start=n-1
    end=data1.shape[0]
    wt = np.array([range(1,n+1)])
    for i in tqdm(range(start,end)):
        result[i,:]=np.dot(wt,data1_values[i-n+1:i+1,])*2/(n+1)/n
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Regression_SST(data1,n):
    data1_values=data1.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      x1=i-n+1
      y1=i+1
      result[i,:]= np.sum( np.power((data1_values[x1:y1,:]-np.nanmean(data1_values[x1:y1,:], axis = 0)),2), axis = 0)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

####################Two####################
# data2的index与columns应当与data1一致，否则强行转换成一致

def Ts_Double_WegihtAverage(data1,data2,n):
    data2_copy = data2.copy()
    data2_copy.columns = data1.columns
    rolling_multiply = (data1 * data2_copy).rolling(n,min_periods=2).sum()
    result = rolling_multiply / data2_copy.rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)

    return result

def Cs_Double_Plus(data1,data2):
    result = data1+data2
    result = result.replace({np.inf: np.nan, -np.inf: np.nan})
    return result

    data1_values=data1.values
    data2_values=data2.values
    result=data1_values+data2_values
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_Double_Minus(data1,data2):
    result = data1-data2
    result = result.replace({np.inf: np.nan, -np.inf: np.nan})
    return result

    data1_values=data1.values
    data2_values=data2.values
    result=data1_values-data2_values
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_Double_Multiply(data1,data2):
    result = data1*data2
    result = result.replace({np.inf: np.nan, -np.inf: np.nan})
    return result
    
    data1_values=data1.values
    data2_values=data2.values
    result=data1_values*data2_values
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_Double_Divide(data1,data2):
    result = data1/data2
    result = result.replace({np.inf: np.nan, -np.inf: np.nan})
    return result

    data1_values=data1.values
    data2_values=data2.values
    result=data1_values/data2_values

    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_UpGap(data1,data2):
    data2_copy = data2.copy()
    data2_copy.columns = data1.columns
    result = (data1.shift(1) < data2_copy).astype(int)
    result = result.where(~np.isinf(result), np.nan)
    return result

def Cs_DownGap(data1,data2):
    data2_copy = data2.copy()
    data2_copy.columns = data1.columns
    result = (data1 < data2_copy.shift(1)).astype(int)
    result = result.where(~np.isinf(result), np.nan)
    return result

def Ts_Double_Skewness(data1,data2,n):
    data1_values = data1.values
    data1_mean_values=data1.rolling(n,min_periods=2).mean().values
    data1_std_values = data1.rolling(n,min_periods=2).std(ddof = 0).values
    data2_values=data2.values
    data2_mean_values = data2.rolling(n,min_periods=2).mean().values
    data2_std_values = data2.rolling(n,min_periods=2).std(ddof = 0).values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        X=data1_values[i-n+1:i+1,]-data1_mean_values[i,:]
        Y=(data2_values[i-n+1:i+1,]-data2_mean_values[i,:])**2
        XY=(X*Y).mean(axis=0)
        X_SD=data1_std_values[i,:]
        Y_SD=(data2_std_values[i,:])**2
        XY_SD=X_SD*Y_SD
        XY_SD = np.where(XY_SD==0,np.nan,XY_SD)
        result[i,]=XY/(XY_SD)

    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Double_Kurtosis(data1,data2,n):
    data1_values = data1.values
    data1_mean_values=data1.rolling(n,min_periods=2).mean().values
    data1_std_values = data1.rolling(n,min_periods=2).std(ddof = 0).values
    data2_values=data2.values
    data2_mean_values = data2.rolling(n,min_periods=2).mean().values
    data2_std_values = data2.rolling(n,min_periods=2).std(ddof = 0).values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        X=data1_values[i-n+1:i+1,]-data1_mean_values[i,:]
        Y=(data2_values[i-n+1:i+1,]-data2_mean_values[i,:])**3
        XY=(X*Y).mean(axis=0)
        X_SD=data1_std_values[i,:]
        Y_SD=(data2_std_values[i,:])**3
        XY_SD=X_SD*Y_SD
        XY_SD = np.where(XY_SD==0,np.nan,XY_SD)
        result[i,]=XY/(XY_SD)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Euclidean_Distance(data1,data2,n):
    data2_copy = data2.copy()
    data2_copy.columns = data1.columns
    result = ( (data1 - data2_copy) ** 2 ).rolling(n,min_periods=2).sum() ** 0.5
    result = result.where(~np.isinf(result), np.nan)

    return result

def Ts_Manhattan_Distance(data1,data2,n):
    data2_copy = data2.copy()
    data2_copy.columns = data1.columns
    result = ( (data1 - data2_copy).abs() ).rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result
# todo 原函数有问题，绝对值取的位置有误
def Ts_Chebyshev_Distance(data1,data2,n):
    data2_copy = data2.copy()
    data2_copy.columns = data1.columns
    result = ( (data1 - data2_copy).abs() ** n ).rolling(n,min_periods=2).sum() ** (1/n)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Cs_Double_Highest(data1,data2):
    data1_values=data1.values
    data2_values=data2.values
    result = np.nanmax([data1_values,data2_values],axis=0)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_Double_Lowest(data1,data2):
    data1_values=data1.values
    data2_values=data2.values
    result = np.nanmin([data1_values,data2_values],axis=0)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_Double_Convergence(data1,data2,diff):
    data2_copy = data2.copy()
    data2_copy.columns = data1.columns
    result = (data1 - data2_copy).divide(data2_copy).abs()
    result = result.where(result<=diff, 0)
    result = result.where(result <= 0, 1)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Cs_Double_UpCross(data1,data2):
    data2_copy = data2.copy()
    data2_copy.columns = data1.columns
    result = ((data1.shift(1) < data2_copy.shift(1)) & (data1 > data2_copy)).astype(int)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Cs_Double_DownCross(data1,data2):
    data2_copy = data2.copy()
    data2_copy.columns = data1.columns
    result = ((data1.shift(1) > data2_copy.shift(1)) & (data1 < data2_copy)).astype(int)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result


# todo 回归相关尚未优化

def Ts_Double_Correlation(data1,data2,n):
    data1_values=data1.values
    data2_values=data2.values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        temp1 = data1_values[i-(n-1):i+1,:]
        temp2 = data2_values[i-(n-1):i+1,:]
        num = np.nanmean(((temp1 - np.nanmean(temp1,axis = 0))*(temp2-np.nanmean(temp2,axis = 0))),axis = 0)
        den = ((np.nanstd(temp1,axis = 0 )*np.nanstd(temp2,axis = 0)))
        den = np.where(den==0,np.nan,den)
        result[i,:] = num/den
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Double_Spearman(data1,data2,n):
    data1_values=data1.values
    data2_values=data2.values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        temp1=np.argsort(np.argsort(data1_values[i-n+1:i+1,:],0),0)
        temp2=np.argsort(np.argsort(data2_values[i-n+1:i+1,:],0),0)
        temp=np.nansum((temp1-temp2)**2,0)
        result[i,:]=1-6*temp/(n)/(n**2-1)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Double_Regression_Beta0(data1,data2,n):
    data1_values=data1.values
    data2_values=data2.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          result[i,j]=beta[0]
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Double_Regression_Beta1(data1,data2,n):
    data1_values=data1.values
    data2_values=data2.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          result[i,j]=beta[1]
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Double_Regression_FV(data1,data2,n):
    data1_values=data1.values
    data2_values=data2.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          result[i,j]=beta[0]+beta[1]*data2_values[i,j]
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Double_Regression_Res(data1,data2,n):
    data1_values=data1.values
    data2_values=data2.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          result[i,j]=beta[0]+beta[1]*data2_values[i,j]-data1_values[i,j]
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Double_Regression_SSE(data1,data2,n):
    data1_values=data1.values
    data2_values=data2.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          result[i,j]=pow((beta[0]+beta[1]*data2_values[x1:y1,j]-data1_values[x1:y1,j]),2).sum()
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Double_Regression_SSR(data1,data2,n):
    data1_values=data1.values
    data2_values=data2.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          result[i,j]=pow((beta[0]+beta[1]*data2_values[x1:y1,j]-np.nanmean(data1_values[x1:y1,j])),2).sum()
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Double_Regression_Rsuqre(data1,data2,n):
    data1_values=data1.values
    data2_values=data2.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          SSR=pow((beta[0]+beta[1]*data2_values[x1:y1,j]-np.nanmean(data1_values[x1:y1,j])),2).sum()
          SST=pow((data1_values[x1:y1,j]-np.nanmean(data1_values[x1:y1,j])),2).sum()
          result[i,j]=SSR/SST
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

####################Three####################
# data2,data3的index与columns应当与data1一致，否则强行转换成一致
def Cs_Triple_Plus(data1,data2,data3):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result=data1_values+data2_values+data3_values
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_Triple_Multiply(data1,data2,data3):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result=data1_values*data2_values*data3_values
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_Triple_Highest(data1,data2,data3):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result = np.nanmax([data1_values,data2_values,data3_values],axis=0)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_Triple_Lowest(data1,data2,data3):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result = np.nanmin([data1_values,data2_values,data3_values],axis=0)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_Triple_UpCross(data1,data2,data3):
    data2_copy = data2.copy()
    data2_copy.columns = data1.columns
    data3_copy = data3.copy()
    data3_copy.columns = data1.columns
    result = ((data1.shift(1) < data2_copy.shift(1)) & (data1 > data2_copy) & \
              (data1.shift(1) < data3_copy.shift(1)) & (data1 > data3_copy) ).astype(int)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isinf(result), np.nan)
    return result

def Cs_Triple_DownCross(data1,data2,data3):
    data2_copy = data2.copy()
    data2_copy.columns = data1.columns
    data3_copy = data3.copy()
    data3_copy.columns = data1.columns
    result = ((data1.shift(1) > data2_copy.shift(1)) & (data1 < data2_copy) & \
              (data1.shift(1) > data3_copy.shift(1)) & (data1 < data3_copy) ).astype(int)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

# todo 回归相关尚未优化
def Ts_Triple_Regression_Beta0(data1,data2,data3,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j],data3_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          result[i,j]=beta[0]
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Triple_Regression_Beta1(data1,data2,data3,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j],data3_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          result[i,j]=beta[1]
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Triple_Regression_Beta2(data1,data2,data3,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j],data3_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          result[i,j]=beta[2]
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Triple_Regression_FV(data1,data2,data3,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j],data3_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          result[i,j]=beta[0]+beta[1]*data2_values[i,j]+beta[2]*data3_values[i,j]
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Triple_Regression_Res(data1,data2,data3,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j],data3_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          result[i,j]=beta[0]+beta[1]*data2_values[i,j]+beta[2]*data3_values[i,j]-data1_values[i,j]
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Triple_Regression_SSE(data1,data2,data3,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j],data3_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          result[i,j]=pow((beta[0]+beta[1]*data2_values[x1:y1,j]+beta[2]*data3_values[x1:y1,j]-data1_values[x1:y1,j]),2).sum()
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Triple_Regression_SSR(data1,data2,data3,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j],data3_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          result[i,j]=pow((beta[0]+beta[1]*data2_values[x1:y1,j]+beta[2]*data3_values[x1:y1,j]-np.nanmean(data1_values[x1:y1,j])),2).sum()
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Triple_Regression_Rsuqre(data1,data2,data3,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
      for j in range(data1.shape[1]):
        x1=i-n+1
        y1=i+1
        Y=data1_values[x1:y1,j]
        X=np.vstack((np.ones((1,n)),data2_values[x1:y1,j],data3_values[x1:y1,j])).T
        Mat=np.matmul(X.T,X)
        Value=np.linalg.det(Mat)
        if (Value==0)|(math.isnan(Value)):
          result[i,j]=0
        else:
          beta=np.linalg.inv(Mat).dot(X.T).dot(Y)
          SSR=pow((beta[0]+beta[1]*data2_values[x1:y1,j]+beta[2]*data3_values[x1:y1,j]-np.nanmean(data1_values[x1:y1,j])),2).sum()
          SST=pow((data1_values[x1:y1,j]-np.nanmean(data1_values[x1:y1,j])),2).sum()
          result[i,j]=SSR/SST
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Triple_Correlation(data1,data2,data3,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result=np.full(data1.shape,np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        temp1 = data1_values[i-(n-1):i+1,:]
        temp2 = data2_values[i-(n-1):i+1,:]
        temp3 = data3_values[i-(n-1):i+1,:]
        result[i,:] = np.nanmean(((temp1 - np.nanmean(temp1,axis = 0))*(temp2-np.nanmean(temp2,axis = 0))*(temp3-np.nanmean(temp3,axis = 0))),axis = 0)/((np.nanstd(temp1,axis = 0 )*np.nanstd(temp2,axis = 0))*np.nanstd(temp3,axis = 0))
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

####################其他####################
def Ts_Shape_Doji(data1,data2,data3,data4,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    data4_values=data4.values
    result_value = ((np.abs((data2_values - data1_values) / data1_values) <= 0.02) & (
                np.abs((data2_values - data3_values) / data2_values) >= 0.02) & (
                 np.abs((data2_values - data4_values) / data2_values) >= 0.02)).astype(int)
    result = pd.DataFrame(result_value, index=data1.index, columns=data1.columns).\
        rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isinf(result), np.nan)
    return result

def Ts_Shape_UpLongLineRed(data1,data2,data3,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result_value = ((data2_values>data1_values)&
                    ((data3_values-data2_values)/data2_values>=0.04)).astype(int)
    result = pd.DataFrame(result_value, index=data1.index, columns=data1.columns).\
        rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isinf(result), np.nan)
    return result

def Ts_Shape_DownLongLineRed(data1,data2,data4,n):
    data1_values=data1.values
    data2_values=data2.values
    data4_values=data4.values
    result_value = ((data2_values>data1_values)\
                    &((data1_values-data4_values)/data1_values>=0.04)).astype(int)
    result = pd.DataFrame(result_value, index=data1.index, columns=data1.columns).\
        rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isinf(result), np.nan)
    return result

def Ts_Shape_UpLongLineGreen(data1,data2,data3,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    result_value = ((data2_values<data1_values)\
                    &((data3_values-data1_values)/data1_values>=0.04)).astype(int)
    result = pd.DataFrame(result_value, index=data1.index, columns=data1.columns).\
        rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Ts_Shape_DownLongLineGreen(data1,data2,data4,n):
    data1_values=data1.values
    data2_values=data2.values
    data4_values=data4.values
    result_value = ((data2_values<data1_values) \
                    &((data2_values-data4_values)/data1_values>=0.04)).astype(int)
    result = pd.DataFrame(result_value, index=data1.index, columns=data1.columns).\
        rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Ts_Shape_PlainDownLongLineRed(data1,data2,data3,data4,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    data4_values=data4.values
    result_value = ((data2_values>data1_values)\
                    &((data1_values-data4_values)/data1_values>=0.04)\
                    &(np.abs((data2_values-data3_values)/data2_values)<=0.01)).astype(int)
    result = pd.DataFrame(result_value, index=data1.index, columns=data1.columns).\
        rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isinf(result), np.nan)
    return result

def Ts_Shape_PlainUpLongLineRed(data1,data2,data3,data4,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    data4_values=data4.values
    result_value = ((data2_values>data1_values)\
                    &((data3_values-data2_values)/data2_values>=0.04)\
                    &(np.abs((data1_values-data4_values)/data1_values)<=0.01)).astype(int)
    result = pd.DataFrame(result_value, index=data1.index, columns=data1.columns).\
        rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Ts_Shape_PlainUpLongLineGreen(data1,data2,data3,data4,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    data4_values=data4.values
    result_value = ((data2_values<data1_values)\
                    &((data3_values-data1_values)/data1_values>=0.04)\
                    &(np.abs((data2_values-data4_values)/data2_values)<=0.01)).astype(int)
    result = pd.DataFrame(result_value, index=data1.index, columns=data1.columns).\
        rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Ts_Shape_PlainDownLongLineGreen(data1,data2,data3,data4,n):
    data1_values=data1.values
    data2_values=data2.values
    data3_values=data3.values
    data4_values=data4.values
    result_value = ((data2_values<data1_values)\
                    &((data2_values-data4_values)/data1_values>=0.04)\
                    &(np.abs((data1_values-data3_values)/data1_values)<=0.01)).astype(int)
    result = pd.DataFrame(result_value, index=data1.index, columns=data1.columns).\
        rolling(n,min_periods=2).sum()
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Cs_Quadruple_UpCross(data1,data2,data3,data4):
    data2_copy = data2.copy()
    data2_copy.columns = data1.columns
    data3_copy = data3.copy()
    data3_copy.columns = data1.columns
    data4_copy = data4.copy()
    data4_copy.columns = data1.columns
    result = ((data1.shift(1) < data2_copy.shift(1)) & (data1 > data2_copy) & \
              (data1.shift(1) < data3_copy.shift(1)) & (data1 > data3_copy) & \
              (data1.shift(1) < data4_copy.shift(1)) & (data1 > data4_copy) ).astype(int)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Cs_Quadruple_DownCross(data1,data2,data3,data4):
    data2_copy = data2.copy()
    data2_copy.columns = data1.columns
    data3_copy = data3.copy()
    data3_copy.columns = data1.columns
    data4_copy = data4.copy()
    data4_copy.columns = data1.columns
    result = ((data1.shift(1) > data2_copy.shift(1)) & (data1 < data2_copy) & \
              (data1.shift(1) > data3_copy.shift(1)) & (data1 < data3_copy) & \
              (data1.shift(1) > data4_copy.shift(1)) & (data1 < data4_copy) ).astype(int)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Dummy_Transform(data1):
    result=copy.deepcopy(data1)
    result[result>0]=1
    result[result<0]=0
    #result+=0.01
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    return result

def Ts_Single_RSV(data1,data2,data3,n):
    min_n = data3.rolling(n,min_periods=2).min().values
    max_n = data2.rolling(n,min_periods=2).max().values
    data1_values=data1.values
    result = (data1_values-min_n) /(max_n-min_n)*100
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_K(data1,data2,data3,n):
    K_initial=50
    data1_values=data1.values
    min_n = data3.rolling(n,min_periods=2).min().values
    max_n = data2.rolling(n,min_periods=2).max().values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        K_initial=(2/3)*K_initial+(1/3)*(data1_values[i,:]-min_n[i,:])/(max_n[i,:]-min_n[i,:])*100
        result[i,:]=K_initial
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_D(data1,data2,data3,n):
    K_initial=50
    D_initial=50
    data1_values=data1.values
    min_n = data3.rolling(n,min_periods=2).min().values
    max_n = data2.rolling(n,min_periods=2).max().values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        K_initial=(2/3)*K_initial+(1/3)*(data1_values[i,:]-min_n[i,:])/(max_n[i,:]-min_n[i,:])*100
        D_initial=(2/3)*D_initial+(1/3)*K_initial
        result[i,:]=D_initial
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_J(data1,data2,data3,n):
    K_initial=50
    D_initial=50
    data1_values=data1.values
    min_n = data3.rolling(n,min_periods=2).min().values
    max_n = data2.rolling(n,min_periods=2).max().values
    result=np.full(data1.shape, np.nan)
    start=n-1
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        K_initial=(2/3)*K_initial+(1/3)*(data1_values[i,:]-min_n[i,:])/(max_n[i,:]-min_n[i,:])*100
        D_initial=(2/3)*D_initial+(1/3)*K_initial
        result[i,:]=3*K_initial-2*D_initial
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_UpTrend(data1,n):
    result = (data1.diff() > 0).astype(int)
    result = (result.rolling(n,min_periods=2).sum() == n ).astype(int)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Ts_DownTrend(data1,n):
    result = (data1.diff() < 0).astype(int)
    result = (result.rolling(n,min_periods=2).sum() == n ).astype(int)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Ts_Single_HPM(data1,n,limit=0.01):
    maxs = data1.rolling(n,min_periods=2).max()
    mins = data1.rolling(n,min_periods=2).min()
    result = ((maxs-mins)/mins<=limit).astype(int)
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Ts_Single_RoughUpTrend(data1, n, rough_limit=0.75):
    result = np.zeros(data1.shape)
    data1_values = data1.values
    start = n - 1
    end = data1.shape[0]
    parameters = n - 1
    for i in tqdm(range(start, end)):
        temp = data1_values[i - n + 1:i + 1, :]
        total_trend = ((temp[-1] - temp[1]) > 0).astype(int)
        # 向量化运算
        count = np.nansum(np.diff(temp, axis=0) > 0, axis=0)
        #
        rough_trend = (count / parameters >= rough_limit).astype(int)
        result[i, :] += total_trend * rough_trend
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = 0
    result = pd.DataFrame(result, index=data1.index, columns=data1.columns)
    return result

def Ts_Single_RoughDownTrend(data1,n,rough_limit=0.75):
    result=np.zeros(data1.shape)
    data1_values=data1.values
    start=n-1
    end=data1.shape[0]
    parameters=n-1
    for i in tqdm(range(start,end)):
        temp = data1_values[i - n + 1:i + 1, :]
        total_trend = ((temp[-1] - temp[1]) < 0).astype(int)
        #
        count = np.nansum(np.diff(temp, axis=0) < 0, axis=0)
        #
        rough_trend=(count/parameters>=rough_limit).astype(int)
        result[i,:]+=total_trend*rough_trend
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_LinearStretch(data1,r1=0,r2=1):
    length=data1.shape[0]
    ratio=np.tile(np.linspace(r1,r2,length),(data1.shape[1],1)).T
    result=data1*ratio
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

def Ts_Single_NonlinearStretch(data1,r1=0,r2=1,times=0.5):
    length=data1.shape[0]
    ratio=np.tile(np.linspace(r1,r2,length)**times,(data1.shape[1],1)).T
    result=data1*ratio
    result = result.where(~np.isinf(result), np.nan)
    result = result.where(~np.isnan(data1),np.nan)
    return result

# todo 尚未优化
def Ts_Single_SMA(data1,n,M=3):
    ratio1=min(M/n,1)
    ratio2=1-ratio1
    result=np.zeros(data1.shape)
    data1_values=data1.values
    start=n
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        temp=data1_values[i-n+1:i+1,:]
        temp1=temp[0,:]
        for j in range(1,n):
            temp1=ratio2*temp1+ratio1*temp[j]
        result[i,:]=temp1
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Ts_Single_TR(high,low,close):
    result=np.zeros(high.shape)
    data1_values=(high-low).values
    data2_values=abs(low-close.shift(1)).values
    data3_values=abs(high-close.shift(1)).values
    start=0
    end=high.shape[0]
    for i in tqdm(range(start,end)):
        result[i,:]=np.nanmax([data1_values[i,:],data2_values[i,:],data3_values[i,:]],axis=0)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(high)]=0
    result=pd.DataFrame(result,index=high.index,columns=high.columns)
    return result

def Cs_Single_Regression_Res(data1, data2):
    data1_values = data1.values
    if len(data2.shape) == 1:
        data2_values = np.tile(data2, (data1.shape[0], 1))
    else:
        data2_values = data2.values
    result = np.full(data1.shape, np.nan)
    start = 0
    end = data1.shape[0]
    for i in tqdm(range(start, end)):
        x = data2_values[i]
        y = data1_values[i]

        beta = (x - np.nanmean(x)) * (y - np.nanmean(y)) / np.nanvar(x) / len(x)
        beta0 = np.nanmean(y) - beta * np.nanmean(x)
        res = beta * x + beta0 - y

        result[i] = res
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = 0
    result = pd.DataFrame(result, index=data1.index, columns=data1.columns)
    return result

def Cs_Muti_Regression_Res(data1, data2):
    data1 = data1.loc[~((data1 == 0) | (np.isnan(data1))).all(axis=1)]
    both_stock = data1.columns & data2.index
    data1_values = data1.loc[:, both_stock].values
    data2_values = data2.loc[both_stock].values
    result = np.full(data1_values.shape, np.nan)
    start = 0
    end = data1.shape[0]
    for i in tqdm(range(start, end)):
        Y = data1_values[i]
        X = data2_values
        delete = (np.isnan(Y))
        Y_ = Y[~delete]
        X_ = X[~delete, :]
        slr = LinearRegression()
        slr.fit(X_, Y_)
        result[i] = slr.predict(X) - Y
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result = pd.DataFrame(result, index=data1.index, columns=both_stock)
    return result

def Cs_Double_Regression_Res(data1, data2):
    data1_values = data1.values
    data2_values = data2.values
    result = np.full(data1_values.shape, np.nan)
    start = 0
    end = data1.shape[0]
    for i in tqdm(range(start, end)):
        try:
            Y = data1_values[i]
            X = data2_values[i]
            delete = (np.isnan(Y) | (Y == 0))
            Y_ = Y[~delete]
            X_ = X[~delete].reshape(-1, 1)
            slr = LinearRegression()
            slr.fit(X_, Y_)
            result[i] = slr.predict(X.reshape(-1, 1)) - Y
        except:
            pass
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result = pd.DataFrame(result, index=data1.index, columns=data1.columns)
    return result

def Cs_Fill_Stock(data1,data2):
    both_index=data1.index&data2.index
    data1=data1.loc[both_index]
    data2=data2.loc[both_index]
    result=pd.DataFrame(np.tile(data1,(data2.shape[1],1)).T,index=data2.index,columns=data2.columns)
    return result

def Ts_Fill_Time(data1,data2):
    both_index=data1.index&data2.columns
    data1=data1.loc[both_index]
    data2=data2.loc[:,both_index]
    result=pd.DataFrame(np.tile(data1,(data2.shape[0],1)),index=data2.index,columns=data2.columns)
    return result

def Cs_Extremum_Mad(data1,n=20,axis=1):
    data=copy.deepcopy(data1.values)
    #####考虑一维情况
    if len(data.shape)==1:
        temp=data
        median_temp=np.nanmedian(temp)
        new_median=np.nanmedian(abs(temp-median_temp))
        data=np.clip(temp,median_temp-n*new_median,new_median+n*new_median)
        data=pd.Series(data,index=data1.index)
    else:
        if axis==1:
            for i in range(data.shape[0]):
                temp=data[i]
                median_temp=np.nanmedian(temp)
                new_median=np.nanmedian(abs(temp-median_temp))
                data[i]=np.clip(temp,median_temp-n*new_median,new_median+n*new_median)
        elif axis==0:
            for i in range(data.shape[1]):
                temp=data[:,i]
                median_temp=np.nanmedian(temp)
                new_median=np.nanmedian(abs(temp-median_temp))
                data[:,i]=np.clip(temp,median_temp-n*new_median,new_median+n*new_median)
        data=pd.DataFrame(data,data1.index,data1.columns)
    return data
# 存疑
#data1=crossStockData['close1']
#n=10
#a=Ts_Single_Cummax(data1,n)
#data1.rolling(n,min_periods=2).sum()
def Ts_Single_Cummax(data1,n=np.inf):
    if n==np.inf:
        result=copy.deepcopy(data1.cummax(0))
    else:
        result=np.full(data1.shape,np.nan)
        start=n-1
        end=data1.shape[0]
        for i in tqdm(range(start,end)):
            result[i,:]=data1.iloc[i-n+1:i+1,:].cummax(0).iloc[-1]
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result
def Ts_Single_Cummin(data1,n=np.inf):
    if n==np.inf:
        result=copy.deepcopy(data1.cummin(0))
    else:
        result=np.full(data1.shape,np.nan)
        start=n-1
        end=data1.shape[0]
        for i in tqdm(range(start,end)):
            result[i,:]=data1.iloc[i-n+1:i+1,:].cummin(0).iloc[-1]
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result[np.isnan(data1)] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Score_Adjusted(data1,n=10,Decreasing=True):
    n=min(n,len(data1))
    if len(data1)==0:
        temp=copy.deepcopy(data1)
    else:
        data=copy.deepcopy(data1)
        data[data.isnull()]=0
        data=data.fillna(0)
        data=data.replace([np.inf, -np.inf],0)
        data[data==0]=np.nanmedian(data[data!=0])
        standard=np.linspace(0.1,1,n)
        standard_cutoff=np.linspace(0,1,n+1)
        cut_off_postion=np.round(len(data)*standard_cutoff)
        temp= data.sort_values(ascending=Decreasing)
        for i in range(n):
            temp.iloc[int(cut_off_postion[i]):int(cut_off_postion[i+1])]=standard[i]
        temp=temp.sort_index()
    return temp

def Score_Adjusted_Specific(data1,n=10,Decreasing=True):
    data_o=pd.Series(0,index=data1.index)
    data=data1[(data1!=0)&(~np.isnan(data1))&(~np.isinf(data1))]
    n=min(n,len(data))
    standard=np.linspace(0.1,1,n)
    standard_cutoff=np.linspace(0,1,n+1)
    cut_off_postion=np.round(len(data)*standard_cutoff)
    temp= data.sort_values(ascending=Decreasing)
    for i in range(n):
        temp.iloc[int(cut_off_postion[i]):int(cut_off_postion[i+1])]=standard[i]
    temp=(temp-np.nanmean(temp))/np.nanstd(temp)
    data_o.loc[temp.index&data_o.index]=temp.loc[temp.index&data_o.index]
    return data_o

def Cs_Single_Stratify(data1,layers=10):
    result=np.full(data1.shape,np.nan)
    data1_values=copy.deepcopy(data1)
    start=0
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        result[i]=Score_Adjusted(data1_values.iloc[i],n=layers)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_Single_Stratify_Specific(data1,layers=10):
    result=np.full(data1.shape,np.nan)
    data1_values=copy.deepcopy(data1)
    start=0
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        result[i]=Score_Adjusted_Specific(data1_values.iloc[i],n=layers)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_Self_Stratify(data1):
    layers=10
    result=np.full(data1.shape,np.nan)
    data1_values=copy.deepcopy(data1)
    start=0
    end=data1.shape[0]
    for i in tqdm(range(start,end)):
        result[i]=Score_Adjusted(data1_values.iloc[i],n=layers)
    where_are_inf = np.isinf(result)
    result[where_are_inf] = np.nan
    result=pd.DataFrame(result,index=data1.index,columns=data1.columns)
    return result

def Cs_Industry_Stratify(data1,industry_matrix,layer=10):
    result=copy.deepcopy(data1)
    data1_values=copy.deepcopy(data1)
    start=0
    end=data1.shape[0]
    for i in tqdm(data1.index):
        stock_temp=data1_values.loc[i]
        for j in industry_matrix.columns:
            temp=industry_matrix[j]
            in_index=(temp[temp==1].index)&(data1.columns)
            result.loc[i,in_index]=Score_Adjusted(stock_temp.loc[in_index],n=layer)
    return result

def Cs_Single_Industry_Stratify(data1):
    ##########industry
    layer=10
    result=copy.deepcopy(data1)
    data1_values=copy.deepcopy(data1)
    start=0
    end=data1.shape[0]
    # for i in tqdm(data1.index):
    #     stock_temp=data1_values.loc[i]
    #     for j in industry_matrix.columns:
    #         temp=industry_matrix[j]
    #         in_index=(temp[temp==1].index)&(data1.columns)
    #         result.loc[i,in_index]=Score_Adjusted(stock_temp.loc[in_index],n=layer)
    return result

