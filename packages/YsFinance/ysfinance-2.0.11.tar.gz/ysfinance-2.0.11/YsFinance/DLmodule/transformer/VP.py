import pandas as pd
from pandas import DataFrame,Series
import numpy as np

import torch 
from torch.utils.data import TensorDataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F
from math import log

from ...stockcalendar import CALENDAR_TOOL
import matplotlib.pyplot as plt


from ..util import DLmodel


trade_dates = Series(CALENDAR_TOOL.trade_date_in_range('2001-01-01','2026-01-01'),index = CALENDAR_TOOL.trade_date_in_range('2001-01-01','2026-01-01'))


class PositionalEncoding(nn.Module):
    """
    位置编码
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
    

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        # self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        # self.bn2 = nn.BatchNorm2d(out_channels)
        self.downsample = downsample

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.relu(out)
        out = self.conv2(out)

        if self.downsample:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out
    

    
class Transformer5(nn.Module):
    """
    实现input_dim * seq_len -> output_dim 的基本的Transformer模型的架构, 不要前馈网络，直接跟编码器，让编码器直接提取数据特征
    """
    def __init__(self, input_dim, d_model, num_heads, num_layers, output_dim, dim_feedforward,drop_rate, backward):
        super(Transformer5, self).__init__()
        
        self.d_model = d_model
        self.backward = backward
        self.aft_dropout = nn.Dropout(drop_rate)
        
        self.pre_layer = nn.Linear(input_dim,d_model)
        
        # 编码器层
        self.pos_encoder = PositionalEncoding(self.d_model, max_len=500)
        self.encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.d_model,
            nhead=num_heads,
            dim_feedforward=dim_feedforward,
            dropout=drop_rate,
            activation='relu',
            batch_first=True,
            # attn_weights_need=attn_weights_need
        )
        
        # 编码器
        self.encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers)
        
        # 输出层
        self.fc1 = nn.Linear(backward*self.d_model, 500)
        self.fc2 = nn.Linear(500,100)
        self.fc3 = nn.Linear(100,output_dim)
        
        # self.init_weights()
        
    def forward(self, x):
        # x: (batch_size, seq_length, input_dim)
        
        ### 添加位置编码
        x = self.pre_layer(x)
        x = self.pos_encoder(x.transpose(0,1)).transpose(0,1)
        
        x = self.encoder(x)
        
        
        # 拼接最后若干时间步的数据再跟全连接网络
        out = x[:,-self.backward:,:].reshape(-1,self.backward*self.d_model)
        # 通过全连接层得到最终输出
        out = F.relu(self.fc1(out))
        out = self.aft_dropout(out)
        out = F.relu(self.fc2(out))
        out = self.fc3(out)
        
        return out
    


    
    

        
    
