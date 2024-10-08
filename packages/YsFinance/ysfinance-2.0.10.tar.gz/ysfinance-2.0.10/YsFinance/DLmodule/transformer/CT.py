import torch.nn as nn
import torch.nn.functional as F
import torch

import numpy as np
import pandas as pd
from pandas import Series,DataFrame

from torch.utils.data import TensorDataset, DataLoader

from math import log

from ..util import DLmodel
from ...stockcalendar import CALENDAR_TOOL


trade_dates = CALENDAR_TOOL.trade_date_in_range(start_date='20010101',end_date='20241201').copy(deep=True)




class BlockConvBase(nn.Module):
    
    def __init__(self, in_channels, out_channels, kernel_size):
        super(BlockConvBase,self).__init__()
        self.conv = nn.Conv2d(in_channels,out_channels,kernel_size)
    def forward(self,x):
        x = self.conv(x).squeeze(3).permute(0,2,1)
        return x


class BlockConvMax(nn.Module):
    
    def __init__(self,in_channels,out_channels,kernel_size) -> None:
        super(BlockConvMax,self).__init__()
        
        self.conv = nn.Conv2d(in_channels,out_channels,kernel_size)
        self.maxpool = nn.MaxPool2d((kernel_size[0],1),stride=1)
        # self.conv3 = nn.Conv2d(10,20,kernel_size=(5,5),padding=2)
        
    def forward(self,x):
        x = self.conv(x)
        x = self.maxpool(x).squeeze(3).permute(0,2,1)
        return x
    

class BlockConvAve(nn.Module):
    
    def __init__(self,in_channels,out_channels,kernel_size) -> None:
        super(BlockConvAve,self).__init__()
        
        self.conv = nn.Conv2d(in_channels,out_channels,kernel_size)
        self.avepool = nn.AvgPool2d((kernel_size[0],1),stride=1)
        # self.conv3 = nn.Conv2d(10,20,kernel_size=(5,5),padding=2)
        
    def forward(self,x):
        x = self.conv(x)
        x = self.avepool(x).squeeze(3).permute(0,2,1)
        return x
    


class BlockConvCross(nn.Module):
    
    def __init__(self,in_channels,out_channels,kernel_size) -> None:
        super(BlockConvCross,self).__init__()
        
        self.conv1 = nn.Conv2d(in_channels,out_channels,kernel_size)
        self.conv2 = nn.Conv2d(out_channels,out_channels,kernel_size)
        self.avepool1 = nn.AvgPool2d((kernel_size[0],1),stride=1)
        self.avepool2 = nn.AvgPool2d((kernel_size[0],1),stride=1)
        
    def forward(self,x):
        x = self.conv1(x)
        x = self.avepool1(x)
        x = self.conv2(x)
        x = self.avepool2(x)
        x = x.permute(0,2,1,3).reshape(x.shape[0],x.shape[2],-1)
        return x
 
