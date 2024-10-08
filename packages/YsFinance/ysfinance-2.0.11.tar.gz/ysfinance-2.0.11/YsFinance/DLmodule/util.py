import torch 
import torch.nn.functional as F
from abc import ABC, abstractmethod
import torch.nn as nn

import pandas as pd
import numpy as np
# from ..stockcalendar import CALENDAR_TOOL
from torch.utils.data import TensorDataset, DataLoader, Dataset,ConcatDataset
import time
import os
import copy
from tqdm import tqdm




class DLmodel(ABC):
    """
    深度学习模型的抽象类, 子类要实现必要的方法.
    
    基类功能:
    - self.__init__():
        -- self.check: 检查GPU资源可用性
        -- self.class_model: DL模型架构
        -- self._model_params(dict): DL模型参数设定
        -- self._dtype: 模型精度，默认float
        -- self.set_params: 设定模型参数，每次调用都会重置模型
    
    - self.check: 检查GPU资源可用性
    - self.set_params: 设定模型参数，每次调用都会重置模型
    - self.save: 存储模型
    
    子类功能:
    - self.train(): 子类必须实现模型的训练功能   
    - self.test(): 子类必须实现模型的测试功能 
    
    """
    
    def __init__(self,model_params:dict,class_model,dtype='float',device_num=0) -> None:
        self.device_num = device_num
        self.check()
        self._state = []
        self.class_model = class_model
        self._model_params:dict = model_params
        self._dtype = dtype
        self.set_params()
    
    def check(self):
        print('CUDA is available:{}'.format(torch.cuda.is_available()))
        print('GPU device count:{}'.format(torch.cuda.device_count()))
        num = torch.cuda.device_count()
        if not torch.cuda.is_available():
            print('Use CPU!!!')
        else:
            for i in range(num):
                print('GPU device name {}:{}'.format(i,torch.cuda.get_device_name(i)))
        if self.device_num >= num:
            raise ValueError('You device is not in the available list!')
            
        self.device = torch.device("cuda:{}".format(self.device_num) if torch.cuda.is_available() else "cpu")
        print("Use the GPU {}!!!!!".format(self.device_num))
        
    def set_params(self):
        if self._dtype == 'float':
            self.model = self.class_model(**self._model_params).float().to(self.device)
        else:
            self.model = self.class_model(**self._model_params).to(self.device)
    
    def r2_score(self,target:torch.tensor,output:torch.tensor):
        # 计算总平方和 (SStot)
        mean_target = torch.mean(target,dim=0)
        total_sum_squares = torch.sum((target - mean_target) ** 2,dim=0)

        # 计算残差平方和 (SSres)
        residual_sum_squares = torch.sum((target - output) ** 2,dim=0)

        # 计算R² score
        r2score = 1 - (residual_sum_squares / total_sum_squares)
        return r2score.item()
    
    def precision(self,y_true:torch.tensor,y_pred:torch.tensor,num:int=None):
        if num is None:
            num = y_pred.max() + 1
        y_true = y_true.view(-1)
        y_pred = y_pred.view(-1)
        
        result = []
        for i in range(num):
            TP = ((y_true == i) & (y_pred == i)).sum().to(torch.float32)  # True Positive
            FP = ((y_true != i) & (y_pred == i)).sum().to(torch.float32)  # False Positive
            FN = ((y_true == i) & (y_pred != i)).sum().to(torch.float32)  # False Negative

            precision = TP / (TP + FP + 1e-6)  # 防止分母为0
            result.append(precision.item())
        return result
    
    def recall(self,y_true:torch.tensor,y_pred:torch.tensor,num:int=None):
        if num is None:
            num = y_pred.max() + 1
        y_true = y_true.view(-1)
        y_pred = y_pred.view(-1)
        
        result = []
        for i in range(num):
            TP = ((y_true == i) & (y_pred == i)).sum().to(torch.float32)  # True Positive
            FN = ((y_true == i) & (y_pred != i)).sum().to(torch.float32)  # False Negative

            recall = TP / (TP + FN + 1e-6)  # 防止分母为0
            result.append(recall.item())
        return result
    
    def accuracy(self,y_true, y_pred):
        y_pred = y_pred.view(-1)
        y_true = y_true.view(-1)

        correct_predictions = torch.sum(y_true == y_pred).item()

        accuracy = correct_predictions / y_true.size(0)
        return accuracy

    def f1_score_macro(self,y_true,y_pred, num:int=None):
        if num is None:
            num = y_pred.max() + 1
        y_true = y_true.view(-1)
        y_pred = y_pred.view(-1)
        
        f1_scores = []
        for i in range(num):
            TP = ((y_true == i) & (y_pred == i)).sum().to(torch.float32)  # True Positive
            FP = ((y_true != i) & (y_pred == i)).sum().to(torch.float32)  # False Positive
            FN = ((y_true == i) & (y_pred != i)).sum().to(torch.float32)  # False Negative

            precision = TP / (TP + FP + 1e-6)  # 防止分母为0
            recall = TP / (TP + FN + 1e-6)  # 防止分母为0
            f1 = 2 * (precision * recall) / (precision + recall + 1e-6)  # 防止分母为0
            f1_scores.append(f1)

        f1_score_macro = torch.mean(torch.tensor(f1_scores)).item()
        return f1_score_macro
    
    def reload_model(self,path):
        self.model = torch.load(path)
            
    
    @abstractmethod
    def train(self):
        raise NotImplementedError("should implement in the derived class")
    
    @abstractmethod
    def test(self):
        raise NotImplementedError("should implement in the derived class")
    
    
    def save(self,path):
        self.model.eval()
        torch.save(self.model.to(self.device),path)
        
    def save_state(self):
        self._state.append(copy.deepcopy(self.model.state_dict()))
    
    def reset_state(self,state):
        self.model.load_state_dict(state, strict=True)
    
    def ave_state(self,window=3,skip=1):
        if len(self._state) == 0:
            raise ValueError("None state in self._state, ensure you use the function to save them after train.")
        if len(self._state) < window:
            print("The length of self._state < window, the average will be restricted to the existing state list!")
        averaged_params = {}
        used_params = self._state[-window:].copy()
        used_params.reverse()
        used_params = used_params[::skip]
        # 遍历所有保存的参数
        for param_name in used_params[0].keys():
            # 初始化参数总和
            param_sum = torch.zeros_like(used_params[0][param_name])
            
            # 累加每个周期的参数
            for params in used_params:
                param_sum += params[param_name]
            
            # 计算平均值
            averaged_params[param_name] = param_sum / len(used_params)
        return averaged_params


