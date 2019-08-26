# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 12:20:56 2018

@author: hh
"""

from WindPy import *
import pandas as pd
import os
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
w.start()
def get_dic_from_two_lists(keys, values):
    return {keys[i]:values[i] for i in range(len(keys))}

#start = dt.date(2000,1,1)
end = dt.date.today()
start = end - dt.timedelta(days = 3000)

#rlist = ["DR001.IB","DR007.IB","IBO001.IB","IBO007.IB","DR014.IB","204001.SH","204007.SH","204014.SH","131810.SZ","131801.SZ","131802.SZ"]
rlist = ["CGB1Y.WI","CGB10Y.WI"]
ecos = ["M1000166","M1000158","M1004271","M1004263","M0000612","M0000616","M0000613","M0046692","M0001227","M0049160","M0000705"]
# china bond total return index
bond_idx = ["000012.sh"]

rate = w.wsd(rlist, "close",start, end, "PriceAdj=MP")
vol = w.wsd(rlist,"volume",start, end, "PriceAdj=MP")
eco = w.edb(ecos, start, end,"Fill=Previous")
idx = w.wsd(bond_idx, "close",start, end, "PriceAdj=MP")


df1 = get_dic_from_two_lists(rate.Codes,rate.Data) 
df_rate = pd.DataFrame(data = df1, index = rate.Times, columns = rate.Codes)
df2 = get_dic_from_two_lists(vol.Codes,vol.Data) 
df_vol = pd.DataFrame(data = df2, index = vol.Times, columns = vol.Codes)
df3 = get_dic_from_two_lists(eco.Codes,eco.Data) 
df_eco = pd.DataFrame(data = df3, index = eco.Times, columns = eco.Codes)


termsprd101 = df_eco.iloc[:,0] - df_eco.iloc[:,1]
termsprd101.plot(title = "term spread")
cdbterm_101 = df_eco.iloc[:,2] - df_eco.iloc[:,3]
cdbterm_101.plot(title = "cdb term spread")
# CDB to Government Spread
sprd_fg = df_eco.iloc[:,2] - df_eco.iloc[:,0]
sprd_fg.plot(title = "10y CDB to Government Spread")
plt.show()

        
w.stop()