# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 10:56:23 2018

@author: hh
"""

from WindPy import *
import pandas as pd
import os
import numpy as np
w.start()

#path_in = os.getcwd() + "\\Input\\"
path_out = os.getcwd() + "\\Output\\DLV\\"
path_bas = os.getcwd() + "\\Output\\DLV\\5Y by Contract\\"
path_fut_hist = os.getcwd() + "\\Output\\DLV\\5Y Bond Future Hist\\"

def get_dic_from_two_lists(keys, values):
    return {keys[i]:values[i] for i in range(len(keys))}    

def right(str, num):
    return str[-num:]   

FutData = w.wset("futurecc","startdate=2015-02-26;enddate=2018-02-26;wind_code=TF.CFE")
s = get_dic_from_two_lists(FutData.Fields,FutData.Data) 
df = pd.DataFrame(data = s, index = FutData.Codes, columns = FutData.Fields)
df.to_csv(path_out + "FutureTable_TF.csv", index = True)

num = len(df["code"])

for i in range(num):
    df.ix[i,"issue_dt"] = df.iloc[i,6].strftime('%Y-%m-%d')
    df.ix[i,"last_trade_dt"] = df.iloc[i,7].strftime('%Y-%m-%d')


# Get DLV for each TF contract
futures = df["code"].values.tolist()
for future in futures:
    dlv=w.wset("conversionfactor","windcode=" + future + ".CFE")
    df_bas = pd.DataFrame({"Ticker":dlv.Data[0],"Conversion Ratio":dlv.Data[1]})
    df_bas["Key"] = future
    df_bas = df_bas[["Ticker", "Conversion Ratio","Key"]]
    df_bas.to_csv(path_bas + future + "_DLV.csv", index = False)

# Get historical prices for each TF contract
i = 0
for i in range(num):
    fut = df.iloc[i,2]
    issue_dt = df.iloc[i,9]
    last_trad = df.iloc[i,10]
    price = w.wsd(fut , "open,high,low,close,volume,settle", issue_dt, last_trad, "TradingCalendar=CFFEX;Fill=Previous")
    dic = get_dic_from_two_lists(price.Fields,price.Data)
    df1 = pd.DataFrame(data = dic, index = price.Times)
    df1.index.name = "DATE"
    df1["AVG"] = (df1["HIGH"] + df1["LOW"]) / 2 
    df1 = df1[["OPEN","HIGH","LOW","CLOSE","VOLUME","SETTLE","AVG"]]
    df1.to_csv(path_fut_hist + fut + ".csv", index = True)

print(df1)

w.stop()