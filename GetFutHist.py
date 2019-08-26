# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 12:44:26 2018

@author: hh
"""
from WindPy import *
import pandas as pd
import os
import numpy as np
import datetime as dt
w.start()

fut_path = os.getcwd() + "\\Output\\DLV\\" +"FutureTable.csv"
path_out = os.getcwd() + "\\Output\\DLV\\Bond Future Hist\\"

def get_dic_from_two_lists(keys, values):
    return {keys[i]:values[i] for i in range(len(keys))}

df = pd.read_csv(fut_path, usecols=["wind_code","issue_dt","last_trade_dt"])
i = 0
num = len(df["wind_code"])

for i in range(num):
    fut = df.iloc[i,0]
    issue_dt = df.iloc[i,1]
    last_trad = df.iloc[i,2]
    price = w.wsd(fut, "open,high,low,close,volume,settle", issue_dt, last_trad, "TradingCalendar=CFFEX;Fill=Previous")
    dic = get_dic_from_two_lists(price.Fields,price.Data)
    df1 = pd.DataFrame(data = dic, index = price.Times)
    df1.index.name = "DATE"
    df1["AVG"] = (df1["HIGH"] + df1["LOW"]) / 2 
    df1 = df1[["OPEN","HIGH","LOW","CLOSE","VOLUME","SETTLE","AVG"]]
    df1.to_csv(path_out + fut + ".csv", index = True)
 
w.stop()