class ClassifyModelFrame(DLmodel):
    """
    Introduce:
        基于分类DL模型的训练和测试框架
    
    Function:
    - __init__:提供你的模型设计和模型参数设定，会自动帮你生成和存储模型，继承DLmodel方法
    - train: 基础的训练框架，请根据你的需要输出一些你的监控指标和不同的批次生成方式
    - test: 提供你的测试集数据，输出预测结果，防止内存不足提供根据一定的批量分批预测的方式。
    """
    def __init__(self, model_params: dict, class_model, dtype='float') -> None:
        super().__init__(model_params, class_model, dtype)
    
    def train(self,dataset,EPOCHS,batch_size=512,shuffle=True,lr=0.001,gap=[-0.005,0.005]):
        gap = torch.tensor(gap).to(self.device)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
        loss_func = nn.CrossEntropyLoss()
        optim = torch.optim.Adam(self.model.parameters(),lr=lr)
        
        for epoch in range(EPOCHS):
            self.model.train()

            for batch_idx, (data,target) in enumerate(dataloader):
                data = data.float().to(self.device)
                target = target.float().to(self.device)
                label = target.reshape(-1)
                label = torch.bucketize(label,gap)
                
                optim.zero_grad()
                output = self.model(data)
                
                l = loss_func(output,label)

                l.backward()
                optim.step()
                
                if batch_idx % 50 == 0:
                    print("train epoch:{}, batch_idx:{}".format(epoch,batch_idx))
            
            
            print("FINISH: train epoch:{}".format(epoch))
            print("")

        return 1
    
    
    def test(self,data:torch.tensor,model,batch_size=1024):
        model = model.to(self.device)
        result = []
        with torch.no_grad():
            model.eval()
            for i in range(0,data.shape[0],batch_size):
                feature = data[i:i+batch_size].float().to(self.device)
                label = F.softmax(model(feature),dim=1).cpu().detach().numpy()
                result.append(label)
        result = np.vstack(result)
        return result
    
    
    
class RegresionModelFrame(DLmodel):
    
    """
    Introduce:
        基于回归DL模型的训练和测试框架
    
    Function:
    - __init__:提供你的模型设计和模型参数设定，会自动帮你生成和存储模型，继承DLmodel方法
    - train: 提供你的训练数据集，批次大小，训练轮次，早停条件，学习率等，回归训练以R2score达标作为早停条件
    - test: 提供你的测试集数据，和同样顺序的index
    """
    
    def __init__(self, model_params, class_model,dtype='float') -> None:
        super().__init__(model_params, class_model, dtype)
        
    def train(self,dataset,EPOCHS,batch_size=512,scale=1,shuffle=True,loss='Huber', lr=0.001):
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
        
        if loss == 'Huber':
            loss_func = nn.HuberLoss()
        elif loss == 'L1':
            loss_func = nn.L1Loss()
        elif loss == 'MSE': 
            loss_func = nn.MSELoss()
        else:
            loss_func = nn.MSELoss()

        
        optim = torch.optim.Adam(self.model.parameters(),lr=lr)

        for epoch in range(EPOCHS):
            self.model.train()
            for batch_idx, (data,target) in enumerate(dataloader):
                
                data = data.float().to(self.device)
                target = target.float().to(self.device)*scale
                optim.zero_grad()
                output = self.model(data)
                
                l = loss_func(output,target)
                
                l.backward()
                
                optim.step()
                
                if batch_idx % 50 == 0:
                    print("train epoch:{}, batch_idx:{}".format(epoch+1,batch_idx))
            
            print("FINISH: train epoch:{}".format(epoch))
            print("")
        
        return 1
    
    def test(self,data:torch.tensor,model,batch_size=2048):
        model = model.cuda()
        result = []
        with torch.no_grad():
            model.eval()
            for i in range(0,data.shape[0],batch_size):
                feature = data[i:i+batch_size].float().to(self.device)
                label = model(feature).cpu().detach().numpy()
                result.append(label)
        result = np.vstack(result)
        return result
    



