# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 15:20:01 2018

@author: hh
"""

from WindPy import *
import pandas as pd
import os
w.start()

#path_in = os.getcwd() + "\\Input\\"
path_out = os.getcwd() + "\\Output\\DLV\\10Y by Contract\\"

futures = ["T1509","T1512","T1603","T1606","T1609","T1612","T1703","T1706","T1709","T1712","T1803","T1806","T1809"]

for future in futures:
    dlv=w.wset("conversionfactor","windcode=" + future + ".CFE")
    df = pd.DataFrame({"Ticker":dlv.Data[0],"Conversion Ratio":dlv.Data[1]})
    df["Key"] = future
    df = df[["Ticker", "Conversion Ratio","Key"]]
    df.to_csv(path_out + future + ".csv", index = False)

w.stop()