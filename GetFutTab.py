# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 12:44:26 2018

@author: hh
"""
from WindPy import *
import pandas as pd
import os
import numpy as np
w.start()

#path_in = os.getcwd() + "\\Input\\"
path_out = os.getcwd() + "\\Output\\DLV\\"

def get_dic_from_two_lists(keys, values):
    return {keys[i]:values[i] for i in range(len(keys))}    

FutData = w.wset("futurecc","wind_code=T1803.CFE")
s = get_dic_from_two_lists(FutData.Fields,FutData.Data) 
df = pd.DataFrame(data = s, index = FutData.Codes, columns = FutData.Fields)

num = len(FutData.Codes)

for i in range(num):
    df.ix[i,"issue_dt"] = df.iloc[i,6].strftime('%Y-%m-%d')
    df.ix[i,"last_trade_dt"] = df.iloc[i,7].strftime('%Y-%m-%d')

print(df)

df.to_csv(path_out + "FutureTable.csv", index = True)

w.stop()