class ConvFeatureGet0(nn.Module):
    
    def __init__(self, base_seq_len, base_dim, out_seq_len):
        super(ConvFeatureGet0,self).__init__()
        if base_seq_len < 140:
            raise ValueError("the seq_len should be >= 140 !!!!")
        self.out_seq_len = out_seq_len
        self.base_dim = base_dim
        
        self.conv_base1 = BlockConvBase(in_channels=1,out_channels=3,kernel_size=(1,self.base_dim))
        self.conv_base2 = BlockConvBase(in_channels=1,out_channels=3,kernel_size=(2,self.base_dim))
        self.conv_base3 = BlockConvBase(in_channels=1,out_channels=3,kernel_size=(3,self.base_dim))
        self.conv_base4 = BlockConvBase(in_channels=1,out_channels=3,kernel_size=(5,self.base_dim))
        self.conv_base5 = BlockConvBase(in_channels=1,out_channels=3,kernel_size=(8,self.base_dim))
        self.conv_base6 = BlockConvBase(in_channels=1,out_channels=3,kernel_size=(13,self.base_dim))
        self.conv_base7 = BlockConvBase(in_channels=1,out_channels=3,kernel_size=(21,self.base_dim))
        self.conv_base8 = BlockConvBase(in_channels=1,out_channels=3,kernel_size=(34,self.base_dim))
        self.conv_base9 = BlockConvBase(in_channels=1,out_channels=3,kernel_size=(55,self.base_dim))
        
        self.max_1 = BlockConvMax(in_channels=1,out_channels=3,kernel_size=(5,self.base_dim))
        self.max_2 = BlockConvMax(in_channels=1,out_channels=3,kernel_size=(8,self.base_dim))
        self.max_3 = BlockConvMax(in_channels=1,out_channels=3,kernel_size=(13,self.base_dim))
        self.max_4 = BlockConvMax(in_channels=1,out_channels=3,kernel_size=(21,self.base_dim))
        self.max_5 = BlockConvMax(in_channels=1,out_channels=3,kernel_size=(34,self.base_dim))
        
        self.ave_1 = BlockConvAve(in_channels=1,out_channels=3,kernel_size=(5,self.base_dim))
        self.ave_2 = BlockConvAve(in_channels=1,out_channels=3,kernel_size=(8,self.base_dim))
        self.ave_3 = BlockConvAve(in_channels=1,out_channels=3,kernel_size=(13,self.base_dim))
        self.ave_4 = BlockConvAve(in_channels=1,out_channels=3,kernel_size=(21,self.base_dim))
        self.ave_5 = BlockConvAve(in_channels=1,out_channels=3,kernel_size=(34,self.base_dim))
        
        self.cross_1 = BlockConvCross(in_channels=1,out_channels=5,kernel_size=(3,3))
        self.cross_2 = BlockConvCross(in_channels=1,out_channels=5,kernel_size=(5,5))
        self.cross_3 = BlockConvCross(in_channels=1,out_channels=5,kernel_size=(7,5))
        self.cross_4 = BlockConvCross(in_channels=1,out_channels=5,kernel_size=(11,5))
        self.cross_5 = BlockConvCross(in_channels=1,out_channels=5,kernel_size=(19,5))
        self.cross_6 = BlockConvCross(in_channels=1,out_channels=5,kernel_size=(21,7))
        
    def forward(self,x:torch.tensor):
        ### x: batch_size, seq_len, base_dim
        x = x.unsqueeze(1)
        base = self.base_block(x)
        max = self.max_block(x)
        ave = self.ave_block(x)
        # cross = self.cross_block(x)
        y = x.squeeze(1)[:,-self.out_seq_len:,:]
        return torch.cat([y,base,max,ave],dim=2)
    
    def base_block(self,x):
        
        base1 = self.conv_base1(x)[:,-self.out_seq_len:,:]
        base2 = self.conv_base2(x)[:,-self.out_seq_len:,:]
        base3 = self.conv_base3(x)[:,-self.out_seq_len:,:]
        base4 = self.conv_base4(x)[:,-self.out_seq_len:,:]
        base5 = self.conv_base5(x)[:,-self.out_seq_len:,:]
        base6 = self.conv_base6(x)[:,-self.out_seq_len:,:]
        base7 = self.conv_base7(x)[:,-self.out_seq_len:,:]
        base8 = self.conv_base8(x)[:,-self.out_seq_len:,:]
        base9 = self.conv_base9(x)[:,-self.out_seq_len:,:]
        # return torch.cat([base1,base2,base3],dim=2)
        return torch.cat([base1,base2,base3,base4,base5,base6,base7,base8,base9],dim=2)
    
    def max_block(self,x):
        
        max1 = self.max_1(x)[:,-self.out_seq_len:,:]
        max2 = self.max_2(x)[:,-self.out_seq_len:,:]
        max3 = self.max_3(x)[:,-self.out_seq_len:,:]
        max4 = self.max_4(x)[:,-self.out_seq_len:,:]
        # max5 = self.max_5(x)[:,-self.out_seq_len:,:]
        
        return torch.cat([max1,max2,max3,max4],dim=2)
    
    def ave_block(self,x):
        
        ave1 = self.ave_1(x)[:,-self.out_seq_len:,:]
        ave2 = self.ave_2(x)[:,-self.out_seq_len:,:]
        ave3 = self.ave_3(x)[:,-self.out_seq_len:,:]
        ave4 = self.ave_4(x)[:,-self.out_seq_len:,:]
        # ave5 = self.ave_5(x)[:,-self.out_seq_len:,:]
        
        return torch.cat([ave1,ave2,ave3,ave4],dim=2)
    
    def cross_block(self,x):
        # cross1 = self.cross_1(x)[:,-self.out_seq_len:,:]
        # cross2 = self.cross_2(x)[:,-self.out_seq_len:,:]
        # cross3 = self.cross_3(x)[:,-self.out_seq_len:,:]
        cross4 = self.cross_4(x)[:,-self.out_seq_len:,:]
        cross5 = self.cross_5(x)[:,-self.out_seq_len:,:]
        cross6 = self.cross_6(x)[:,-self.out_seq_len:,:]
        
        return torch.cat([cross4,cross5,cross6],dim=2)

   
    