class StockDataset(Dataset):
    """
    时序dataset, 截面特征set num_feature_times = 1, then 处理 dimension in the neural network
    """

    def __init__(self, features, label=None, num_feature_times=1, is_train=True, feature_stan=None,classify=None):
        """
        feature: index=(date,feature), columns=stock
        label: index = date, columns=stock
        num_feature_times: 时序长度
        is_train: 是否为训练集
        classify: pd.Series. index=(date,asset), values = 类别标签 
        """
        self.dates = features.index.get_level_values(0).unique()
        self.features = features
        self.label = label
        self.num_feature_times = num_feature_times
        self.is_train = is_train
        self.num_features = len(self.features.loc[self.dates[0]])
        self.feature_stan = feature_stan
        self.classify = classify

    def __len__(self):
        return len(self.dates) - self.num_feature_times + 1

    def convert_to_3d_numpy(self, df, label=None,facnum=46,classify_map:pd.Series=None):
        df: pd.DataFrame = df.dropna(axis=1)  ## index = (date,features), columns=stock
        if self.is_train:
            if label is None:
                raise ValueError("when you set is_train==True, you should provide label")
            label = label.dropna()
            
            assets_feature = set(df.columns)
            assets_label = set(label.index)
            assets = list(assets_feature & assets_label)
            assets.sort()
            
            df = df[assets]
            label = label.loc[assets]
        else:
            assets = list(df.columns)
        
        # 获取形状信息
        num_stocks = len(assets)
        np_array = df.to_numpy()
        
        if classify_map is not None:
            classify_matrix = self.classify_matrix(classify_map)
            r_matrix = classify_matrix.loc[assets].values
            r_matrix = r_matrix @ r_matrix.T
            r_matrix = r_matrix/r_matrix.sum(axis=1,keepdims=True)
            comm_features = r_matrix @ np_array.T
            if facnum is None:
                comm_features = comm_features.reshape(
                    num_stocks, self.num_feature_times, self.num_features
                )
            else:
                comm_features = comm_features.reshape(
                    num_stocks, self.num_feature_times, self.num_features
                )[:,:,:facnum]

        # 重塑数组为[N, T, F]
        features = np_array.T.reshape(
            num_stocks, self.num_feature_times, self.num_features
        )
        
        if classify_map is not None:
            ### 若有行业, 则拼接为[N,T,F+facnum]
            features = np.concatenate([features,comm_features],axis=2)
        if self.feature_stan == "panel":
            features = self.panel_stan(features) ## 轴1不动，沿着特征，将time*stock矩阵做标准化，并用0值填充空缺值
        elif self.feature_stan == "two-step":
            features = self.two_step_stan(features) ## 先对时序除以平均值，再沿股票做标准
        
             

        if self.is_train:
            labels = label.values
            return assets, features, labels
        else:
            return assets, features

    def panel_stan(self, matrix):
        mean = np.nanmean(matrix, axis=(0, 1), keepdims=True)
        std = np.nanstd(matrix, axis=(0, 1), keepdims=True)
        return np.nan_to_num((matrix - mean) / std)

    def two_step_stan(self, matrix):
        # divided by timeseries mean and then cross-sectional zscore
        ts_mean = np.nanmean(matrix, axis=1, keepdims=True)
        matrix /= ts_mean
        cs_mean = np.nanmean(matrix, axis=0, keepdims=True)
        cs_std = np.nanstd(matrix, axis=0, keepdims=True)
        return np.nan_to_num((matrix - cs_mean) / cs_std)
    
    def classify_matrix(self,industry:pd.Series):
        """
        根据index为asset,value为类别的Series生成01的DataFrame(index=asset,columns=classify)
        """
        industry.index.name = 'asset'
        industry.name = 'industry'
        industry:pd.DataFrame = industry.reset_index()
        industry['is_true'] = 1
        industry = industry.pivot(index='asset',columns='industry',values='is_true').fillna(0)
        return industry

    def __getitem__(self, idx):
        start_date = self.dates[idx]
        end_date = self.dates[idx + self.num_feature_times - 1]
        if self.classify is None:
            classify_map = None
        else:
            classify_map = self.classify.loc[end_date]
        if self.is_train:
            label = self.label.loc[end_date].dropna()
            stocks, features, labels = self.convert_to_3d_numpy(
                self.features.loc[start_date:end_date],label,classify_map=classify_map,
            )
            return end_date, stocks, features, labels
        else:
            stocks, features = self.convert_to_3d_numpy(
                self.features.loc[start_date:end_date],label=None,classify_map=classify_map,
            )
            return end_date, stocks, features

    @staticmethod
    def data_wash(factor,cols=None):
        """
        factor: pd.DataFrame. index=(date,asset)
        cols: list.指定你需要的因子或者排列顺序, 默认使用全部因子.
        """
        if cols is not None:
            factor = factor[cols]
        factor = factor.swaplevel().sort_index()
        factor = factor.groupby(level=0).ffill(limit=3)
        factor = factor.dropna(how='all')
        factor = factor.unstack(level=1).T
        factor = factor.swaplevel().sort_index()
        return factor

