# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 16:07:27 2018

@author: hh
"""
from WindPy import *
import pandas as pd
import datetime as dt
import os
import matplotlib.pyplot as plt
w.start()

def plot_data(df, title="Prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()
def get_dic_from_two_lists(keys, values):
    return { keys[i] : values[i] for i in range(len(keys)) }    
#path_in = os.getcwd() + "\\Input\\"
path_out = os.getcwd() + "\\Output\\"

begin_date = "2007-01-01"
end_date = dt.date.today() - dt.timedelta(days = 1)
dt.datetime
rate = w.wsd("CGB1Y.WI,CGB3Y.WI,CGB5Y.WI,CGB7Y.WI,CGB10Y.WI,DR001.IB,DR007.IB,DR014.IB,DR021.IB,DR1M.IB,DR3M.IB,SHIBORON.IR,SHIBOR1W.IR,SHIBOR2W.IR,SHIBOR1M.IR,SHIBOR3M.IR,204001.SH,204007.SH,204014.SH,204028.SH,204091.SH,204182.SH", "close", begin_date, end_date, "Fill=Previous")
s = get_dic_from_two_lists(rate.Codes,rate.Data)    
df = pd.DataFrame(data = s, index = rate.Times, columns = rate.Codes)
print(df.head())

plot_data(df)
df.to_csv(path_out + "Rate Data.csv", index = True)

w.stop()