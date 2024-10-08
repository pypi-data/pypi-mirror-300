import numpy as np
import pandas as pd
from tqdm import tqdm



class AlphaMorpho:
    
    def __init__(self, df:pd.DataFrame):
        self.open:pd.DataFrame = np.log(df['open'])
        self.close:pd.DataFrame = np.log(df['close'])
        self.high:pd.DataFrame = np.log(df['high'])
        self.low:pd.DataFrame = np.log(df['low'])
        self.volume:pd.DataFrame = np.log(df['volume'])
        self.amt:pd.DataFrame = np.log(df['amount'])
        self.turn:pd.DataFrame = df['turnover']
        self.pct:pd.DataFrame = self.close-self.close.shift(1)
        self.dates = self.pct.index
        self.assets = self.pct.columns
    
    def basic_1(self):
        return self.close-self.open
    
    def basic_2(self):
        return self.close-self.low
    
    def basic_3(self):
        return self.close-self.high
    
    def basic_4(self):
        return self.open-self.low
    
    def basic_5(self):
        return self.open-self.high

    def basic_6(self):
        return self.high-self.low
    
    def basic_7(self):
        return self.high-self.high.shift(1)
    
    def basic_8(self):
        return self.low-self.low.shift(1)
    
    def basic_9(self):
        return self.turn
    
    def basic_10(self):
        return self.volume
    
    def basic_11(self):
        return self.volume-self.volume.shift(1)
    
    def basic_12(self):
        return np.abs(self.close-self.open) - np.abs(self.high-self.low)
    
    def basic_13(self):
        return self.pct/self.volume*100
    
    
    
    
    
    
    def mean_1(self):
        return self.close - self.close.rolling(window=5,min_periods=3).mean()
    
    def mean_2(self):
        return self.close - self.close.rolling(window=7,min_periods=3).mean()
    
    def mean_3(self):
        return self.close - self.close.rolling(window=10,min_periods=3).mean()
    
    def mean_4(self):
        return self.close - self.close.rolling(window=20,min_periods=3).mean()
    
    def mean_5(self):
        return self.volume - self.volume.rolling(window=5,min_periods=3).mean()
    
    def mean_6(self):
        return self.volume - self.volume.rolling(window=7,min_periods=3).mean()
    
    def mean_7(self):
        return self.volume - self.volume.rolling(window=10,min_periods=3).mean()
    
    def mean_8(self):
        return self.volume - self.volume.rolling(window=20,min_periods=3).mean()
    
    def mean_9(self):
        return self.turn.rolling(window=5,min_periods=3).mean()
    
    def mean_10(self):
        return self.turn.rolling(window=10,min_periods=3).mean()
    
    
    
    def max_1(self):
        return self.close - self.close.rolling(window=10,min_periods=3).max()
    
    def max_2(self):
        return self.close - self.close.rolling(window=20,min_periods=3).max()
    
    def max_3(self):
        return self.close - self.close.rolling(window=30,min_periods=3).max()
    
    def max_4(self):
        rmin = self.close.rolling(window=10,min_periods=3).min()
        rmax = self.close.rolling(window=10,min_periods=3).max()
        return (self.close-rmin)/(rmax-rmin)
    
    def max_5(self):
        rmin = self.close.rolling(window=20,min_periods=3).min()
        rmax = self.close.rolling(window=20,min_periods=3).max()
        return (self.close-rmin)/(rmax-rmin)
    
    def max_6(self):
        rmin = self.close.rolling(window=30,min_periods=3).min()
        rmax = self.close.rolling(window=30,min_periods=3).max()
        return (self.close-rmin)/(rmax-rmin)
    
    def max_7(self):
        return self.close - self.close.rolling(window=10,min_periods=3).max()
    
    def max_8(self):
        return self.close - self.close.rolling(window=20,min_periods=3).max()
    
    def max_9(self):
        return self.close - self.close.rolling(window=30,min_periods=3).max()
    
    def mix_1(self):
        return (self.high-self.low)/self.volume/20
    
    def mix_2(self):
        window=10
        result = weight_multip_sum(self.pct.values,self.volume.values,window=window,scale=100)
        result = pd.DataFrame(result,index=self.dates[window-1:],columns=self.assets)
        return result
    
    def mix_3(self):
        window=20
        result = weight_multip_sum(self.pct.values,self.volume.values,window=window,scale=100)
        result = pd.DataFrame(result,index=self.dates[window-1:],columns=self.assets)
        return result
    
    def mix_4(self):
        window=30
        result = weight_multip_sum(self.pct.values,self.volume.values,window=window,scale=100)
        result = pd.DataFrame(result,index=self.dates[window-1:],columns=self.assets)
        return result
    
    def mix_5(self):
        window=10
        result = weight_divide_sum(self.pct.values,self.volume.values,window=window)
        result = pd.DataFrame(result,index=self.dates[window-1:],columns=self.assets)
        return result
    
    def mix_6(self):
        window=20
        result = weight_divide_sum(self.pct.values,self.volume.values,window=window)
        result = pd.DataFrame(result,index=self.dates[window-1:],columns=self.assets)
        return result
    
    def mix_7(self):
        window=30
        result = weight_divide_sum(self.pct.values,self.volume.values,window=window)
        result = pd.DataFrame(result,index=self.dates[window-1:],columns=self.assets)
        return result
    
        
    
    
    
    
    def std_1(self):
        return self.pct.rolling(window=10,min_periods=3).std()
    
    def std_2(self):
        return (np.abs(self.open-self.close) - np.abs(self.high-self.low)).rolling(window=5,min_periods=3).std()
    
    def std_3(self):
        return (np.abs(self.open-self.close) - np.abs(self.high-self.low)).rolling(window=10,min_periods=3).std()
    
    def std_4(self):
        return (np.abs(self.open-self.close) - np.abs(self.high-self.low)).rolling(window=20,min_periods=3).std()
    
    def std_5(self):
        return self.pct.rolling(window=10,min_periods=3).std()
        
    def std_6(self):
        return self.pct.rolling(window=20,min_periods=3).std()




















def weight_multip_sum(data1:np.ndarray,data2:np.ndarray, window:int, scale=1, penalty=2):
    if data1.shape != data2.shape:
        raise ValueError
    result = []
    for i in tqdm(range(window,len(data1)+1)):
        a = data1[i-window:i]
        b = data2[i-window:i]
        b = (b/b.sum(axis=0))**penalty * scale
        factor = (a * b).sum(axis=0)
        result.append(factor)
    return np.vstack(result)

def weight_divide_sum(data1:np.ndarray,data2:np.ndarray, window:int, scale=1, penalty=2):
    if data1.shape != data2.shape:
        raise ValueError
    result = []
    for i in tqdm(range(window,len(data1)+1)):
        a = data1[i-window:i]
        b = data2[i-window:i]
        b = (b/b.sum(axis=0))**penalty * scale
        factor = (a / b).sum(axis=0)
        result.append(factor)
    return np.vstack(result)