# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 09:28:11 2021

@author: Allen
"""

import pandas as pd
import os 

path = './Crypto_Currency_Cointegration/2021/'
path_new = './Crypto_Currency_Cointegration/tmp/'

for text in os.listdir(path) :
    df = pd.read_csv(path+text)
    df.dropna(axis = 0, how = 'any',inplace = True)
    
    df.to_csv(path_new + text)