class StockDataLoader(DataLoader):
    """
    custom stock market dataloader, 每个batch只包含单日全部股票
    """

    def __init__(
        self,
        df,
        label=None,
        is_train=True,
        feature_stan=None,
        num_feature_times=1,
        batch_size=1,
        shuffle=False,
        num_workers=0,
        industry=None,
    ):
        dataset = StockDataset(
            df,
            label,
            num_feature_times=num_feature_times,
            is_train=is_train,
            feature_stan=feature_stan,
            industry=industry,
        )

        self.is_train = is_train

        super().__init__(
            dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=num_workers,
            collate_fn=self.collate_fn,
        )

    def collate_fn(self, batch):
        if self.is_train:
            date, stocks, features, labels = zip(*batch)
            features = torch.tensor(features[0], dtype=torch.float)
            labels = torch.tensor(labels[0], dtype=torch.float)
            return date[0], stocks[0], features, labels
        else:
            date, stocks, features = zip(*batch)
            features = torch.tensor(features[0], dtype=torch.float)
            return date[0], stocks[0], features


if __name__ == "__main__":
    pass


def gen_train_dataloader(df,label,dataset_path,num_feature_times,batch_size,shuffle=True,hard_stop=50,industry=None):
    """维护一个不大于hard_stop GB 的数据集文件夹，以数据生成点的日期命名文件，大于hard_stop强制停止工作，df和label格式与StockDataset格式相同"""
    def bytes_to_GB(num):
        return round(num/1073741824,3)

    def file_size(path):
        file_lst = os.listdir(path)
        total = 0
        for name in file_lst:
            total += os.path.getsize(path+'/' + name)
        return bytes_to_GB(total)
    print("Gen train dataloader.......")
    t1 = time.time()
    stock_dataset = StockDataset(df,label,is_train=True,num_feature_times=num_feature_times,classify=industry)
        
    ### 删除无用数据集
    exist_dataset = os.listdir(dataset_path)
    use_dataset = list(map(lambda x: 'dataset.train.'+x.strftime("%Y%m%d"),stock_dataset.dates[num_feature_times-1:]))
    for name in exist_dataset:
        if name not in use_dataset:
            os.remove(dataset_path+'/'+name)
    
    ### 生成使用的数据集
    exist_dataset = os.listdir(dataset_path)
    print("生成：")
    for idx in tqdm(range(len(stock_dataset))):
        ed =  stock_dataset.dates[idx+num_feature_times-1]
        ed = ed.strftime('%Y%m%d')
        if 'dataset.train.'+ed in exist_dataset:
            continue
        
        _, _, features, labels = stock_dataset.__getitem__(idx)
        features = torch.tensor(features).float()
        labels = torch.tensor(labels).float()
        dataset = TensorDataset(features,labels)
        torch.save(dataset,dataset_path + '/' + 'dataset.train.{}'.format(ed))
        test_size = file_size(dataset_path)
        if test_size > hard_stop:
            raise ValueError("file size is {}GB > hard_stop {}GB, Stop it!".format(test_size,hard_stop))
    print("    dataset_path file size is {} GB".format(file_size(dataset_path)))           
    ### 生成训练用数据集和dataloader
    exist_dataset = os.listdir(dataset_path)
    datasets = []
    print("合并：")
    for name in tqdm(exist_dataset):
        datasets.append(torch.load(dataset_path+'/'+name))
    train_dataset = ConcatDataset(datasets)
    dataloader = DataLoader(train_dataset,batch_size=batch_size,shuffle=shuffle,num_workers=12)
    t2 = time.time()
    print("    gen time: {}".format(round(t2-t1,2)))
    return dataloader
    
    
    











# trade_dates = CALENDAR_TOOL.trade_date_in_range(start_date='20010101',end_date='20261201').copy(deep=True)

# class ByTimeDataLoader:
#     """
#     每回遍历不重复的从data_set中跳出一个数据点
#     """
#     def __init__(self, data_set, data_range=None):
#         """
#         初始化迭代器
#         :param data_set: 数据集，列表形式
#         :param data_range: 生成随机数据的范围，默认为data_set的列表长度
#         """
#         self.data_set = data_set
#         if data_range == None:
#             self.data_range = len(data_set)
#         else:
#             self.data_range = data_range
#         self.current_batch = 0
#         self.random_shuffle = [_ for _ in range(self.data_range)]
#         random.shuffle(self.random_shuffle)
    
#     def reset(self):
#         random.shuffle(self.random_shuffle)
#         self.current_batch = 0

#     def __iter__(self):
#         """返回迭代器对象本身"""
#         return self

#     def __next__(self):
#         """生成下一个随机批量的数据"""
#         if self.current_batch < self.data_range:
#             batch_data = self.data_set[self.random_shuffle[self.current_batch]]
#             self.current_batch += 1
#             return batch_data
#         else:
#             self.reset()
#             raise StopIteration  # 如果所有批次都已经生成，则停止迭代    

# class GenDataSet:
#     """
#     用于生成各种类型数据集的类函数
#     """
    
