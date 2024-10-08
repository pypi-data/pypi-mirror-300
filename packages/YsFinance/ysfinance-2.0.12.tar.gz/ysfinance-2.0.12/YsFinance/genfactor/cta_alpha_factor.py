from .cta_alpha_function import *
import pandas as pd
class AlphaLC(object):
    def __init__(self, df_data):

        self.open = df_data['open']
        self.high = df_data['high']
        self.low = df_data['low']
        self.close = df_data['close']
        self.volume = df_data['volume']
        self.pct_chg = (self.close.ffill()/(self.close.ffill().shift(1)) - 1)
        self.amt = df_data['amount']
        self.swing = (self.high.values - self.low.values)/ (self.close.shift(1))
        self.turn = df_data['turnover']
        self.vwap = (df_data['amount']*1000)/(df_data['volume']*100+1) 
        # 因为成交
        self.volume_ratio = (self.volume/self.volume.shift(1) - 1).replace({np.inf: np.nan, -np.inf: np.nan}) #加0.01是为了防止分母出现0,用1去填充第一个值
        # Alpha#1	 (rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) -0.5)

        # self.open.columns = ['data']
        # self.close.columns = ['data']
        # self.high.columns = ['data']
        # self.low.columns = ['data']
        # self.volume.columns = ['data']
        # self.amt.columns = ['data']
        # self.turn.columns = ['data']
        # self.vwap.columns = ['data']
        # self.volume_ratio.columns = ['data']
        
    def basic_in1(self):
        return self.open
        
    def basic_in2(self):
        return self.close
        
    def basic_in3(self):
        return self.high
        
    def basic_in4(self):
        return self.low
        
    def basic_in5(self):
        return self.volume
        
    def basic_in6(self):
        return self.amt
        
    def basic_in7(self):
        return self.turn
        
    def basic_in8(self):
        return self.swing
        
    def basic_in9(self):
        return self.pct_chg
        
    def basic_in10(self):
        return self.vwap
        
    def basic_in12(self):
        return self.volume_ratio
        
    def basic_in13(self):
        return self.close.shift(1)
        
    def basic_in14(self):
        return self.volume.shift(1)
        
    def basic_in15(self):
        return self.swing.shift(1)
        
    def basic_in16(self):
        return self.pct_chg.shift(1)
        
    def mean_in1(self):
        return Ts_Single_Mean(self.volume,3)
        
    def mean_in2(self):
        return Ts_Single_Mean(self.volume,5)
        
    def mean_in3(self):
        return Ts_Single_Mean(self.volume,10)
        
    def mean_in4(self):
        return Ts_Single_Mean(self.volume,30)
        
    def mean_in5(self):
        return Ts_Single_Mean(self.volume,60)
        
    def mean_in6(self):
        return Ts_Single_Mean(self.pct_chg,3)
        
    def mean_in7(self):
        return Ts_Single_Mean(self.pct_chg,5)
        
    def mean_in8(self):
        return Ts_Single_Mean(self.pct_chg,10)
        
    def mean_in9(self):
        return Ts_Single_Mean(self.pct_chg,30)
        
    def mean_in10(self):
        return Ts_Single_Mean(self.pct_chg,60)
        
    def mean_in11(self):
        return Ts_Single_Mean(self.amt*Self_Sign(self.pct_chg),3)
        
    def mean_in12(self):
        return Ts_Single_Mean(self.amt*Self_Sign(self.pct_chg),5)
        
    def mean_in13(self):
        return Ts_Single_Mean(self.amt*Self_Sign(self.pct_chg),10)
        
    def mean_in14(self):
        return Ts_Single_Mean(self.amt*Self_Sign(self.pct_chg),30)
        
    def mean_in15(self):
        return Ts_Single_Mean(self.amt*Self_Sign(self.pct_chg),60)
        
    def mean_in16(self):
        return Ts_Single_Mean(self.turn,3)
        
    def mean_in17(self):
        return Ts_Single_Mean(self.turn,5)
        
    def mean_in18(self):
        return Ts_Single_Mean(self.turn,10)
        
    def mean_in19(self):
        return Ts_Single_Mean(self.turn,30)
        
    def mean_in20(self):
        return Ts_Single_Mean(self.turn,60)
        
    def mean_in21(self):
        return Ts_Single_Mean(self.volume_ratio,3)
        
    def mean_in22(self):
        return Ts_Single_Mean(self.volume_ratio,5)
        
    def mean_in23(self):
        return Ts_Single_Mean(self.volume_ratio,10)
        
    def mean_in24(self):
        return Ts_Single_Mean(self.volume_ratio,30)
        
    def mean_in25(self):
        return Ts_Single_Mean(self.volume_ratio,60)
        
    def delta_in1(self):
        return Ts_Single_Delta(self.turn,1)
        
    def delta_in2(self):
        return Ts_Single_Delta(self.volume,1)
        
    def delta_in3(self):
        return Ts_Single_Delta(self.pct_chg,1)
        
    def delta_in5(self):
        return Ts_Single_Delta(self.amt*Self_Sign(self.pct_chg),1)
        
    def delta_in6(self):
        return Ts_Single_Delta(self.open,1)
        
    def delta_in7(self):
        return Ts_Single_Delta(self.close,1)
        
    def delta_in8(self):
        return Ts_Single_Delta(self.high,1)
        
    def delta_in9(self):
        return Ts_Single_Delta(self.low,1)
        
    def delta_in10(self):
        return Ts_Single_Delta(self.vwap,1)
        
    def delta_in11(self):
        return Ts_Single_Rate(self.vwap,1)
        
    def delta_in13(self):
        return Ts_Single_Rate(self.turn,1)
        
    def delta_in14(self):
        return Ts_Single_Rate(self.volume,1)
        
    def delta_in15(self):
        return Ts_Single_Rate(self.pct_chg,1)
        
    def delta_in18(self):
        return Ts_Single_Rate(self.amt*Self_Sign(self.pct_chg),1)
        
    def delta_in19(self):
        return Ts_Single_Rate(self.open,1)
        
    def delta_in20(self):
        return Ts_Single_Rate(self.close,1)
        
    def delta_in21(self):
        return Ts_Single_Rate(self.high,1)
        
    def delta_in22(self):
        return Ts_Single_Rate(self.low,1)
        
    def delta_in23(self):
        return Ts_Single_Delta(self.volume_ratio,1)
        
    def delta_in24(self):
        return Ts_Single_Rate(self.volume_ratio,1)
        
    def mometum_in1(self):
        return Cs_Single_UpZeroLimit(Ts_Single_Sum(self.pct_chg,3))
        
    def mometum_in2(self):
        return Cs_Single_UpZeroLimit(Ts_Single_Sum(self.pct_chg,5))
        
    def mometum_in3(self):
        return Cs_Single_UpZeroLimit(Ts_Single_Sum(self.pct_chg,10))
        
    def mometum_in4(self):
        return Cs_Single_UpZeroLimit(Ts_Single_Sum(self.pct_chg,30))
        
    def mometum_in5(self):
        return Cs_Single_UpZeroLimit(Ts_Single_Sum(self.pct_chg,60))
        
    def mometum_in6(self):
        return Ts_Shape_Compare(self.open,self.close,3)/3
        
    def mometum_in7(self):
        return Ts_Shape_Compare(self.open,self.close,5)/5
        
    def mometum_in8(self):
        return Ts_Shape_Compare(self.open,self.close,10)/10
        
    def mometum_in9(self):
        return Ts_Shape_Compare(self.open,self.close,30)/30
        
    def mometum_in10(self):
        return Ts_Shape_Compare(self.open,self.close,60)/60
        
    def mometum_in11(self):
        return Ts_Increase_Times_Discontinuous(self.close,3)/3
        
    def mometum_in12(self):
        return Ts_Increase_Times_Discontinuous(self.close,5)/5
        
    def mometum_in13(self):
        return Ts_Increase_Times_Discontinuous(self.close,10)/10
        
    def mometum_in14(self):
        return Ts_Increase_Times_Discontinuous(self.close,30)/30
        
    def mometum_in15(self):
        return Ts_Increase_Times_Discontinuous(self.close,60)/60
        
    def mometum_in16(self):
        return Ts_Increase_Times_Continuous(self.close,3)/3
        
    def mometum_in17(self):
        return Ts_Increase_Times_Continuous(self.close,5)/5
        
    def mometum_in18(self):
        return Ts_Increase_Times_Continuous(self.close,10)/10
        
    def mometum_in19(self):
        return Ts_Increase_Times_Continuous(self.close,30)/30
        
    def mometum_in20(self):
        return Ts_Increase_Times_Continuous(self.close,60)/60
        
    def mometum_in21(self):
        return Ts_Single_RSI(self.pct_chg,3)
        
    def mometum_in22(self):
        return Ts_Single_RSI(self.pct_chg,5)
        
    def mometum_in23(self):
        return Ts_Single_RSI(self.pct_chg,10)
        
    def mometum_in24(self):
        return Ts_Single_RSI(self.pct_chg,30)
        
    def mometum_in25(self):
        return Ts_Single_RSI(self.pct_chg,60)
        
    def mometum_in26(self):
        return Cs_Double_Multiply(Ts_Single_Rate(self.close,3),Self_Power(Ts_Single_Linear_Decay(Ts_Single_Divide(self.volume,1),3),1.5))
        
    def mometum_in27(self):
        return Cs_Double_Multiply(Ts_Single_Rate(self.close,5),Self_Power(Ts_Single_Linear_Decay(Ts_Single_Divide(self.volume,1),5),1.5))
        
    def mometum_in28(self):
        return Cs_Double_Multiply(Ts_Single_Rate(self.close,7),Self_Power(Ts_Single_Linear_Decay(Ts_Single_Divide(self.volume,1),7),1.5))
        
    def mometum_in29(self):
        return Cs_Double_Multiply(Ts_Single_Rate(self.close,14),Self_Power(Ts_Single_Linear_Decay(Ts_Single_Divide(self.volume,1),14),1.5))
        
    def mometum_in30(self):
        return Cs_Double_Multiply(Ts_Single_Rate(self.close,28),Self_Power(Ts_Single_Linear_Decay(Ts_Single_Divide(self.volume,1),28),1.5))
        
    def reversion_in1(self):
        return Self_Negative(Cs_Single_DownZeroLimit(Ts_Single_Sum(self.pct_chg,3)))
        
    def reversion_in2(self):
        return Self_Negative(Cs_Single_DownZeroLimit(Ts_Single_Sum(self.pct_chg,5)))
        
    def reversion_in3(self):
        return Self_Negative(Cs_Single_DownZeroLimit(Ts_Single_Sum(self.pct_chg,10)))
        
    def reversion_in4(self):
        return Self_Negative(Cs_Single_DownZeroLimit(Ts_Single_Sum(self.pct_chg,30)))
        
    def reversion_in5(self):
        return Self_Negative(Cs_Single_DownZeroLimit(Ts_Single_Sum(self.pct_chg,60)))
        
    def reversion_in6(self):
        return 1-Ts_Shape_Compare(self.open,self.close,3)/3
        
    def reversion_in7(self):
        return 1-Ts_Shape_Compare(self.open,self.close,5)/5
        
    def reversion_in8(self):
        return 1-Ts_Shape_Compare(self.open,self.close,10)/10
        
    def reversion_in9(self):
        return 1-Ts_Shape_Compare(self.open,self.close,22)/22
        
    def reversion_in10(self):
        return 1-Ts_Shape_Compare(self.open,self.close,60)/60
        
    def reversion_in11(self):
        return Ts_Decrease_Times_Discontinuous(self.close,3)/3
        
    def reversion_in12(self):
        return Ts_Decrease_Times_Discontinuous(self.close,5)/5
        
    def reversion_in13(self):
        return Ts_Decrease_Times_Discontinuous(self.close,10)/10
        
    def reversion_in14(self):
        return Ts_Decrease_Times_Discontinuous(self.close,30)/30
        
    def reversion_in15(self):
        return Ts_Decrease_Times_Discontinuous(self.close,60)/60
        
    def reversion_in16(self):
        return Ts_Decrease_Times_Continuous(self.close,3)/3
        
    def reversion_in17(self):
        return Ts_Decrease_Times_Continuous(self.close,5)/5
        
    def reversion_in18(self):
        return Ts_Decrease_Times_Continuous(self.close,10)/10
        
    def reversion_in19(self):
        return Ts_Decrease_Times_Continuous(self.close,30)/30
        
    def reversion_in20(self):
        return Ts_Decrease_Times_Continuous(self.close,60)/60
        
    def reversion_in21(self):
        return Ts_Single_RSI(-self.pct_chg,3)
        
    def reversion_in22(self):
        return Ts_Single_RSI(-self.pct_chg,5)
        
    def reversion_in23(self):
        return Ts_Single_RSI(-self.pct_chg,10)
        
    def reversion_in24(self):
        return Ts_Single_RSI(-self.pct_chg,22)
        
    def reversion_in25(self):
        return Ts_Single_RSI(-self.pct_chg,60)
        
    def reversion_in26(self):
        return Cs_Double_Divide(Ts_Single_Rate(self.close,3),Self_Power(Ts_Single_Linear_Decay(Ts_Single_Divide(self.volume,1),3),1.5))
        
    def reversion_in27(self):
        return Cs_Double_Divide(Ts_Single_Rate(self.close,5),Self_Power(Ts_Single_Linear_Decay(Ts_Single_Divide(self.volume,1),5),1.5))
        
    def reversion_in28(self):
        return Cs_Double_Divide(Ts_Single_Rate(self.close,7),Self_Power(Ts_Single_Linear_Decay(Ts_Single_Divide(self.volume,1),7),1.5))
        
    def reversion_in29(self):
        return Cs_Double_Divide(Ts_Single_Rate(self.close,14),Self_Power(Ts_Single_Linear_Decay(Ts_Single_Divide(self.volume,1),14),1.5))
        
    def reversion_in30(self):
        return Cs_Double_Divide(Ts_Single_Rate(self.close,28),Self_Power(Ts_Single_Linear_Decay(Ts_Single_Divide(self.volume,1),28),1.5))
        
    def volume_in1(self):
        return Ts_Single_AccRate(self.volume,3)
        
    def volume_in2(self):
        return Ts_Single_AccRate(self.volume,5)
        
    def volume_in3(self):
        return Ts_Single_AccRate(self.volume,10)
        
    def volume_in4(self):
        return Ts_Single_AccRate(self.volume,20)
        
    def volume_in5(self):
        return Ts_Single_AccRate(self.volume,30)
        
    def volume_in6(self):
        return Ts_Single_Sum(Self_Sign(self.pct_chg)*self.volume,3)
        
    def volume_in7(self):
        return Ts_Single_Sum(Self_Sign(self.pct_chg)*self.volume,5)
        
    def volume_in8(self):
        return Ts_Single_Sum(Self_Sign(self.pct_chg)*self.volume,10)
        
    def volume_in9(self):
        return Cs_Double_Divide(Ts_Single_Sum(Self_Sign(self.pct_chg)*self.amt,3),self.amt)
        
    def volume_in10(self):
        return Cs_Double_Divide(Ts_Single_Sum(Self_Sign(self.pct_chg)*self.amt,5),self.amt)
        
    def volume_in11(self):
        return Cs_Double_Divide(Ts_Single_Sum(Self_Sign(self.pct_chg)*self.amt,10),self.amt)
        
    def volatility_in1(self):
        return Ts_Single_Stddev(self.pct_chg,3)
        
    def volatility_in2(self):
        return Ts_Single_Stddev(self.pct_chg,5)
        
    def volatility_in3(self):
        return Ts_Single_Stddev(self.pct_chg,10)
        
    def volatility_in4(self):
        return Ts_Single_Stddev(self.pct_chg,30)
        
    def volatility_in5(self):
        return Ts_Single_Stddev(self.pct_chg,60)
        
    def volatility_in6(self):
        return Ts_Single_Stddev(self.swing,3)
        
    def volatility_in7(self):
        return Ts_Single_Stddev(self.swing,5)
        
    def volatility_in8(self):
        return Ts_Single_Stddev(self.swing,10)
        
    def volatility_in9(self):
        return Ts_Single_Stddev(self.swing,30)
        
    def volatility_in10(self):
        return Ts_Single_Stddev(self.swing,60)
        
    def volatility_in11(self):
        return Ts_Single_Stddev(self.turn,3)
        
    def volatility_in12(self):
        return Ts_Single_Stddev(self.turn,5)
        
    def volatility_in13(self):
        return Ts_Single_Stddev(self.turn,10)
        
    def volatility_in14(self):
        return Ts_Single_Stddev(self.turn,30)
        
    def volatility_in15(self):
        return Ts_Single_Stddev(self.turn,60)
        
    def volatility_in16(self):
        return Ts_Single_Max_Divide_Min(self.close,5)-1
        
    def volatility_in17(self):
        return Ts_Single_Max_Divide_Min(self.close,10)-1
        
    def volatility_in18(self):
        return Ts_Single_Max_Divide_Min(self.close,30)-1
        
    def volatility_in19(self):
        return Ts_Single_Max_Divide_Min(self.close,60)-1
        
    def volatility_in20(self):
        return Ts_Single_Max_Divide_Min(self.volume,5)-1
        
    def volatility_in21(self):
        return Ts_Single_Max_Divide_Min(self.volume,10)-1
        
    def volatility_in22(self):
        return Ts_Single_Max_Divide_Min(self.volume,30)-1
        
    def volatility_in23(self):
        return Ts_Single_Max_Divide_Min(self.volume,60)-1
        
    def skewness_in1(self):
        return Ts_Single_Skewness(self.volume,5)
        
    def skewness_in2(self):
        return Ts_Single_Skewness(self.volume,10)
        
    def skewness_in3(self):
        return Ts_Single_Skewness(self.volume,30)
        
    def skewness_in4(self):
        return Ts_Single_Skewness(self.volume,60)
        
    def skewness_in5(self):
        return Ts_Single_Skewness(self.turn,5)
        
    def skewness_in6(self):
        return Ts_Single_Skewness(self.turn,10)
        
    def skewness_in7(self):
        return Ts_Single_Skewness(self.turn,20)
        
    def skewness_in8(self):
        return Ts_Single_Skewness(self.turn,60)
        
    def skewness_in9(self):
        return Ts_Single_Skewness(self.pct_chg,5)
        
    def skewness_in10(self):
        return Ts_Single_Skewness(self.pct_chg,10)
        
    def skewness_in11(self):
        return Ts_Single_Skewness(self.pct_chg,30)
        
    def skewness_in12(self):
        return Ts_Single_Skewness(self.pct_chg,60)
        
    def skewness_in13(self):
        return Ts_Single_Skewness(self.open,5)
        
    def skewness_in14(self):
        return Ts_Single_Skewness(self.open,10)
        
    def skewness_in15(self):
        return Ts_Single_Skewness(self.open,30)
        
    def skewness_in16(self):
        return Ts_Single_Skewness(self.open,60)
        
    def skewness_in21(self):
        return Ts_Double_Skewness(self.turn,self.swing,5)
        
    def skewness_in22(self):
        return Ts_Double_Skewness(self.turn,self.swing,10)
        
    def skewness_in23(self):
        return Ts_Double_Skewness(self.pct_chg,self.turn,5)
        
    def skewness_in24(self):
        return Ts_Double_Skewness(self.pct_chg,self.turn,10)
        
    def skewness_in25(self):
        return Ts_Double_Skewness(self.pct_chg,self.swing,5)
        
    def skewness_in26(self):
        return Ts_Double_Skewness(self.pct_chg,self.swing,10)
        
    def skewness_in27(self):
        return Ts_Double_Skewness(self.open,self.close,5)
        
    def skewness_in28(self):
        return Ts_Double_Skewness(self.open,self.close,10)
        
    def skewness_in29(self):
        return Ts_Double_Skewness(self.high,self.low,5)
        
    def skewness_in30(self):
        return Ts_Double_Skewness(self.high,self.low,10)
        
    def kurtosis_in1(self):
        return Ts_Single_Kurtosis(self.volume,5)
        
    def kurtosis_in2(self):
        return Ts_Single_Kurtosis(self.volume,10)
        
    def kurtosis_in3(self):
        return Ts_Single_Kurtosis(self.volume,30)
        
    def kurtosis_in4(self):
        return Ts_Single_Kurtosis(self.volume,60)
        
    def kurtosis_in5(self):
        return Ts_Single_Kurtosis(self.turn,5)
        
    def kurtosis_in6(self):
        return Ts_Single_Kurtosis(self.turn,10)
        
    def kurtosis_in7(self):
        return Ts_Single_Kurtosis(self.turn,30)
        
    def kurtosis_in8(self):
        return Ts_Single_Kurtosis(self.turn,60)
        
    def kurtosis_in9(self):
        return Ts_Single_Kurtosis(self.pct_chg,5)
        
    def kurtosis_in10(self):
        return Ts_Single_Kurtosis(self.pct_chg,10)
        
    def kurtosis_in11(self):
        return Ts_Single_Kurtosis(self.pct_chg,30)
        
    def kurtosis_in12(self):
        return Ts_Single_Kurtosis(self.pct_chg,60)
        
    def kurtosis_in13(self):
        return Ts_Single_Kurtosis(self.open,5)
        
    def kurtosis_in14(self):
        return Ts_Single_Kurtosis(self.open,10)
        
    def kurtosis_in15(self):
        return Ts_Single_Kurtosis(self.open,30)
        
    def kurtosis_in16(self):
        return Ts_Single_Kurtosis(self.open,60)
        
    def kurtosis_in21(self):
        return Ts_Double_Kurtosis(self.turn,self.swing,5)
        
    def kurtosis_in22(self):
        return Ts_Double_Kurtosis(self.turn,self.swing,10)
        
    def kurtosis_in23(self):
        return Ts_Double_Kurtosis(self.pct_chg,self.turn,5)
        
    def kurtosis_in24(self):
        return Ts_Double_Kurtosis(self.pct_chg,self.turn,10)
        
    def kurtosis_in25(self):
        return Ts_Double_Kurtosis(self.pct_chg,self.swing,5)
        
    def kurtosis_in26(self):
        return Ts_Double_Kurtosis(self.pct_chg,self.swing,10)
        
    def kurtosis_in27(self):
        return Ts_Double_Kurtosis(self.open,self.close,5)
        
    def kurtosis_in28(self):
        return Ts_Double_Kurtosis(self.open,self.close,10)
        
    def kurtosis_in29(self):
        return Ts_Double_Kurtosis(self.high,self.low,5)
        
    def kurtosis_in30(self):
        return Ts_Double_Kurtosis(self.high,self.low,10)
        
    def correlation_in1(self):
        return Cs_Single_Correlation(self.pct_chg,3)
        
    def correlation_in2(self):
        return Cs_Single_Correlation(self.pct_chg,5)
        
    def correlation_in3(self):
        return Cs_Single_Correlation(self.pct_chg,10)
        
    def correlation_in4(self):
        return Cs_Single_Correlation(self.pct_chg,30)
        
    def correlation_in5(self):
        return Cs_Single_Correlation(self.turn,3)
        
    def correlation_in6(self):
        return Cs_Single_Correlation(self.turn,5)
        
    def correlation_in7(self):
        return Cs_Single_Correlation(self.turn,10)
        
    def correlation_in8(self):
        return Cs_Single_Correlation(self.turn,30)
        
    def correlation_in9(self):
        return Cs_Single_Correlation(self.volume,3)
        
    def correlation_in10(self):
        return Cs_Single_Correlation(self.volume,5)
        
    def correlation_in11(self):
        return Cs_Single_Correlation(self.volume,10)
        
    def correlation_in12(self):
        return Cs_Single_Correlation(self.volume,30)
        
    def correlation_in13(self):
        return Ts_Double_Correlation(self.pct_chg,self.turn,3)
        
    def correlation_in14(self):
        return Ts_Double_Correlation(self.pct_chg,self.turn,5)
        
    def correlation_in15(self):
        return Ts_Double_Correlation(self.pct_chg,self.turn,10)
        
    def correlation_in16(self):
        return Ts_Double_Correlation(self.pct_chg,self.turn,30)
        
    def correlation_in17(self):
        return Ts_Double_Correlation(self.pct_chg,self.turn,60)
        
    def correlation_in23(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.close,5,1),Self_Sign(Ts_Single_Delta(self.close,5)))
        
    def correlation_in24(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.close,10,1),Self_Sign(Ts_Single_Delta(self.close,10)))
        
    def correlation_in25(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.close,20,1),Self_Sign(Ts_Single_Delta(self.close,20)))
        
    def correlation_in26(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.close,60,1),Self_Sign(Ts_Single_Delta(self.close,60)))
        
    def correlation_in27(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.close,6,3),Self_Sign(Ts_Single_Delta(self.close,3)))
        
    def correlation_in28(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.close,10,5),Self_Sign(Ts_Single_Delta(self.close,5)))
        
    def correlation_in29(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.close,20,10),Self_Sign(Ts_Single_Delta(self.close,10)))
        
    def correlation_in30(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.close,60,30),Self_Sign(Ts_Single_Delta(self.close,30)))
        
    def correlation_in31(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.volume,5,1),Self_Sign(Ts_Single_Delta(self.volume,5)))
        
    def correlation_in32(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.volume,10,1),Self_Sign(Ts_Single_Delta(self.volume,10)))
        
    def correlation_in33(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.volume,20,1),Self_Sign(Ts_Single_Delta(self.volume,20)))
        
    def correlation_in34(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.volume,60,1),Self_Sign(Ts_Single_Delta(self.volume,60)))
        
    def correlation_in35(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.volume,6,3),Self_Sign(Ts_Single_Delta(self.volume,3)))
        
    def correlation_in36(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.volume,10,5),Self_Sign(Ts_Single_Delta(self.volume,5)))
        
    def correlation_in37(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.volume,20,10),Self_Sign(Ts_Single_Delta(self.volume,10)))
        
    def correlation_in38(self):
        return Cs_Double_Multiply(Ts_Single_AutoCorrelation(self.volume,60,30),Self_Sign(Ts_Single_Delta(self.volume,30)))
        
    def bias_in6(self):
        return Cs_Double_Divide(Ts_Single_Linear_Decay(self.close,3),self.close)-1
        
    def bias_in7(self):
        return Cs_Double_Divide(Ts_Single_Linear_Decay(self.close,5),self.close)-1
        
    def bias_in8(self):
        return Cs_Double_Divide(Ts_Single_Linear_Decay(self.close,10),self.close)-1
        
    def bias_in9(self):
        return Cs_Double_Divide(Ts_Single_Linear_Decay(self.close,30),self.close)-1
        
    def bias_in10(self):
        return Cs_Double_Divide(Ts_Single_Linear_Decay(self.close,60),self.close)-1
        
    def bias_in11(self):
        return Cs_Double_Divide(Ts_Single_Pressure(self.close,7),self.close)-1
        
    def bias_in12(self):
        return Cs_Double_Divide(Ts_Single_Pressure(self.close,14),self.close)-1
        
    def bias_in13(self):
        return Cs_Double_Divide(Ts_Single_Pressure(self.close,30),self.close)-1
        
    def bias_in14(self):
        return Cs_Double_Divide(Ts_Single_Pressure(self.close,60),self.close)-1
        
    def bias_in15(self):
        return Cs_Double_Divide(self.close,Ts_Single_Support(self.close,7))-1
        
    def bias_in16(self):
        return Cs_Double_Divide(self.close,Ts_Single_Support(self.close,14))-1
        
    def bias_in17(self):
        return Cs_Double_Divide(self.close,Ts_Single_Support(self.close,30))-1
        
    def bias_in18(self):
        return Cs_Double_Divide(self.close,Ts_Single_Support(self.close,60))-1
        
    def bias_in19(self):
        return Cs_Double_Divide(self.close,Ts_Single_Max(self.high,5))-0.5
        
    def bias_in20(self):
        return Cs_Double_Divide(self.close,Ts_Single_Max(self.high,10))-0.5
        
    def bias_in21(self):
        return Cs_Double_Divide(self.close,Ts_Single_Max(self.high,20))-0.5
        
    def bias_in22(self):
        return Cs_Double_Divide(self.close,Ts_Single_Max(self.high,60))-0.5
        
    def bias_in23(self):
        return Cs_Double_Divide(self.close,Ts_Single_Min(self.low,5))-0.5
        
    def bias_in24(self):
        return Cs_Double_Divide(self.close,Ts_Single_Min(self.low,10))-0.5
        
    def bias_in25(self):
        return Cs_Double_Divide(self.close,Ts_Single_Min(self.low,20))-0.5
        
    def bias_in26(self):
        return Cs_Double_Divide(self.close,Ts_Single_Min(self.low,60))-0.5
        
    def bias_in27(self):
        return Cs_Double_Divide(self.close,0.01+Cs_Double_Divide(Ts_Single_Sum(self.amt,3),Ts_Single_Sum(self.volume,3)))-1
        
    def bias_in28(self):
        return Cs_Double_Divide(self.close,0.01+Cs_Double_Divide(Ts_Single_Sum(self.amt,5),Ts_Single_Sum(self.volume,5)))-1
        
    def bias_in29(self):
        return Cs_Double_Divide(self.close,0.01+Cs_Double_Divide(Ts_Single_Sum(self.amt,10),Ts_Single_Sum(self.volume,10)))-1
        
    def bias_in30(self):
        return Cs_Double_Divide(self.close,0.01+Cs_Double_Divide(Ts_Single_Sum(self.amt,20),Ts_Single_Sum(self.volume,20)))-1
        
    def bias_in31(self):
        return Cs_Double_Divide(self.close,0.01+Cs_Double_Divide(Ts_Single_Sum(self.amt,60),Ts_Single_Sum(self.volume,60)))-1
        
    def bias_in32(self):
        return Cs_Double_Divide(self.close,self.vwap)-1
        
    def bias_in33(self):
        return Cs_Double_Divide(self.high,self.vwap)-1
        
    def bias_in34(self):
        return Cs_Double_Divide(self.low,self.vwap)-1
        
    def bias_in35(self):
        return Cs_Double_Divide(self.open,self.vwap)-1
        
    def bias_in36(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.close,5),Ts_Single_Mean(self.close,10))-1
        
    def bias_in37(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.close,10),Ts_Single_Mean(self.close,20))-1
        
    def bias_in38(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.close,20),Ts_Single_Mean(self.close,30))-1
        
    def bias_in39(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.close,30),Ts_Single_Mean(self.close,60))-1
        
    def bias_in40(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.close,5),Ts_Single_Mean(self.close,10))-1
        
    def bias_in41(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.close,10),Ts_Single_Mean(self.close,20))-1
        
    def bias_in42(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.close,20),Ts_Single_Mean(self.close,30))-1
        
    def bias_in43(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.close,30),Ts_Single_Mean(self.close,60))-1
        
    def bias_in44(self):
        return Cs_Double_Divide(Ts_Single_Cummax(self.close,5),self.close)
        
    def bias_in45(self):
        return Cs_Double_Divide(Ts_Single_Cummax(self.close,10),self.close)
        
    def bias_in46(self):
        return Cs_Double_Divide(Ts_Single_Cummax(self.close,20),self.close)
        
    def bias_in47(self):
        return Cs_Double_Divide(Ts_Single_Cummax(self.close,30),self.close)
        
    def bias_in48(self):
        return Cs_Double_Divide(Ts_Single_Cummax(self.close,60),self.close)
        
    def bias_in49(self):
        return Cs_Double_Divide(Ts_Single_Cummin(self.close,5),self.close)
        
    def bias_in50(self):
        return Cs_Double_Divide(Ts_Single_Cummin(self.close,10),self.close)
        
    def bias_in51(self):
        return Cs_Double_Divide(Ts_Single_Cummin(self.close,20),self.close)
        
    def bias_in52(self):
        return Cs_Double_Divide(Ts_Single_Cummin(self.close,30),self.close)
        
    def bias_in53(self):
        return Cs_Double_Divide(Ts_Single_Cummin(self.close,60),self.close)
        
    def bias_in54(self):
        return Cs_Double_Divide(self.close,Ts_Single_Delay(Ts_Single_UpBoll(self.close,10,2),3))
        
    def bias_in55(self):
        return Cs_Double_Divide(self.close,Ts_Single_Delay(Ts_Single_UpBoll(self.close,30,2),3))
        
    def bias_in56(self):
        return Cs_Double_Divide(self.close,Ts_Single_Delay(Ts_Single_UpBoll(self.close,60,2),3))
        
    def bias_in57(self):
        return Cs_Double_Divide(Ts_Single_Delay(Ts_Single_DownBoll(self.close,10,2),3),self.close)
        
    def bias_in58(self):
        return Cs_Double_Divide(Ts_Single_Delay(Ts_Single_DownBoll(self.close,30,2),3),self.close)
        
    def bias_in59(self):
        return Cs_Double_Divide(Ts_Single_Delay(Ts_Single_DownBoll(self.close,60,2),3),self.close)
        
    def stability_in1(self):
        return Ts_Single_Sharp(self.pct_chg,10)
        
    def stability_in2(self):
        return Ts_Single_Sharp(self.pct_chg,20)
        
    def stability_in3(self):
        return Ts_Single_Sharp(self.pct_chg,30)
        
    def stability_in4(self):
        return Ts_Single_Sharp(self.pct_chg,60)
        
    def stability_in5(self):
        return Ts_Single_Sharp(self.turn,10)
        
    def stability_in6(self):
        return Ts_Single_Sharp(self.turn,20)
        
    def stability_in7(self):
        return Ts_Single_Sharp(self.turn,30)
        
    def stability_in8(self):
        return Ts_Single_Sharp(self.turn,60)
        
    def stability_in9(self):
        return Ts_Single_Sharpee(self.pct_chg,10)
        
    def stability_in10(self):
        return Ts_Single_Sharpee(self.pct_chg,20)
        
    def stability_in11(self):
        return Ts_Single_Sharpee(self.pct_chg,30)
        
    def stability_in12(self):
        return Ts_Single_Sharpee(self.pct_chg,60)
        
    def technique_in1(self):
        return Cs_Double_Divide(self.close-self.open+1,self.high-self.low+1)
        
    def technique_in2(self):
        return Cs_Double_Divide(self.close-self.low+1,self.high-self.open+1)
        
    def technique_in3(self):
        return Cs_Double_Divide(self.high-self.close+1,self.open-self.low+1)
        
    def technique_in4(self):
        return Ts_Single_AroonUp(self.close,7)/7
        
    def technique_in5(self):
        return Ts_Single_AroonUp(self.close,30)/30
        
    def technique_in6(self):
        return Ts_Single_AroonUp(self.close,60)/60
        
    def technique_in7(self):
        return Ts_Single_AroonDown(self.close,7)/7
        
    def technique_in8(self):
        return Ts_Single_AroonDown(self.close,30)/30
        
    def technique_in9(self):
        return Ts_Single_AroonDown(self.close,60)/60
        
    def technique_in10(self):
        return Cs_Double_Minus(Ts_Single_AroonUp(self.close,7),Ts_Single_AroonDown(self.close,7))/7
        
    def technique_in11(self):
        return Cs_Double_Minus(Ts_Single_AroonUp(self.close,30),Ts_Single_AroonDown(self.close,30))/30
        
    def technique_in12(self):
        return Cs_Double_Minus(Ts_Single_AroonUp(self.close,60),Ts_Single_AroonDown(self.close,60))/60
        
    def technique_in14(self):
        return Cs_Double_Divide(self.close-self.open,self.close.shift(1))
        
    def technique_in15(self):
        return Cs_Double_Divide(self.high-self.close,self.close.shift(1))
        
    def technique_in16(self):
        return Cs_Double_Divide(self.close-self.low,self.close.shift(1))
        
    def technique_in17(self):
        return Cs_Double_Divide(self.open-self.low,self.close.shift(1))
        
    def technique_in18(self):
        return Cs_Double_Divide(self.open-self.high,self.close.shift(1))
        
    def technique_in23(self):
        return Cs_Double_Divide(Ts_Single_Delay(Ts_Single_Rate(self.close,3),3),Ts_Single_Stddev(self.pct_chg,3))
        
    def technique_in24(self):
        return Cs_Double_Divide(Ts_Single_Delay(Ts_Single_Rate(self.close,5),5),Ts_Single_Stddev(self.pct_chg,5))
        
    def technique_in25(self):
        return Cs_Double_Divide(Ts_Single_Delay(Ts_Single_Rate(self.close,10),10),Ts_Single_Stddev(self.pct_chg,10))
        
    def technique_in26(self):
        return Cs_Double_Divide(Ts_Single_Delay(Ts_Single_Rate(self.close,20),20),Ts_Single_Stddev(self.pct_chg,20))
        
    def technique_in27(self):
        return Cs_Double_Divide(Ts_Single_Delay(Ts_Single_Rate(self.close,60),60),Ts_Single_Stddev(self.pct_chg,60))
        
    def technique_in28(self):
        return Cs_Double_Divide(Ts_Single_Rate(self.close,3),Ts_Single_Delay(Ts_Single_Stddev(self.pct_chg,3),3))
        
    def technique_in29(self):
        return Cs_Double_Divide(Ts_Single_Rate(self.close,5),Ts_Single_Delay(Ts_Single_Stddev(self.pct_chg,5),5))
        
    def technique_in30(self):
        return Cs_Double_Divide(Ts_Single_Rate(self.close,10),Ts_Single_Delay(Ts_Single_Stddev(self.pct_chg,10),10))
        
    def technique_in31(self):
        return Cs_Double_Divide(Ts_Single_Rate(self.close,20),Ts_Single_Delay(Ts_Single_Stddev(self.pct_chg,20),20))
        
    def technique_in32(self):
        return Cs_Double_Divide(Ts_Single_Rate(self.close,60),Ts_Single_Delay(Ts_Single_Stddev(self.pct_chg,60),60))
        
    def elasticity1(self):
        return Cs_Double_Divide(self.pct_chg,self.turn)
        
    def elasticity2(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.pct_chg,3),Ts_Single_Mean(self.turn,3))
        
    def elasticity3(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.pct_chg,5),Ts_Single_Mean(self.turn,5))
        
    def elasticity4(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.pct_chg,10),Ts_Single_Mean(self.turn,10))
        
    def elasticity5(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.pct_chg,30),Ts_Single_Mean(self.turn,30))
        
    def elasticity6(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.pct_chg,60),Ts_Single_Mean(self.turn,60))
        
    def elasticity7(self):
        return Cs_Double_Divide(self.swing,self.turn)
        
    def elasticity8(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.swing,3),Ts_Single_Mean(self.turn,3))
        
    def elasticity9(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.swing,5),Ts_Single_Mean(self.turn,5))
        
    def elasticity10(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.swing,10),Ts_Single_Mean(self.turn,10))
        
    def elasticity11(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.swing,30),Ts_Single_Mean(self.turn,30))
        
    def elasticity12(self):
        return Cs_Double_Divide(Ts_Single_Mean(self.swing,60),Ts_Single_Mean(self.turn,60))
        
    def elasticity13(self):
        return Cs_Double_Divide(Cs_Double_Highest(self.swing,Self_Abs(self.pct_chg)),self.turn)
        
    def elasticity14(self):
        return Cs_Double_Divide(Cs_Double_Highest(Ts_Single_Mean(self.swing,3),Ts_Single_Mean(Self_Abs(self.pct_chg),3)),self.turn)
        
    def elasticity15(self):
        return Cs_Double_Divide(Cs_Double_Highest(Ts_Single_Mean(self.swing,3),Ts_Single_Mean(Self_Abs(self.pct_chg),5)),self.turn)
        
    def elasticity16(self):
        return Cs_Double_Divide(Cs_Double_Highest(Ts_Single_Mean(self.swing,3),Ts_Single_Mean(Self_Abs(self.pct_chg),10)),self.turn)
        
    def elasticity17(self):
        return Cs_Double_Divide(Cs_Double_Highest(Ts_Single_Mean(self.swing,3),Ts_Single_Mean(Self_Abs(self.pct_chg),30)),self.turn)
        
    def elasticity18(self):
        return Cs_Double_Divide(Cs_Double_Highest(Ts_Single_Mean(self.swing,3),Ts_Single_Mean(Self_Abs(self.pct_chg),60)),self.turn)
    
    def ga_factor_1(self):
        return Ts_Single_Stddev(self.volume,8)
        
    def ga_factor_2(self):
        return Cs_Single_Correlation(self.open,18)
        
    def ga_factor_3(self):
        return Cs_Single_Correlation(self.high,16)
        
    def ga_factor_4(self):
        return Ts_Single_Max_Divide_Min(self.volume,9)
        
    def ga_factor_5(self):
        return Ts_Single_Max_Divide_Min(self.volume,9)
        
    def ga_factor_6(self):
        return Cs_Single_Correlation(self.amt,16)
        
    def ga_factor_7(self):
        return Ts_Double_Kurtosis(self.pct_chg,self.high,7)
        
    def ga_factor_8(self):
        return Cs_Single_Correlation(self.pct_chg,8)
        
    def ga_factor_9(self):
        return Ts_Single_Amplitude(Cs_Single_Correlation(self.pct_chg,8),11)
        
    def ga_factor_10(self):
        return Cs_Single_Correlation(self.close,13)
        
    def ga_factor_11(self):
        return Ts_Single_Amplitude(Cs_Single_Correlation(self.pct_chg,16),24)
        
    def ga_factor_12(self):
        return Ts_Single_Amplitude(self.amt,19)
        
    def ga_factor_13(self):
        return Ts_Single_Sharpee(Ts_Manhattan_Distance(self.volume, self.pct_chg,10),19)
        
    def ga_factor_14(self):
        return Cs_Single_Correlation(self.amt,24)
        
    def ga_factor_15(self):
        return Cs_Single_Correlation(self.amt,8)
        
    def ga_factor_16(self):
        return Ts_Single_Max_Minus_Min(Cs_Single_Correlation(self.pct_chg,8),9)
        
    def ga_factor_17(self):
        return Ts_Single_Max_Minus_Min(Cs_Single_Correlation(self.pct_chg,16),8)
        
    def ga_factor_18(self):
        return Cs_Single_Correlation(Cs_Double_Lowest(self.swing,Ts_Single_Sharp(self.pct_chg,28)),8)
        
    def ga_factor_19(self):
        return Cs_Single_Correlation(self.swing,9)
        
    def ga_factor_20(self):
        return Ts_Single_Max_Minus_Min(Cs_Single_Correlation(self.pct_chg,16),30)
        
    def ga_factor_21(self):
        return Ts_Single_Max_Minus_Min(Ts_Single_Max(Ts_Single_Stddev(self.amt,8),8),9)
        
    def ga_factor_22(self):
        return Ts_Single_Max(Cs_Single_Correlation(self.pct_chg,16),9)
        
    def ga_factor_23(self):
        return Cs_Single_Correlation(self.swing,30)
        
    def ga_factor_24(self):
        return Ts_Single_Max_Minus_Min(Cs_Single_Correlation(self.close,13),13)
        
    def ga_factor_25(self):
        return Cs_Single_Correlation(Self_SignPower_Inv(self.volume,15),9)
        
    def ga_factor_26(self):
        return Ts_Single_Max(Ts_Double_Skewness(self.amt,self.high,8),8)
        
    def ga_factor_27(self):
        return Cs_Double_Lowest(Ts_Single_Max_Minus_Min(Ts_Single_Max_Minus_Min(Self_SignPower_Inv(self.volume,15),16),19),Cs_Double_Lowest(Cs_Double_Lowest(self.swing,Ts_Single_Sharp(self.pct_chg,28)),Cs_DeepScale(self.amt,16)),19)
    
    # def factor_generate(self,function_name):
    #     factor_data = []
    #     factor_name = []
    #     for name in function_name:
    #         if hasattr(self, name) and callable(getattr(self, name)):
    #             try:
    #                 fac = getattr(self, name)().copy()
    #                 fac.columns = [name]
    #                 factor_data.append(fac)
    #             except:
    #                 print(f"函数 {name} 计算时出错")
    #                 continue
    #         else:
    #             print(f"函数 {name} 未找到")
    #     factor_data = pd.concat(factor_data,axis=1)
    #     return factor_data
    