class ConvFeatureGet1(nn.Module):
    
    def __init__(self, base_seq_len, base_dim, out_seq_len):
        super(ConvFeatureGet1,self).__init__()
        if base_seq_len < 140:
            raise ValueError("the seq_len should be >= 140 !!!!")
        self.out_seq_len = out_seq_len
        self.base_dim = base_dim
        
        self.conv_base1 = BlockConvBase(in_channels=1,out_channels=5,kernel_size=(1,self.base_dim))
        self.conv_base2 = BlockConvBase(in_channels=1,out_channels=5,kernel_size=(2,self.base_dim))
        self.conv_base3 = BlockConvBase(in_channels=1,out_channels=5,kernel_size=(3,self.base_dim))
        self.conv_base4 = BlockConvBase(in_channels=1,out_channels=5,kernel_size=(5,self.base_dim))
        self.conv_base5 = BlockConvBase(in_channels=1,out_channels=5,kernel_size=(8,self.base_dim))
        self.conv_base6 = BlockConvBase(in_channels=1,out_channels=5,kernel_size=(13,self.base_dim))
        self.conv_base7 = BlockConvBase(in_channels=1,out_channels=5,kernel_size=(21,self.base_dim))
        self.conv_base8 = BlockConvBase(in_channels=1,out_channels=5,kernel_size=(34,self.base_dim))
        self.conv_base9 = BlockConvBase(in_channels=1,out_channels=5,kernel_size=(55,self.base_dim))
        
        self.max_1 = BlockConvMax(in_channels=1,out_channels=3,kernel_size=(5,self.base_dim))
        self.max_2 = BlockConvMax(in_channels=1,out_channels=3,kernel_size=(8,self.base_dim))
        self.max_3 = BlockConvMax(in_channels=1,out_channels=3,kernel_size=(13,self.base_dim))
        self.max_4 = BlockConvMax(in_channels=1,out_channels=3,kernel_size=(21,self.base_dim))
        self.max_5 = BlockConvMax(in_channels=1,out_channels=3,kernel_size=(34,self.base_dim))
        
        self.ave_1 = BlockConvAve(in_channels=1,out_channels=3,kernel_size=(5,self.base_dim))
        self.ave_2 = BlockConvAve(in_channels=1,out_channels=3,kernel_size=(8,self.base_dim))
        self.ave_3 = BlockConvAve(in_channels=1,out_channels=3,kernel_size=(13,self.base_dim))
        self.ave_4 = BlockConvAve(in_channels=1,out_channels=3,kernel_size=(21,self.base_dim))
        self.ave_5 = BlockConvAve(in_channels=1,out_channels=3,kernel_size=(34,self.base_dim))
        
        self.cross_1 = BlockConvCross(in_channels=1,out_channels=5,kernel_size=(3,3))
        self.cross_2 = BlockConvCross(in_channels=1,out_channels=5,kernel_size=(5,5))
        self.cross_3 = BlockConvCross(in_channels=1,out_channels=5,kernel_size=(7,5))
        self.cross_4 = BlockConvCross(in_channels=1,out_channels=5,kernel_size=(11,5))
        self.cross_5 = BlockConvCross(in_channels=1,out_channels=5,kernel_size=(19,5))
        self.cross_6 = BlockConvCross(in_channels=1,out_channels=5,kernel_size=(21,7))
        
    def forward(self,x:torch.tensor):
        ### x: batch_size, seq_len, base_dim
        x = x.unsqueeze(1)
        base = self.base_block(x)
        max = self.max_block(x)
        ave = self.ave_block(x)
        # cross = self.cross_block(x)
        y = x.squeeze(1)[:,-self.out_seq_len:,:]
        return torch.cat([y,base,max,ave],dim=2)
    
    def base_block(self,x):
        
        base1 = self.conv_base1(x)[:,-self.out_seq_len:,:]
        base2 = self.conv_base2(x)[:,-self.out_seq_len:,:]
        base3 = self.conv_base3(x)[:,-self.out_seq_len:,:]
        base4 = self.conv_base4(x)[:,-self.out_seq_len:,:]
        base5 = self.conv_base5(x)[:,-self.out_seq_len:,:]
        base6 = self.conv_base6(x)[:,-self.out_seq_len:,:]
        base7 = self.conv_base7(x)[:,-self.out_seq_len:,:]
        base8 = self.conv_base8(x)[:,-self.out_seq_len:,:]
        base9 = self.conv_base9(x)[:,-self.out_seq_len:,:]
        # return torch.cat([base1,base2,base3],dim=2)
        return torch.cat([base1,base2,base3,base4,base5,base6,base7,base8,base9],dim=2)
    
    def max_block(self,x):
        
        max1 = self.max_1(x)[:,-self.out_seq_len:,:]
        max2 = self.max_2(x)[:,-self.out_seq_len:,:]
        max3 = self.max_3(x)[:,-self.out_seq_len:,:]
        max4 = self.max_4(x)[:,-self.out_seq_len:,:]
        max5 = self.max_5(x)[:,-self.out_seq_len:,:]
        
        return torch.cat([max1,max2,max3,max4,max5],dim=2)
    
    def ave_block(self,x):
        
        ave1 = self.ave_1(x)[:,-self.out_seq_len:,:]
        ave2 = self.ave_2(x)[:,-self.out_seq_len:,:]
        ave3 = self.ave_3(x)[:,-self.out_seq_len:,:]
        ave4 = self.ave_4(x)[:,-self.out_seq_len:,:]
        ave5 = self.ave_5(x)[:,-self.out_seq_len:,:]
        
        return torch.cat([ave1,ave2,ave3,ave4,ave5],dim=2)
    
    def cross_block(self,x):
        # cross1 = self.cross_1(x)[:,-self.out_seq_len:,:]
        # cross2 = self.cross_2(x)[:,-self.out_seq_len:,:]
        # cross3 = self.cross_3(x)[:,-self.out_seq_len:,:]
        cross4 = self.cross_4(x)[:,-self.out_seq_len:,:]
        cross5 = self.cross_5(x)[:,-self.out_seq_len:,:]
        cross6 = self.cross_6(x)[:,-self.out_seq_len:,:]
        
        return torch.cat([cross4,cross5,cross6],dim=2)
        