#     @staticmethod
#     def base_train_dataset(factor,price,dates,seq_len,forward,dropmid=None,dtype='float',assets=None):
#         """
#         Params:
#         -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
#         -price: pd.DataFrame. index=date, columns = asset
#         -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
#         -seq_len: int. 获取的因子矩阵的时序长度
#         -forward: int. 获取的未来收益率长度
#         -dropmid=None: float. 在进行标签筛选时是否扔掉中间的部分数据
#         -dtype='float': str. 生成的数据集数据类型
        
#         Return:
#         (index,dataset): 与dataset相对应的index, 方便直接使用训练集输出测试预测因子
        
#         Attention: 
#         - 建议你提供的数据相对于时间点来说要足够长, 否则会丢弃很多长度不够的数据点。
#         - 对于时间点前seqlen长度的数据，若空缺比例超过0.1会丢弃该数据点，所以请在因子输入时dropna
#         """
#         seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
#         if assets is None:
#             assets = list(set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
#         else:
#             assets = list(set(list(assets)) & set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
#         price = price[assets]
        
        
#         def single_point(asset,date,seq_len):
#             pre_date = seek_backward_dates.loc[date]
#             df = factor.loc[asset].loc[pre_date:date]
            
#             if len(df) < seq_len*0.9:
#                 return None
#             else:
#                 df = factor.loc[asset].loc[:date].iloc[-seq_len:].values
#                 if len(df) != seq_len:
#                     return None
#                 return ((asset,date),df)
        
#         X_ = []
#         y_ = []
        
#         index = []
        
#         def drop_mid_Series(sr:Series,dropmid):
#             sr = sr.sort_values()
#             l = len(sr)
#             if l < 100:
#                 return sr
#             return pd.concat([sr.iloc[:int(l*(1/2-dropmid/2))],sr.iloc[int(l*(1/2+dropmid/2)):]])
        
#         forward_returns = (price.shift(-forward)/price - 1)
#         for date in dates:
#             y:Series = forward_returns.loc[date].dropna()
#             if len(y) == 0:
#                 continue
#             if dropmid is not None:
#                 y = drop_mid_Series(y,dropmid)
#             for asset in y.index:
#                 dv = single_point(asset,date,seq_len)
#                 if dv is None:
#                     continue
                
#                 X_.append(dv[1])
#                 y_.append(y.loc[asset])
#                 index.append(dv[0])

#         if dtype == 'float':
#             X_ = torch.tensor(np.array(X_)).float()
#             y_ = torch.tensor(np.array(y_)).reshape(len(y_),-1).float()
#         else:
#             X_ = torch.tensor(np.array(X_))
#             y_ = torch.tensor(np.array(y_)).reshape(len(y_),-1)
            
