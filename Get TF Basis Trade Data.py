# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 10:56:23 2018

@author: hh
"""

from WindPy import *
import pandas as pd
import os
import numpy as np
import datetime as dt

w.start()

#path_in = os.getcwd() + "\\Input\\"
path_out = os.getcwd() + "\\Output\\DLV\\"
path_bas = os.getcwd() + "\\Output\\DLV\\5Y by Contract\\"
path_fut_hist = os.getcwd() + "\\Output\\DLV\\5Y Bond Future Hist\\"
path_bond_hist = os.getcwd() + "\\Output\\DLV\\Bond Hist\\5Y\\"

def get_dic_from_two_lists(keys, values):
    return {keys[i]:values[i] for i in range(len(keys))}    

def right(str, num):
    return str[-num:]   

def left(str, num):
    return str[0:num]   

FutData = w.wset("futurecc","startdate=2013-06-20;enddate=2018-02-26;wind_code=TF.CFE")
s = get_dic_from_two_lists(FutData.Fields,FutData.Data) 
df = pd.DataFrame(data = s, index = FutData.Codes, columns = FutData.Fields)
df.to_csv(path_out + "FutureTable_TF.csv", index = True)

num = len(df["code"])

for i in range(num):
    df.ix[i,"issue_dt"] = df.iloc[i,6].strftime('%Y-%m-%d')
    df.ix[i,"last_trade_dt"] = df.iloc[i,7].strftime('%Y-%m-%d')

# Get historical prices for each TF contract
i = 0
for i in range(num):
    fut = df.iloc[i,2]
    issue_dt = df.iloc[i,9]
    last_trad = df.iloc[i,10]
    price = w.wsd(fut, "open,high,low,close,volume,settle", issue_dt, last_trad, "TradingCalendar=CFFEX;Fill=Previous")
    dic = get_dic_from_two_lists(price.Fields,price.Data)
    df1 = pd.DataFrame(data = dic, index = price.Times)
    df1.index.name = "DATE"
    df1["AVG"] = (df1["HIGH"] + df1["LOW"]) / 2 
    df1 = df1[["OPEN","HIGH","LOW","CLOSE","VOLUME","SETTLE","AVG"]]
    df1.to_csv(path_fut_hist + fut + ".csv", index = True)
#    print(df1)
    
    dlv=w.wset("conversionfactor","windcode=" + fut)
    df_bas = pd.DataFrame({"Ticker":dlv.Data[0],"Conversion Ratio":dlv.Data[1]})
    df_bas["Key"] = fut
    df_bas = df_bas[["Ticker", "Conversion Ratio","Key"]]
    df_bas.to_csv(path_bas + left(fut,6) + "_DLV.csv", index = False)

    # Get DLV for each TF contract  
    dlvs = df_bas["Ticker"].values.tolist()
    for dlv in dlvs:
        exch = right(dlv,2)
        if exch == "SH":
            price = w.wsd(dlv, "open,high,low,close", issue_dt, last_trad, "Fill=Previous;PriceAdj=CP")
        elif exch == "IB":
            price = w.wsd(dlv, "open,high,low,close", issue_dt, last_trad, "TradingCalendar=NIB; Fill=Previous;PriceAdj=CP")
        elif exch == "sz":
            price = w.wsd(dlv, "open,high,low,close", issue_dt, last_trad, "TradingCalendar=SZSE; Fill=Previous;PriceAdj=CP")
        s = get_dic_from_two_lists(price.Fields,price.Data)
        hist = pd.DataFrame(data = s, index = price.Times)
        hist.index.name = "DATE"
        hist["AVG"] = (hist["HIGH"] + hist["LOW"]) / 2 
        hist.to_csv(path_bond_hist + left(fut,6) + "_" + dlv + ".csv", index = True)
        
w.stop()