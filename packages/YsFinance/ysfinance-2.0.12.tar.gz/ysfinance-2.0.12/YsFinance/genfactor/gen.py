from pandas import DataFrame
import pandas as pd
from .cta_alpha_factor import AlphaLC
from .morpho_factor import AlphaMorpho
from joblib import delayed,Parallel
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

def trans_multicolumns(data):
    """data:pd.DataFrame, multiindex, level_0 assets, level_1 date, columns projects"""
    
    return data.unstack(level=0)
    # multi_col_data = []
    # for col in data.columns:
    #     d = data[col].unstack().reset_index()
    #     d['project'] = col
    #     multi_col_data.append(d)
    # multi_col_data = pd.concat(multi_col_data).set_index(['project','asset'])
    # return multi_col_data.T.sort_index()
    

class DailyMoveFactor:
    """Generate move factor based on daily bar.
    """
    def __init__(self, daily:DataFrame,min_length = 60):
        """daily:DataFrame. With datetime index, multicolumns and level_0 includes open,high,low,close,volume,amount,turnover, level_1 with assets."""
        if len(daily) < min_length:
            raise ValueError("len(daily) < min_length")
        self.daily = daily.sort_index()
        self.alpha = AlphaLC(df_data=self.daily)
        self.factor_name = [method for method in dir(AlphaLC) if callable(getattr(AlphaLC, method)) and not method.startswith("__")]
        
    def gen_factor(self,factor_name=None):
        if factor_name is None:
            factor_name = self.factor_name
            
        factor_data = []
        used_fac = []
        for name in factor_name:
            if hasattr(AlphaLC, name) and callable(getattr(AlphaLC, name)):
                try:
                    print("计算中：{}".format(name))
                    fac = getattr(self.alpha, name)()
                    fac.index = pd.to_datetime(fac.index)
                    fac = fac.stack(dropna=False).sort_index().astype('float32')
                    used_fac.append(name)
                    factor_data.append(fac)
                except:
                    print(f"函数 {name} 计算时出错")
                    continue
            else:
                print(f"函数 {name} 未找到")
        factor_data = pd.concat(factor_data,axis=1).sort_index()
        factor_data.columns = used_fac
        return factor_data.astype('float32')
    
    def quick_gen_factor(self,factor_name=None,n_job=8):
        if factor_name is None:
            factor_name = self.factor_name 
            
        def work_func(name):
            if hasattr(AlphaLC, name) and callable(getattr(AlphaLC, name)):
                try:
                    print("计算中：{}".format(name))
                    fac = getattr(self.alpha, name)()
                    fac.index = pd.to_datetime(fac.index)
                    fac = fac.stack(future_stack=True).sort_index().astype('float32')
                    fac.name = name
                    return fac
                except:
                    print(f"函数 {name} 计算时出错")
                    return None
            else:
                print(f"函数 {name} 未找到")
                return None
        
        results = Parallel(n_jobs=n_job)(delayed(work_func)(name) for name in factor_name)
        return results
        

class MorphoFactor:
    
    """Generate morphology factor based on daily bar.
    """
    def __init__(self, daily:DataFrame,min_length = 60):
        """daily:DataFrame. With datetime index, multicolumns and level_0 includes open,high,low,close,volume,amount,turnover, level_1 with assets."""
        if len(daily) < min_length:
            raise ValueError("len(daily) < min_length")
        self.daily = daily.sort_index()
        self.alpha = AlphaMorpho(df=self.daily)
        self.factor_name = [method for method in dir(AlphaMorpho) if callable(getattr(AlphaMorpho, method)) and not method.startswith("__")]
        
    def gen_factor(self,factor_name=None):
        if factor_name is None:
            factor_name = self.factor_name
            
        factor_data = []
        used_fac = []
        for name in factor_name:
            if hasattr(AlphaMorpho, name) and callable(getattr(AlphaMorpho, name)):
                print("计算中：{}".format(name))
                fac = getattr(self.alpha, name)()
                fac.index = pd.to_datetime(fac.index)
                fac = fac.stack(dropna=False).sort_index().astype('float32')
                used_fac.append(name)
                factor_data.append(fac)
                # try:
                #     print("计算中：{}".format(name))
                #     fac = getattr(self.alpha, name)()
                #     fac.index = pd.to_datetime(fac.index)
                #     fac = fac.stack(dropna=False).sort_index().astype('float32')
                #     used_fac.append(name)
                #     factor_data.append(fac)
                # except:
                #     print(f"函数 {name} 计算时出错")
                #     continue
            else:
                print(f"函数 {name} 未找到")
        factor_data = pd.concat(factor_data,axis=1).sort_index()
        factor_data.columns = used_fac
        return factor_data.astype('float32')
    
    def quick_gen_factor(self,factor_name=None,n_job=8):
        if factor_name is None:
            factor_name = self.factor_name 
            
        def work_func(name):
            if hasattr(AlphaMorpho, name) and callable(getattr(AlphaMorpho, name)):
                try:
                    print("计算中：{}".format(name))
                    fac = getattr(self.alpha, name)()
                    fac.index = pd.to_datetime(fac.index)
                    fac = fac.stack(dropna=False).sort_index().astype('float32')
                    fac.name = name
                    return fac
                except:
                    print(f"函数 {name} 计算时出错")
                    return None
            else:
                print(f"函数 {name} 未找到")
                return None
        
        results = Parallel(n_jobs=n_job)(delayed(work_func)(name) for name in factor_name)
        return results
        
        
        
        