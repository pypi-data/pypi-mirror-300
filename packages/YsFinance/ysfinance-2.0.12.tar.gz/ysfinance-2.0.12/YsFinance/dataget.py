# from .account import sd
# from .stockcalendar import CALENDAR_TOOL,STOCKBASIC
# from .stockcalendar import pro as ts_pro
# import pandas as pd
# from pandas import Series,DataFrame
# import numpy as np
# import datetime
# import joblib
# from .utils import get_resource_path

# START_DATE = '19900101'
# END_DATE = datetime.date.today().strftime("%Y%m%d")


# def trans_date(date):
#     date = pd.to_datetime(date)
#     return datetime.datetime.strftime(date,'%Y-%m-%d')



# def qfq(data:DataFrame):
#     if data.empty:
#         return data['close']
#     cum = (data['close']/data['pre_close']).cumprod()
#     last_price = data['close'].iloc[-1]
#     return cum/cum.iloc[-1]*last_price

# def qfq_daily_bar(data:DataFrame):
#     if data.empty:
#         return data
#     cum = (data['close']/data['pre_close']).cumprod()
#     last_price = data['close'].iloc[-1]
#     qfq_close = cum/cum.iloc[-1]*last_price
#     qfq_open = data['open']/data['close']*qfq_close
#     qfq_high = data['high']/data['close']*qfq_close
#     qfq_low = data['low']/data['close']*qfq_close
#     data['close'] = qfq_close
#     data['open'] = qfq_open
#     data['high'] = qfq_high
#     data['low'] = qfq_low
#     return data    

# class pro:
    
#     @staticmethod
#     def ini_daily(assets:list,start_date=None,end_date=None):
#         if not isinstance(assets, list):
#             assets = list(assets)
#         if start_date is None:
#             start_date = START_DATE
#         if end_date is None:
#             end_date = END_DATE
#         df = sd.get_bars(security=assets,start_date=start_date,end_date=end_date,unit='1d',fields=["date","issue", "preclose","open","high","low","close","last","volume","value","adj","ret","is_limit_buy","is_limit_sell","numTrades"]).reset_index()
#         return df
    
#     @staticmethod
#     def daily(assets:list, start_date=None, end_date=None, need_turn=False, hfq=False):
#         if not isinstance(assets, list):
#             assets = list(assets)
#         if start_date is None:
#             start_date = START_DATE
#         if end_date is None:
#             end_date = END_DATE
        
#         if hfq:
#             adjust='hfq'
#         else:
#             adjust=''
#         df = sd.get_bars(security=assets,start_date=start_date,end_date=end_date,unit='1d',fields=["date","issue", "preclose","open","high","low","close","last","volume","value","adj",'is_limit_buy','is_limit_sell'],adjust=adjust).reset_index()
#         project = ['issue','date','open','close','high','low','preclose','value','volume','adj','is_limit_buy','is_limit_sell']
#         df = df[project]
#         df.columns = ['asset','date','open','close','high','low','pre_close','amount','volume','adj','is_limit_buy','is_limit_sell']
#         df = df.set_index(['asset','date']).sort_index()
#         if need_turn:
#             turnover = sd.get_turnover_rate(assets,start_date=start_date,end_date=end_date,fields=['today'])
#             turnover.columns = ['asset','date','turnover']
#             turnover = turnover.set_index(['asset','date']).sort_index()/100
#             df = pd.concat([df,turnover],axis=1)
#         return df
    
#     @staticmethod
#     def daily_qfq(assets:list,start_date=None,end_date=None,need_turn=False):
#         """有坑，有些数据点pre_close在停牌时被ffill了，导致cumprod之后值很大或者很小，麻了"""
#         if not isinstance(assets, list):
#             assets = list(assets)
#         df = pro.daily(assets,start_date,end_date,need_turn)
#         df = df.groupby(level=0,group_keys=False).apply(qfq_daily_bar)
#         return df
    
    
#     @staticmethod
#     def price(assets:list, start_date=None,end_date=None):
#         if not isinstance(assets, list):
#             assets = list(assets)
#         df = pro.daily(assets,start_date,end_date)
#         df = df.groupby(level=0,group_keys=False).apply(qfq).unstack().T.sort_index()
#         return df
    
#     @staticmethod
#     def index_daily(asset:str,start_date=None,end_date=None):
#         if start_date is None:
#             start_date = START_DATE
#         if end_date is None:
#             end_date = END_DATE
        
#         df = sd.get_index_bar(asset, start_date=trans_date(start_date), end_date=trans_date(end_date))
#         df = df[['date','close','high','low','open','volume']]
#         df = df.set_index(['date']).sort_index()
#         df.index = pd.to_datetime(df.index)
#         return df
    
#     @staticmethod
#     def stock_basic():
#         return STOCKBASIC
    
#     @staticmethod
#     def index_components(asset:str,end_date, break_date='20090101'):
#         trade_date = CALENDAR_TOOL.trade_date_in_range(end_date=end_date)
#         for date in np.flip(trade_date):
#             if date < pd.to_datetime(break_date):
#                 print('component not found, break')
#                 return []
#             comp = sd.get_index_stocks(asset,date=date)
#             if len(comp) > 20:
#                 return (date,comp)
#         return (date,comp)  
    
#     @staticmethod
#     def is_limit_buy(assets,start_date=None,end_date=None):
#         if not isinstance(assets, list):
#             assets = list(assets)
#         if start_date is None:
#             start_date = START_DATE
#         if end_date is None:
#             end_date = END_DATE
        
#         df = sd.get_bars(security=assets,start_date=start_date,end_date=end_date,unit='1d',fields=["date","issue","is_limit_buy"]).reset_index().pivot(index = 'date', columns= 'issue', values='is_limit_buy').sort_index()
#         return df
    
#     @staticmethod
#     def is_limit_sell(assets,start_date=None,end_date=None):
#         if not isinstance(assets, list):
#             assets = list(assets)
#         if start_date is None:
#             start_date = START_DATE
#         if end_date is None:
#             end_date = END_DATE
        
#         df = sd.get_bars(security=assets,start_date=start_date,end_date=end_date,unit='1d',fields=["date","issue","is_limit_sell"]).reset_index().pivot(index = 'date', columns= 'issue', values='is_limit_sell').sort_index()
#         return df
        
# class fpro:
    
#     @staticmethod
#     def info_derive(types=False,fields=False):
#         info = joblib.load(get_resource_path('info.derive.finance'))
#         if types:
#             return info.index.get_level_values(0).unique()
#         if fields:
#             return info.index.get_level_values(1)
#         return info
    
#     @staticmethod
#     def factor_derive(issue:list,start_date=None,end_date=None,fields:list=None,type:str=None):
#         info:pd.DataFrame = fpro.info_derive()
#         s_types = set(info.index.get_level_values(0).unique())
#         s_fields = set(info.index.get_level_values(1))
#         if start_date is None:
#             start_date = START_DATE
#         if end_date is None:
#             end_date = END_DATE
#         if type is not None:
#             if type not in s_types:
#                 raise KeyError('type is wrong!')
#             fields = list(info.loc[type].index)
#             df = sd.get_ricequant_factor(issue,start_date,end_date,fields)
#             return df
#         else:
#             if fields is None:
#                 raise KeyError('Without type input, you should provide fields list.')
#             for f in s_fields:
#                 if f not in s_fields:
#                     raise KeyError("field '{}' is wrong.".format(f))
#             df = sd.get_ricequant_factor(issue,start_date,end_date,fields)
#             return df    