def getCrossFactor(dateList,needStockList):
        high = np.zeros((len(dateList)*241,len(needStockList)))
        low = np.zeros((len(dateList)*241,len(needStockList)))
        open = np.zeros((len(dateList)*241,len(needStockList)))
        close = np.zeros((len(dateList)*241,len(needStockList)))
        amount = np.zeros((len(dateList)*241,len(needStockList)))
        volume = np.zeros((len(dateList)*241,len(needStockList)))
        turn = np.zeros((len(dateList)*241,len(needStockList)))
        adjfactor = np.zeros((len(dateList)*241,len(needStockList)))
        minute = np.zeros(len(dateList)*241)
        for i in range(len(needStockList)):
            code = 'stock_'+str(int(needStockList[i][:6]))+'.h5'
            data = pd.read_hdf('./stockBar/'+code)
            for j in range(len(dateList)):
                pos = np.where(data['tdate']==dateList[j])[0]
                if len(pos)==241:
                    high[(j*241):(j*241+241),i] = data['high'].iloc[pos]
                    low[(j*241):(j*241+241),i] = data['low'].iloc[pos]
                    open[(j*241):(j*241+241),i] = data['open'].iloc[pos]
                    close[(j*241):(j*241+241),i] = data['close'].iloc[pos]
                    amount[(j*241):(j*241+241),i] = data['amount'].iloc[pos]
                    volume[(j*241):(j*241+241),i] = data['volume'].iloc[pos]
                    turn[(j*241):(j*241+241),i] = data['to'].iloc[pos]
                    adjfactor[(j*241):(j*241+241),i] = data['adjfactor'].iloc[pos]
                    minute[(j*241):(j*241+241)] = data['tdate'].astype(float).iloc[pos]*10000+data['bar'].iloc[pos]
                else:
                    print(needStockList[i]+'在'+str(dateList[j])+'日数据不全')
        high = pd.DataFrame(high,index=minute, columns=needStockList)
        low = pd.DataFrame(low,index=minute, columns=needStockList)
        open = pd.DataFrame(open,index=minute, columns=needStockList)
        close = pd.DataFrame(close,index=minute, columns=needStockList)
        amount = pd.DataFrame(amount,index=minute, columns=needStockList)
        volume = pd.DataFrame(volume,index=minute, columns=needStockList)
        turn = pd.DataFrame(turn,index=minute, columns=needStockList)
        adjfactor = pd.DataFrame(adjfactor,index=minute, columns=needStockList)
        vwap = pd.DataFrame(amount.values/volume.values,index=close.index, columns=close.columns).fillna(0)
        crossStockData = {'high':high,'low':low,'open1':open,'close1':close,'vol':volume,'amt':amount,'turn':turn,'VWAP':vwap,'adjfactor':adjfactor}
        return crossStockData
    