class ConvFeatureGet2(nn.Module):
    
    def __init__(self, base_seq_len, base_dim, out_seq_len):
        super(ConvFeatureGet2,self).__init__()
        if base_seq_len < 120:
            raise ValueError("the seq_len should be >= 140 !!!!")
        self.out_seq_len = out_seq_len
        self.base_dim = base_dim
        
        self.conv_base3 = BlockConvBase(in_channels=1,out_channels=5,kernel_size=(3,self.base_dim))
        self.conv_base4 = BlockConvBase(in_channels=1,out_channels=5,kernel_size=(5,self.base_dim))
        self.conv_base5 = BlockConvBase(in_channels=1,out_channels=7,kernel_size=(8,self.base_dim))
        self.conv_base6 = BlockConvBase(in_channels=1,out_channels=10,kernel_size=(13,self.base_dim))

        
        self.max_1 = BlockConvMax(in_channels=1,out_channels=5,kernel_size=(5,self.base_dim))
        self.max_2 = BlockConvMax(in_channels=1,out_channels=7,kernel_size=(8,self.base_dim))
        self.max_3 = BlockConvMax(in_channels=1,out_channels=10,kernel_size=(13,self.base_dim))

        
        self.ave_1 = BlockConvAve(in_channels=1,out_channels=5,kernel_size=(5,self.base_dim))
        self.ave_2 = BlockConvAve(in_channels=1,out_channels=7,kernel_size=(8,self.base_dim))
        self.ave_3 = BlockConvAve(in_channels=1,out_channels=10,kernel_size=(13,self.base_dim))

        
        self.cross_1 = BlockConvCross(in_channels=1,out_channels=5,kernel_size=(3,5))
        self.cross_2 = BlockConvCross(in_channels=1,out_channels=7,kernel_size=(5,5))
        self.cross_3 = BlockConvCross(in_channels=1,out_channels=10,kernel_size=(7,5))
        self.cross_4 = BlockConvCross(in_channels=1,out_channels=10,kernel_size=(11,7))
        
    def forward(self,x:torch.tensor):
        ### x: batch_size, seq_len, base_dim
        x = x.unsqueeze(1)
        # base = self.base_block(x)
        max = self.max_block(x)
        ave = self.ave_block(x)
        # cross = self.cross_block(x)
        # y = x.squeeze(1)[:,-self.out_seq_len:,:]
        return torch.cat([max,ave],dim=2)
    
    def base_block(self,x):
        
        base3 = self.conv_base3(x)[:,-self.out_seq_len:,:]
        base4 = self.conv_base4(x)[:,-self.out_seq_len:,:]
        base5 = self.conv_base5(x)[:,-self.out_seq_len:,:]
        base6 = self.conv_base6(x)[:,-self.out_seq_len:,:]

        # return torch.cat([base1,base2,base3],dim=2)
        return torch.cat([base3,base4,base5,base6],dim=2)
    
    def max_block(self,x):
        
        max1 = self.max_1(x)[:,-self.out_seq_len:,:]
        max2 = self.max_2(x)[:,-self.out_seq_len:,:]
        max3 = self.max_3(x)[:,-self.out_seq_len:,:]

        return torch.cat([max1,max2,max3],dim=2)
    
    def ave_block(self,x):
        
        ave1 = self.ave_1(x)[:,-self.out_seq_len:,:]
        ave2 = self.ave_2(x)[:,-self.out_seq_len:,:]
        ave3 = self.ave_3(x)[:,-self.out_seq_len:,:]

        
        return torch.cat([ave1,ave2,ave3],dim=2)
    
    def cross_block(self,x):
        cross1 = self.cross_1(x)[:,-self.out_seq_len:,:]
        cross2 = self.cross_2(x)[:,-self.out_seq_len:,:]
        cross3 = self.cross_3(x)[:,-self.out_seq_len:,:]
        cross4 = self.cross_4(x)[:,-self.out_seq_len:,:]

        # return torch.cat([cross5,cross6],dim=2)
        return torch.cat([cross1,cross2,cross3,cross4],dim=2)        
        
