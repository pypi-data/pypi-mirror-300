import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import tushare as ts
from joblib import Memory
import joblib
from datetime import datetime,timedelta
import os

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
resources_dir = os.path.join(current_dir, 'resources')
calendar_file_path = os.path.join(resources_dir, 'stock.calendar')
basic_file_path = os.path.join(resources_dir, 'stock.basic')



STARTDATE = '19910101'
ENDDATE = '20991231'
def reload():   
    ts.set_token(token='afc6021c1b2e8029eed7f41e1a7f9f98b87bc84cdc9ee3f5755df06a')
    pro = ts.pro_api()

    def CALENDAR_trade_get():
        df = pro.trade_cal(exchange='',start_date=STARTDATE,end_date=ENDDATE)
        df.columns = ['exchange','cal_date','is_open','pretrade_date']
        df.set_index('cal_date',inplace=True)
        df.index = pd.to_datetime(df.index)
        df['pretrade_date'] = pd.to_datetime(df['pretrade_date'])
        df.sort_index(inplace=True)
        return df

    def stock_basic():
        data1 = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date,list_status,delist_date')
        data2 = pro.stock_basic(exchange='', list_status='D', fields='ts_code,symbol,name,area,industry,list_date,list_status,delist_date')
        data = pd.concat([data1,data2]).set_index(['symbol'])
        data['list_date'] = pd.to_datetime(data['list_date'])
        data['delist_date'] = pd.to_datetime(data['delist_date'])
        return data
    
    calendar_file_path = os.path.join(resources_dir, 'stock.calendar')
    
    CALENDAR = CALENDAR_trade_get()
    STOCKBASIC = stock_basic()
    joblib.dump(CALENDAR,calendar_file_path)
    joblib.dump(STOCKBASIC,basic_file_path)
    print("Reload calendar, stockbasic: Success!")

memory = Memory(location='./cache')

STARTDATE = '19910101'
ENDDATE = '20251231'


# @memory.cache
# def CALENDAR_trade_get():
#     df = pro.trade_cal(exchange='',start_date=STARTDATE,end_date=ENDDATE)
#     df.columns = ['exchange','cal_date','is_open','pretrade_date']
#     df.set_index('cal_date',inplace=True)
#     df.index = pd.to_datetime(df.index)
#     df['pretrade_date'] = pd.to_datetime(df['pretrade_date'])
#     df.sort_index(inplace=True)
#     return df

# @memory.cache
# def stock_basic():
#     data1 = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date,list_status,delist_date')
#     data2 = pro.stock_basic(exchange='', list_status='D', fields='ts_code,symbol,name,area,industry,list_date,list_status,delist_date')
#     data = pd.concat([data1,data2]).set_index(['symbol'])
#     data['list_date'] = pd.to_datetime(data['list_date'])
#     data['delist_date'] = pd.to_datetime(data['delist_date'])
#     return data


def unique(lst):
    uni = np.unique(np.array(lst))
    uni.sort()
    return uni

# CALENDAR = CALENDAR_trade_get()
# STOCKBASIC = stock_basic()

CALENDAR = joblib.load(calendar_file_path)
STOCKBASIC = joblib.load(basic_file_path)

class CALENDAR:
    
    def __init__(self,start_date = STARTDATE,end_date = ENDDATE, CALENDAR = CALENDAR):
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.CALENDAR = CALENDAR
        
    def is_trade_date(self,date):
        if self.CALENDAR.loc[date]['is_open'] == 1:
            return True
        return False
    
    def trade_date_in_range(self,start_date=None,end_date=None,keeplast=True):
        '''get trade date between start_date and end_date
        if keeplast=False: 若end_date为交易日,则丢弃该日期,主要是防止分区间提取数据时发生日期重复问题
        '''
        tar = self.CALENDAR.loc[start_date:end_date].copy()
        tar = tar[tar['is_open']==1].index
        if keeplast:
            return tar
        if self.is_trade_date(pd.to_datetime(end_date)):
            return list(tar[:-1])
        else:
            return list(tar)
    
    def single_shift(self,date:datetime,days=0):
        '''get the last most recent trading date around date minus days'''
        assert isinstance(date,datetime), "input should be datetime type"
        date = date-timedelta(days)
        if date < self.start_date or date > self.end_date:
            return np.nan
        try:
            return self.trade_date_in_range(end_date=date)[-1]
        except:
            return np.nan 
        
    def single_next(self,date:datetime,days=0):
        '''get the first most recent trading date around date plus days'''
        assert isinstance(date,datetime), "input should be datetime type"
        date = date+timedelta(days)
        while date >= self.start_date or date <= self.end_date:
            if self.CALENDAR.loc[date]['is_open'] == 1:
                return date
            date += timedelta(1)
        return np.nan

    def shift(self,date_lst,days=0):
        '''get the last most recent trading dates around dates minus days'''
        if days==0:
            return pd.to_datetime(self.CALENDAR.loc[date_lst]['pretrade_date'].values)
        shift_date = []
        for date in date_lst:
            shift_date.append(self.single_shift(date,days=days))
        return pd.to_datetime(shift_date)
    
    def next(self,date_lst,days=0):
        '''get the next trading dates if current date is not a trading day'''
        if days==0:
            return pd.to_datetime(self.CALENDAR.loc[date_lst]['pretrade_date'].values)
        next_date = []
        for date in date_lst:
            next_date.append(self.single_next(date,days=days))
        return pd.to_datetime(next_date)
        
        
    def get_trade_date(self,date_lst):
        '''get the trade dates in the date list'''
        tar = self.CALENDAR.loc[date_lst].copy()
        return tar[tar['is_open']==1].index
    
    def monthly(self,start_date,end_date,loc=1):
        '''get the last trading day of each month if loc==1 or the first if loc==0 '''
        if loc == 1:
            date_lst = pd.date_range(start=start_date,end=end_date,freq='M')
            return self.shift(date_lst,days=0)
        if loc == 0:
            date_lst = pd.date_range(start=start_date,end=end_date,freq='MS')
            return self.next(date_lst,days=0)
        raise ValueError('param loc should be 0 or 1')
    
    def weekly(self,start_date,end_date,loc=1):
        '''get the last trading day of each week if loc==1 or the first if loc==0 '''
        if loc == 1:
            date_lst = pd.date_range(start=start_date,end=end_date,freq='W')
            return self.shift(date_lst,days=0).drop_duplicates().sort_values()
        if loc == 0:
            date_lst = pd.date_range(start=start_date,end=end_date,freq='WS')
            return self.next(date_lst,days=0).drop_duplicates().sort_values()
        raise ValueError('param loc should be 0 or 1')

CALENDAR_TOOL = CALENDAR()