if __name__ == '__main__':
    # dateList = [20170101,20170102]
    # needStockList = ['000333.SZ','600519.SH']
    # # 根据股票代码一个个取股票数据
    # baseFactor = getCrossFactor(dateList,needStockList)
    # # 计算因子值dd
    # needFactorList = pd.read_excel('FactorFunction_351.xlsx')['Label']
    # stock = AlphaLC(baseFactor)
    # dict0 = dict()
    # for i in range(len(needFactorList)):
    #     factorName = needFactorList[i]
    #     try:
    #         dict0[factorName] = eval('stock.' + factorName + '()')
    #     except:
    #         dict0[factorName] = None
    # # 把因子值转换成三维数组
    # subFactorValue = dict0[needFactorList[0]]
    # minuteList = subFactorValue.index.values
    # factorValue3D = np.zeros((len(minuteList), len(needStockList), len(needFactorList)))
    # for i in range(len(needFactorList)):
    #     factorValue3D[:, :, i] = dict0[needFactorList[i]].values
    feature_names = ['open', 'close', 'low', 'high', 'volume', 'pct_chg', 'amt', 'turn', 'vwap']
    data_df = dict()
    for name in feature_names:
        data_df[name] = pd.DataFrame(np.random.normal(0, 1, size=(252, 50)))
    alphalc = AlphaLC(data_df)
    print(alphalc.basic_in15())
    print("Hello world")



        