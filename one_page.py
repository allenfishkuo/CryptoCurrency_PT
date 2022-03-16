# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 17:24:11 2022

@author: Allen
"""

import pandas as pd
from glob import glob
 
files = glob('BTC_ETH_Table_1min/*.csv')
print(files)
df = pd.DataFrame()
for file in files :
    date = file.split('\\')[1].split('_')[0]
    data = pd.read_csv(file)
    data['date'] = date
    print(data)
    df = pd.concat([df,data],ignore_index = True)
print(df)
#df = pd.concat(
    #(pd.read_csv(file) for file in files ), ignore_index=True)
 
print(df)
df.to_csv('BTC_ETH_total_table_1min.csv',index = False)