class PositionalEncoding(nn.Module):
    """
    位置编码, 添加时要求维度为seq_len * batch_size * dim
    """
    def __init__(self, d_model, max_len=1000):
        super(PositionalEncoding, self).__init__()
        # 创建一个足够长的P
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:x.size(0), :]
        return x


class CNNTransformer1(nn.Module):
    
    def __init__(self,base_seq_len,base_dim,seq_len,feature_dim,
                 num_heads,num_layers,d_model,output_dim,dim_feedforward,drop_rate,backward):
        super(CNNTransformer1,self).__init__()
        self.feature_dim = feature_dim
        self.d_model = d_model
        self.backward = backward
        
        
        self.pos_encoder = PositionalEncoding(d_model, max_len=1000)
        
        self.feature_get = ConvFeatureGet1(base_seq_len,base_dim,seq_len)
        
        self.pre_layer = nn.Linear(feature_dim,d_model)
        
        self.encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.d_model,
            nhead=num_heads,
            dim_feedforward=dim_feedforward,
            dropout=drop_rate,
            activation='relu',
            batch_first=True,
        )
        
        self.encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers)
        
        
        self.fc1 = nn.Linear(backward*self.d_model, 300)
        self.fc2 = nn.Linear(300,100)
        self.fc3 = nn.Linear(100,output_dim)
        
        self.aft_dropout1 = nn.Dropout(drop_rate)
        self.aft_dropout2 = nn.Dropout(drop_rate)

    def forward(self,x):
        
        x = self.feature_get(x)
        x = self.pre_layer(x)
        x = x.transpose(0,1)
        x = self.pos_encoder(x).transpose(0,1)
        
        x = self.encoder(x)
        
        
        out = x[:,-self.backward:,:].reshape(-1,self.backward*self.d_model)
        # 通过全连接层得到最终输出
        
        out = F.relu(self.fc1(out))
        out = self.aft_dropout1(out)
        out = F.relu(self.fc2(out))
        out = self.aft_dropout2(out)
        out = self.fc3(out)
        
        return out

