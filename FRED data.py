#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 14:16:56 2018

@author: hh
"""

from pandas_datareader import DataReader
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

start = datetime.date(1990,1,1)
end = datetime.date.today()
tickers = ["DGS10",
           "FEDFUNDS",
           "DCOILWTICO",
           "GOLDAMGBD228NLBM",
           "UNRATE",
           "CIVPART",
           "BAMLHYH0A0HYM2TRIV",
           "SP500"]
data_source = "fred"

#for ticker in tickers:    
#    fed = DataReader(ticker,data_source,start,end)
#    print(fed.tail(10))
#    fed.plot(title = ticker,figsize = (15,5))
#    plt.show()

sp = DataReader(tickers[7],data_source,start,end)
print(sp.tail(10))
sp.plot(title = tickers[7],figsize = (15,5))
plt.show()

num = 233
risk_num = 60


sp1 = sp.copy()
sample = sp1.dropna()
ret_cum = sample / sample.iloc[0,:]
ret_per = sample / sample.shift(1) - 1
print(ret_cum.tail())
print(ret_per.tail())
ret_cum.plot(title = "cumulative return")

mn  = ret_per.rolling(window = num).mean()
#(rolling_mean(ret_per,window = num)
stdev  = ret_per.rolling(window = num).std()
mn.plot(title = "rolling mean")
stdev.plot(title = "rolling std")
sharp_roll = 252 ** 0.5 * (mn / stdev)
sharp_roll.plot(title = "rolling sharp")
plt.show() 

#bb_data = con.bdh(tickers, 'PX_LAST', '19801231', '20171113')
#data = bb_data.copy()
#
#num = 233
#risk_num = 60
#sample = data.dropna()
#ret = log(sample).diff()
#mn  = ret.rolling(num).mean() * 252.0
#stdev  = ret.rolling(num).std() * sqrt(252.0)
#ir = tanh(mn.values / stdev.values)
#lag = 1
#idx = 0
#pos = pd.DataFrame(index = sample.index, columns=sample.columns)
#signal = ir[0,:] - mean(ir[0,:])
#scale = 1.0
#for i in range(0, sample.shape[0]) :
#      #if sample.index[i].month != sample.index[i+1].month:
#      if sample.index[i].dayofweek == 2:
#            signal = ir[(idx -lag),:] - mean(ir[(idx -lag),:])
#            cv = ret.iloc[(idx-lag-risk_num):(idx-lag), :].cov()
#            scale = 100000000 * 0.01 / sqrt(cv.dot(signal).dot(signal)*252)
#      for j in range(0, sample.columns.shape[0]):
#            pos.iloc[idx, j]  = round(signal[j] * scale, -4)
#      idx = idx + 1
#
#pnls = pd.DataFrame(pos.head(sample.shape[0] -1).values * ret.tail(sample.shape[0] -1).values)
#pnls.index = sample.index[1:]
#port = pnls.dropna().sum(1).cumsum()
#ann_ret = pnls.dropna().sum(1).mean()*252
#ann_vol = pnls.dropna().sum(1).std()*sqrt(252)
#ir = ann_ret / ann_vol
#port.plot()
#print(ir)
