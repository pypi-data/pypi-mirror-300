from ..util import DLmodel
import torch
import torch.nn as nn
import torch.nn.functional as F
from math import log






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
    

class BlockTransformer(nn.Module):
    """
    Transformer模块的编码器，一层全连接网络+编码器，实现(batch_size,seq_len,input_dim)->(batch_size,seq_len,d_model)的输出
    """
    def __init__(self, input_dim, d_model, num_heads, num_layers, dim_feedforward,drop_rate):
        super(BlockTransformer, self).__init__()
        
        self.d_model = d_model
        self.aft_dropout = nn.Dropout(drop_rate)
        self.pre_layer = nn.Linear(input_dim,d_model)
        self.pre_dropout = nn.Dropout(drop_rate)
        
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
        
    def forward(self, x):
        # x: (batch_size, seq_len, input_dim)
        
        ### 添加位置编码
        x = self.pre_layer(x)
        x = self.pre_dropout(x)
        x = self.pos_encoder(x.transpose(0,1)).transpose(0,1)
        
        x = self.encoder(x)
        
        # x:(batch_size, seq_len, d_model)
        return x

class BlockLSTM(nn.Module):
    """
    LSTM编码器模块，一层lstm编码器，实现(batch_siez,seq_len,input_dim)->(batch_size,seq_len,hidden_dim)的输出
    """
    def __init__(self, input_dim, hidden_dim, num_layers=1,lstm_drop=0):
        super(BlockLSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        # LSTM层
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True,dropout=lstm_drop)
        
    def forward(self, x):
        # 初始化隐藏状态和细胞状态
        h0 = torch.zeros((self.num_layers, x.size(0), self.hidden_dim)).to(x.device) 
        c0 = torch.zeros((self.num_layers, x.size(0), self.hidden_dim)).to(x.device)
        # 前向传播LSTM
        out, _ = self.lstm(x, (h0, c0))  # out: tensor of shape (batch_size, seq_length, hidden_dim)
        return out

class BlockGRU(nn.Module):
    
    def __init__(self, input_dim, hidden_dim, num_layers=1,lstm_drop=0):
        super(BlockGRU, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        # LSTM层
        self.gru = nn.GRU(input_dim, hidden_dim, num_layers, batch_first=True,dropout=lstm_drop)
        
    def forward(self, x):
        # 初始化隐藏状态
        h0 = torch.zeros((self.num_layers, x.size(0), self.hidden_dim)).to(x.device) 
        # 前向传播LSTM
        out, _ = self.gru(x, h0)  # out: tensor of shape (batch_size, seq_length, hidden_dim)
        return out
    

class AttentionLSTM(nn.Module):
    def __init__(self,input_dim,d_model,num_heads,trans_layers,dim_feedforward,hidden_dim,lstm_layers,out_dim,backward,drop_rate):
        super(AttentionLSTM, self).__init__()
        self.backward = backward
        self.hidden_dim = hidden_dim
        self.trans_encoder = BlockTransformer(input_dim,d_model,num_heads,trans_layers,dim_feedforward,drop_rate)
        self.lstm_encoder = BlockLSTM(d_model,hidden_dim,lstm_layers)
        self.aft_layer1 = nn.Linear(backward*hidden_dim,300)
        self.drop_out1 = nn.Dropout(drop_rate)
        self.aft_layer2 = nn.Linear(300,100)
        self.drop_out2 = nn.Dropout(drop_rate)
        self.aft_layer3 = nn.Linear(100,out_dim)
        
    
    def forward(self,x):
        x = self.trans_encoder(x)
        x = self.lstm_encoder(x)
        x = x[:,-self.backward:,:].reshape(-1,self.backward*self.hidden_dim)
        x = F.relu(self.aft_layer1(x))
        x = self.drop_out1(x)
        x = F.relu(self.aft_layer2(x))
        x = self.drop_out2(x)
        x = self.aft_layer3(x)
        return x
        
    