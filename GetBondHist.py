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

dlv_path = os.getcwd() + "\\Output\\DLV\\Bond_basket_T.csv"
path_out = os.getcwd() + "\\Output\\DLV\\Bond Hist\\"

def get_dic_from_two_lists(keys, values):
    return {keys[i]:values[i] for i in range(len(keys))}
def right(str, num):
    return str[-num:]    

df = pd.read_csv(dlv_path, usecols=["Ticker"])
dlvs = df["Ticker"].values.tolist()
end = dt.date.today().strftime('%Y-%m-%d')
begin = dt.date(2015,1,1).strftime('%Y-%m-%d')
#print(right(dlvs[0],2))

for dlv in dlvs:
    exch = right(dlv,2)
    if exch == "SH":
        price = w.wsd(dlv, "open,high,low,close", begin, end, "Fill=Previous;PriceAdj=CP")
    elif exch == "IB":
        price = w.wsd(dlv, "open,high,low,close", begin, end, "TradingCalendar=NIB; Fill=Previous;PriceAdj=CP")
    elif exch == "sz":
        price = w.wsd(dlv, "open,high,low,close", begin, end, "TradingCalendar=SZSE; Fill=Previous;PriceAdj=CP")
    s = get_dic_from_two_lists(price.Fields,price.Data)
    hist = pd.DataFrame(data = s, index = price.Times)
    hist.index.name = "DATE"
    hist["AVG"] = (hist["HIGH"] + hist["LOW"]) / 2 
    hist.to_csv(path_out + dlv + ".csv", index = True)

w.stop()