class BlockCNNTransformer1(nn.Module):
    
    def __init__(self,base_seq_len,base_dim,seq_len,feature_dim,
                 num_heads,num_layers,d_model,dim_feedforward,drop_rate,backward):
        super(BlockCNNTransformer1,self).__init__()
        self.feature_dim = feature_dim
        self.d_model = d_model
        self.backward = backward
        
        
        self.pos_encoder = PositionalEncoding(d_model, max_len=1000)
        
        self.feature_get = ConvFeatureGet0(base_seq_len,base_dim,seq_len)
        
        self.pre_layer = nn.Linear(feature_dim,d_model)
        
        self.encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.d_model,
            nhead=num_heads,
            dim_feedforward=dim_feedforward,
            dropout=drop_rate,
            activation='relu',
            batch_first=True,
        )
        
        self.encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers)
        

    def forward(self,x):
        
        x = self.feature_get(x)
        x = self.pre_layer(x)
        x = x.transpose(0,1)
        x = self.pos_encoder(x).transpose(0,1)
        x = self.encoder(x)
        out = x[:,-self.backward:,:].reshape(-1,self.backward*self.d_model)
        
        return out


class CNNTransformer2(nn.Module):
    
    def __init__(self,base_seq_len,base_dim,seq_len,feature_dim,
                 num_heads,num_layers,d_model,output_dim,dim_feedforward,drop_rate,backward):
        super(CNNTransformer2,self).__init__()
        self.feature_dim = feature_dim
        self.d_model = d_model
        self.backward = backward
        
        
        self.pos_encoder = PositionalEncoding(d_model, max_len=1000)
        
        self.feature_get = ConvFeatureGet2(base_seq_len,base_dim,seq_len)
        
        self.pre_layer = nn.Linear(feature_dim,d_model)
        
        self.encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.d_model,
            nhead=num_heads,
            dim_feedforward=dim_feedforward,
            dropout=drop_rate,
            activation='relu',
            batch_first=True,
        )
        
        self.encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers)
        
        
        self.fc1 = nn.Linear(backward*self.d_model, 300)
        self.fc2 = nn.Linear(300,100)
        self.fc3 = nn.Linear(100,output_dim)
        
        self.aft_dropout1 = nn.Dropout(drop_rate)
        self.aft_dropout2 = nn.Dropout(drop_rate)

    def forward(self,x):
        
        x = self.feature_get(x)
        x = self.pre_layer(x)
        x = x.transpose(0,1)
        x = self.pos_encoder(x).transpose(0,1)
        
        x = self.encoder(x)
        
        
        out = x[:,-self.backward:,:].reshape(-1,self.backward*self.d_model)
        # 通过全连接层得到最终输出
        
        out = F.relu(self.fc1(out))
        out = self.aft_dropout1(out)
        out = F.relu(self.fc2(out))
        out = self.aft_dropout2(out)
        out = self.fc3(out)
        
        return out