#         index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
#         return (index,TensorDataset(X_,y_))
    
    
    # @staticmethod
    # def market_train_dataset(factor,price,market,dates,seq_len,forward,dropmid=None,dtype='float',droptop=None):
    #     """
    #     Params:
    #     -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
    #     -price: pd.DataFrame. index=date, columns = asset
    #     -market: pd.Series. index=date, 你需要额外提供一个市场数据(收盘价)，标签将会是超市场收益
    #     -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
    #     -seq_len: int. 获取的因子矩阵的时序长度
    #     -forward: int. 获取的未来收益率长度
    #     -dropmid=None: float. 在进行标签筛选时是否扔掉中间的部分数据
    #     -dtype='float': str. 生成的数据集数据类型
        
    #     Return:
    #     (index,dataset): 与dataset相对应的index, 方便直接使用训练集输出测试预测因子
    #     """
    #     seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
    #     def single_point(asset,date,seq_len):
    #         pre_date = seek_backward_dates.loc[date]
    #         df = factor.loc[asset].loc[pre_date:date]
    #         if len(df) < seq_len*0.9:
    #             return None
    #         else:
    #             df = factor.loc[asset].loc[:date].iloc[-seq_len:].values
    #             if len(df) != seq_len:
    #                 return None
    #             return ((asset,date),df)
        
    #     X_ = []
    #     y_ = []
        
    #     index = []
        
    #     def drop_mid_Series(sr:Series,dropmid):
    #         sr = sr.sort_values()
    #         l = len(sr)
    #         if l < 100:
    #             return sr
    #         return pd.concat([sr.iloc[:int(l*(1/2-dropmid/2))],sr.iloc[int(l*(1/2+dropmid/2)):]])
        
    #     def drop_top_Series(sr:Series,droptop):
    #         sr = sr.sort_values()
    #         l = len(sr)
    #         if l < 100:
    #             return sr
    #         return sr.iloc[:int(l*(1-droptop))]
        
    #     forward_returns:DataFrame = (price.shift(-forward)/price - 1)
    #     forward_market = (market.shift(-forward)/market - 1)
    #     forward_exceed = forward_returns.subtract(forward_market,axis=0)
    #     for date in dates:
    #         y:Series = forward_exceed.loc[date].dropna()
    #         if len(y) == 0:
    #             continue
    #         if dropmid is not None:
    #             y = drop_mid_Series(y,dropmid)
    #         if droptop is not None:
    #             y = drop_top_Series(y,droptop)
    #         for asset in y.index:
    #             dv = single_point(asset,date,seq_len)
    #             if dv is None:
    #                 continue
                
    #             X_.append(dv[1])
    #             y_.append(y.loc[asset])
    #             index.append(dv[0])

    #     if dtype == 'float':
    #         X_ = torch.tensor(np.array(X_)).float()
    #         y_ = torch.tensor(np.array(y_)).reshape(len(y_),-1).float()
    #     else:
    #         X_ = torch.tensor(np.array(X_))
    #         y_ = torch.tensor(np.array(y_)).reshape(len(y_),-1)
            
    #     index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
    #     return (index,TensorDataset(X_,y_))
    
    
    # @staticmethod
    # def seq_train_dataset(factor,price,dates,seq_len,forward,assets=None,dtype='float'):
    #     """
    #     Params:
    #     -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
    #     -price: pd.DataFrame. index=date, columns = asset
    #     -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
    #     -seq_len: int. 获取的因子矩阵的时序长度
    #     -forward: int. 获取的未来收益率长度
    #     -dtype='float': str. 生成的数据集数据类型
        
    #     Return:
    #     (index,dataset): 你得到的标签将会是forward长度的收益率序列，而非单个收益率.与dataset相对应的index, 方便直接使用训练集输出测试预测因子.
    #     """
    #     if assets is None:
    #         assets = list(set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
    #     else:
    #         assets = list(set(list(assets)) & set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
    #     price = price[assets]
        
        
    #     seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
    #     def single_point(asset,date,seq_len):
    #         pre_date = seek_backward_dates.loc[date]
    #         df = factor.loc[asset].loc[pre_date:date]
    #         if len(df) < seq_len*0.9:
    #             return None
    #         else:
    #             df = factor.loc[asset].loc[:date].iloc[-seq_len:].values
    #             if len(df) != seq_len:
    #                 return None
    #             return ((asset,date),df)
        
    #     X_ = []
    #     y_ = []
        
    #     index = []
    #     returns = price/price.shift(1)-1
    #     forward_returns = (price.shift(-forward)/price - 1)
    #     for date in dates:
    #         y = returns.loc[date:].iloc[1:forward+1].T.dropna()
    #         if len(y) == 0:
    #             continue
    #         for asset in y.index:
    #             dv = single_point(asset,date,seq_len)
    #             if dv is None:
    #                 continue
                
    #             X_.append(dv[1])
    #             y_.append(y.loc[asset].values)
    #             index.append(dv[0])

    #     if dtype == 'float':
    #         X_ = torch.tensor(np.array(X_)).float()
    #         y_ = torch.tensor(np.array(y_)).float()
    #     else:
    #         X_ = torch.tensor(np.array(X_))
    #         y_ = torch.tensor(np.array(y_))
            
    #     index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
    #     return (index,TensorDataset(X_,y_))
    
    # @staticmethod
    # def Seq_train_dataset(factor,price,dates,seq_len,forward:int=7,dtype='float',assets=None):
    #     """
    #     Introduce:
    #     获得标签为未来forward日的数据序列的数据集，要保证factor已经dropna，空缺日期比例超过10%则丢弃该数据点
        
    #     Params:
    #     -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
    #     -price: pd.DataFrame. index=date, columns = asset
    #     -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
    #     -seq_len: int. 获取的因子矩阵的时序长度
    #     -forward: int. 获取的未来收益率长度, 输出的标签为未来forward天的收益率序列，可以构造夏普比等特殊标签
    #     -dropmid=None: float. 在进行标签筛选时是否扔掉中间的部分数据
    #     -dtype='float': str. 
    #     -assets=None: list. 提供你筛选后的股票，如果没有则默认为price表提供的股票
        
    #     Return:
    #     (index,dataset): 与dataset相对应的index, 方便直接使用训练集输出测试预测因子
        
    #     Attention: 
    #     - 建议你提供的数据相对于时间点来说要足够长, 否则会丢弃很多长度不够的数据点。
    #     - 对于时间点前seqlen长度的数据，若空缺比例超过0.1会丢弃该数据点，所以请在因子输入时dropna
    #     """
    #     seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
    #     if assets is None:
    #         assets = list(set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
    #     else:
    #         assets = list(set(list(assets)) & set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
    #     price:DataFrame = price[assets]
    #     returns = price.pct_change()
        
    #     def single_point(asset,date,seq_len):
    #         pre_date = seek_backward_dates.loc[date]
            
    #         df = factor.loc[asset].loc[:date]
    #         test_df = df.loc[pre_date:]
    #         if len(test_df) < seq_len*0.9:
    #             return None
    #         else:
    #             df = df.iloc[-seq_len:].values
    #             if np.isnan(df).sum() > 0:
    #                 return None
    #             if len(df) != seq_len:
    #                 return None
    #             return ((asset,date),df)
        
    #     X_ = []
    #     label = []

    #     index = []
    #     forward_returns = []
    #     for i in range(forward):
    #         forward_returns.append(returns.shift(-i-1).stack(dropna=False))
    #     forward_returns = pd.concat(forward_returns,axis=1).sort_index()
    #     for date in dates:
    #         y_ = forward_returns.loc[date].dropna()
    #         if len(y_) == 0:
    #             continue
    #         for asset in y_.index:
    #             dv = single_point(asset,date,seq_len)
    #             if dv is None:
    #                 continue
                
    #             X_.append(dv[1])
    #             label.append(y_.loc[asset].values)
    #             index.append(dv[0])

    #     if dtype == 'float':
    #         X_ = torch.tensor(np.array(X_)).float()
    #         label = torch.tensor(np.array(label)).float()
    #     else:
    #         X_ = torch.tensor(np.array(X_)).float()
    #         label = torch.tensor(np.array(label)).float()
            
    #     index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
    #     return (index,TensorDataset(X_,label))
    
    
    # def None_train_dataset(factor,price,dates,seq_len,forward,none_num=None,dropmid=None,dtype='float',assets=None):
    #     """
    #     Introduce:
    #     主要添加了空缺值的处理逻辑，同时尽量不损失数据，空缺比例高于10%则丢弃，否则用ffill填补空缺值.
        
    #     Params:
    #     -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
    #     -price: pd.DataFrame. index=date, columns = asset
    #     -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
    #     -seq_len: int. 获取的因子矩阵的时序长度
    #     -forward: int. 获取的未来收益率长度
    #     -dropmid=None: float. 在进行标签筛选时是否扔掉中间的部分数据
    #     -dtype='float': str. 
    #     -assets=None: list. 提供你筛选后的股票，如果没有则默认为price表提供的股票
    #     -none_num: Serier. 提供因子每一行是否有空缺值的bool值Series，不提供会内部计算，有点慢.
        
    #     Return:
    #     (index,dataset): 与dataset相对应的index, 方便直接使用训练集输出测试预测因子
        
    #     Attention: 
    #     - 建议你提供的数据相对于时间点来说要足够长, 否则会丢弃很多长度不够的数据点。
    #     """
    #     seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
    #     if assets is None:
    #         assets = list(set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
    #     else:
    #         assets = list(set(list(assets)) & set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
    #     price = price[assets]
    #     if none_num is None:
    #         none_num = factor.isna().sum(axis=1)>0
        
        
    #     def single_point(asset,date,seq_len):
    #         pre_date = seek_backward_dates.loc[date]
    #         n = none_num.loc[asset].loc[pre_date:date]
            
    #         if n.sum() > seq_len*0.1:
    #             return None
    #         else:
    #             df = factor.loc[asset].loc[:date].ffill().iloc[-seq_len:].values
    #             if np.isnan(df).sum() > 0:
    #                 return None
    #             if len(df) != seq_len:
    #                 return None
    #             return ((asset,date),df)
        
    #     X_ = []
    #     y_ = []
        
    #     index = []
        
    #     def drop_mid_Series(sr:Series,dropmid):
    #         sr = sr.sort_values()
    #         l = len(sr)
    #         if l < 100:
    #             return sr
    #         return pd.concat([sr.iloc[:int(l*(1/2-dropmid/2))],sr.iloc[int(l*(1/2+dropmid/2)):]])
        
    #     forward_returns = (price.shift(-forward)/price - 1)
    #     for date in dates:
    #         y:Series = forward_returns.loc[date].dropna()
    #         if len(y) == 0:
    #             continue
    #         if dropmid is not None:
    #             y = drop_mid_Series(y,dropmid)
    #         for asset in y.index:
    #             dv = single_point(asset,date,seq_len)
    #             if dv is None:
    #                 continue
                
    #             X_.append(dv[1])
    #             y_.append(y.loc[asset])
    #             index.append(dv[0])

    #     if dtype == 'float':
    #         X_ = torch.tensor(np.array(X_)).float()
    #         y_ = torch.tensor(np.array(y_)).reshape(len(y_),-1).float()
    #     else:
    #         X_ = torch.tensor(np.array(X_))
    #         y_ = torch.tensor(np.array(y_)).reshape(len(y_),-1)
            
    #     index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
    #     return (index,TensorDataset(X_,y_))
    
    
    # @staticmethod
    # def Multi_None_train_dataset(factor,price,dates,seq_len,forward=(1,3,5,10),none_num=None,dtype='float',assets=None):
    #     """
    #     Introduce:
    #     主要添加了空缺值的处理逻辑，同时尽量不损失数据，空缺比例高于10%则丢弃，否则用ffill填补空缺值. 得到的标签则是多个未来区间的收益率，用于不同长度的预测。
        
    #     Params:
    #     -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
    #     -price: pd.DataFrame. index=date, columns = asset
    #     -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
    #     -seq_len: int. 获取的因子矩阵的时序长度
    #     -forward: tuple. 获取的未来收益率长度, 可接受多个时间按长度，最后输出的标签每一列都是不同forward的数据
    #     -dropmid=None: float. 在进行标签筛选时是否扔掉中间的部分数据
    #     -dtype='float': str. 
    #     -assets=None: list. 提供你筛选后的股票，如果没有则默认为price表提供的股票
    #     -none_num: Serier. index=pd.MultiIndex, level0 = asset, level1 = date. 提供因子每一行是否有空缺值的bool值Series，不提供会内部计算，有点慢.
        
    #     Return:
    #     (index,dataset): 与dataset相对应的index, 方便直接使用训练集输出测试预测因子
        
    #     Attention: 
    #     - 建议你提供的数据相对于时间点来说要足够长, 否则会丢弃很多长度不够的数据点。
    #     """
    #     seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
    #     if assets is None:
    #         assets = list(set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
    #     else:
    #         assets = list(set(list(assets)) & set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
    #     price = price[assets]
    #     if none_num is None:
    #         none_num = factor.isna().sum(axis=1)>0
        
        
    #     def single_point(asset,date,seq_len):
    #         pre_date = seek_backward_dates.loc[date]
    #         n = none_num.loc[asset].loc[pre_date:date]
            
    #         if n.sum() > seq_len*0.1:
    #             return None
    #         else:
    #             df = factor.loc[asset].loc[:date].ffill().iloc[-seq_len:].values
    #             if np.isnan(df).sum() > 0:
    #                 return None
    #             if len(df) != seq_len:
    #                 return None
    #             return ((asset,date),df)
        
    #     X_ = []
    #     label = []

    #     index = []
        
    #     forward_returns = []
    #     for fw in forward:
    #         forward_returns.append((price.shift(-fw)/price - 1))
        
    #     for date in dates:
    #         y_ = []
    #         for i in range(len(forward_returns)):
    #             y_.append(forward_returns[i].loc[date])
    #         y_ = pd.concat(y_,axis=1).dropna()
    #         if len(y_) == 0:
    #             continue
    #         for asset in y_.index:
    #             dv = single_point(asset,date,seq_len)
    #             if dv is None:
    #                 continue
                
    #             X_.append(dv[1])
    #             label.append(y_.loc[asset].values)
    #             index.append(dv[0])

    #     if dtype == 'float':
    #         X_ = torch.tensor(np.array(X_)).float()
    #         label = torch.tensor(np.array(label)).float()
    #     else:
    #         X_ = torch.tensor(np.array(X_)).float()
    #         label = torch.tensor(np.array(label)).float()
            
    #     index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
    #     return (index,TensorDataset(X_,label))
    
    # @staticmethod
    # def Seq_None_train_dataset(factor,price,dates,seq_len,forward:int=7,none_num=None,dtype='float',assets=None):
    #     """
    #     Introduce:
    #     主要添加了空缺值的处理逻辑，同时尽量不损失数据，空缺比例高于10%则丢弃，否则用ffill填补空缺值. 得到的标签是未来forward日的收益率序列，用于更加复杂的标签构造分析。
        
    #     Params:
    #     -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
    #     -price: pd.DataFrame. index=date, columns = asset
    #     -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
    #     -seq_len: int. 获取的因子矩阵的时序长度
    #     -forward: int. 获取的未来收益率长度, 输出的标签为未来forward天的收益率序列，可以构造夏普比等特殊标签
    #     -dropmid=None: float. 在进行标签筛选时是否扔掉中间的部分数据
    #     -dtype='float': str. 
    #     -assets=None: list. 提供你筛选后的股票，如果没有则默认为price表提供的股票
    #     -none_num: Serier. index=pd.MultiIndex, level0 = asset, level1 = date. 提供因子每一行是否有空缺值的bool值Series，不提供会内部计算，有点慢.
        
    #     Return:
    #     (index,dataset): 与dataset相对应的index, 方便直接使用训练集输出测试预测因子
        
    #     Attention: 
    #     - 建议你提供的数据相对于时间点来说要足够长, 否则会丢弃很多长度不够的数据点。
    #     - 对于时间点前seqlen长度的数据，若空缺比例超过0.1会丢弃该数据点，所以请在因子输入时dropna
    #     """
    #     seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
    #     if assets is None:
    #         assets = list(set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
    #     else:
    #         assets = list(set(list(assets)) & set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
    #     price:DataFrame = price[assets]
    #     returns = price.pct_change()
    #     if none_num is None:
    #         none_num = factor.isna().sum(axis=1)>0
        
        
    #     def single_point(asset,date,seq_len):
    #         pre_date = seek_backward_dates.loc[date]
    #         n = none_num.loc[asset].loc[pre_date:date]
            
    #         if n.sum() > seq_len*0.1:
    #             return None
    #         else:
    #             df = factor.loc[asset].loc[:date].ffill().iloc[-seq_len:].values
    #             if np.isnan(df).sum() > 0:
    #                 return None
    #             if len(df) != seq_len:
    #                 return None
    #             return ((asset,date),df)
        
    #     X_ = []
    #     label = []

    #     index = []
    #     forward_returns = []
    #     for i in range(forward):
    #         forward_returns.append(returns.shift(-i-1).stack(dropna=False))
    #     forward_returns = pd.concat(forward_returns,axis=1).sort_index()
    #     for date in dates:
    #         y_ = forward_returns.loc[date].dropna()
    #         if len(y_) == 0:
    #             continue
    #         for asset in y_.index:
    #             dv = single_point(asset,date,seq_len)
    #             if dv is None:
    #                 continue
                
    #             X_.append(dv[1])
    #             label.append(y_.loc[asset].values)
    #             index.append(dv[0])

    #     if dtype == 'float':
    #         X_ = torch.tensor(np.array(X_)).float()
    #         label = torch.tensor(np.array(label)).float()
    #     else:
    #         X_ = torch.tensor(np.array(X_)).float()
    #         label = torch.tensor(np.array(label)).float()
            
    #     index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
    #     return (index,TensorDataset(X_,label))