# class BaseFactorTransformer(DLmodel):
    
#     def __init__(self, model_params: dict, class_model=CNNTransformer1, dtype='float') -> None:
#         super().__init__(model_params, class_model, dtype)
        
#     def reload_model(self,path):
#         self.model = torch.load(path)
        

#     def train(self,dataset,EPOCHS,batch_size=512,scale=100,shuffle=True,loss='Huber',lr=0.001,stop = 100):
        
#         dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
        
#         if loss[:5] == 'Huber':
#             if len(loss) == 5:
#                 delta = 1
#             else:
#                 delta = float(loss[5:])
#             loss_func = nn.HuberLoss(delta=delta)
#         elif loss == 'MSE':
#             loss_func = nn.MSELoss()
#         elif loss == 'L1':
#             loss_func = nn.L1Loss()
#         else:
#             loss_func = nn.MSELoss()
        
#         optim = torch.optim.Adam(self.model.parameters(),lr=lr)
#         loss_lst = []
#         r2score_lst = []
#         for epoch in range(EPOCHS):
#             self.model.train()
#             epoch_r2score = []
#             epoch_loss = []
#             for batch_idx, (data,target) in enumerate(dataloader):
#                 data = data.float().cuda()
#                 target = target.float().cuda()*scale
#                 optim.zero_grad()
#                 output = self.model(data)
#                 # print(output.shape)
#                 # print(target.shape)
                
#                 l = loss_func(output,target)
#                 if torch.isnan(l):
#                     print(data.isnan().sum())
#                     print(data.max())
#                     print(data.min())
#                     print(output.isnan().sum())
#                     print(output.max())
#                     print(output.min())
#                     print(target.isnan().sum())
#                     print(target.max())
#                     print(target.min())
                    
#                     return 0
    
#                 r2score = self.r2_score(target,output)[0].item()
#                 epoch_r2score.append(r2score)
#                 epoch_loss.append(l.item())
                
#                 l.backward()
                
#                 optim.step()
                
#                 if batch_idx % 100 == 0:
#                     print("train epoch:{}, batch_idx:{}, loss: {:.4f}, R2_score:{:.4f}".format(epoch+1,batch_idx,l.item(),r2score))
            
#             epoch_r2score = np.array(epoch_r2score)
#             epoch_loss = np.array(epoch_loss)
#             if epoch_r2score.mean() > stop:
#                 print("STOP: train epoch:{}, loss:{:.4f}, R2_score:{:.4f}".format(epoch+1,epoch_loss.mean(),epoch_r2score.mean()))
#                 print("")
#                 break
#             print("FINISH: train epoch:{}, loss:{:.4f}, R2_score:{:.4f}".format(epoch+1,epoch_loss.mean(),epoch_r2score.mean()))
#             print("")
     
#         self._r2score_lst = r2score_lst
#         self._loss_lst = loss_lst

#         return 1
    
#     @staticmethod
#     def gen_train_dataset(factor,price,dates,seq_len,forward,dropmid=None,dtype='float'):
#         seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
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
    
#     @staticmethod
#     def test(data:torch.tensor,index,model,batch_size=2048):
#         model = model.cuda()
#         result = []
#         with torch.no_grad():
#             model.eval()
#             for i in range(0,data.shape[0],batch_size):
#                 feature = data[i:i+batch_size].float().cuda()
#                 label = model(feature).reshape(-1).cpu().detach().numpy()
#                 result.append(label)
#         result = np.hstack(result)
#         factor = Series(result,index=index).sort_index()
#         return factor
    


                
                