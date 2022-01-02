# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 16:23:13 2020

@author: allen
"""
#import torch
#import torch.nn as nn
import numpy as np
#import new_dataloader

from trade_trend import trade_down_slope, trade_up_slope, trade_normal
#import matrix_trading
import os 
import pandas as pd
import torch
import torch.utils.data as Data

import matplotlib.pyplot as plt
import time
import sys
import time
from multiprocessing import Pool
path_to_2015compare = "./newstdcompare2015/" 
path_to_2016compare = "./newstdcompare2016/" 
path_to_2017compare = "./newstdcompare2017/" 
path_to_2018compare = "./newstdcompare2018/" 
path_to_2019compare = "./newstdcompare2019/" 
path_to_2020compare = "./newstdcompare2020/" 

path_to_2018compare = "./newstdcompare2018/" 

ext_of_compare = "_table.csv"

path_to_python ="C:/Users/Allen/pair_trading DL2"

path_to_half = "C:/Users/Allen/pair_trading DL2/2016/2016_half/"
path_to_2017half = "./2017_halfmin/"
path_to_2018half = "./2018_halfmin/"
ext_of_half = "_half_min.csv"
model_name = '201611_only_stock_price_return'

open, loss = 2, 1000#
trading_cost_threshold = 0.003
max_hold = 1000
trading_cost = 0.002
capital = 3000000000
cost_gate_Train = False
loading_data = False
dtype = {
    'S1' : str,
    'S2' : str,
    'VECMQ' : float,
    'mu': float,
    'Johansen_slope' : float,
    'stdev' : float,
    'model' : int,
    'w1' : float,
    'w2' : float
}


def test_reward():
    start_time = time.time()
    path_to_average = "./"+str(time)+"/averageprice/"
    ext_of_average = "_averagePrice_min.csv"
    path_to_minprice = "./"+str(time)+"/minprice/"
    ext_of_minprice = "_min_stock.csv"
    range_trading_cost_threshold = np.arange(0.0015,0.008,0.0005)
    number_of_label = len(range_trading_cost_threshold)
    total_reward = 0
    total_num = 0
    total_trade = [0,0,0]
    action_list = []
    action_list2 = []
    check = 0
    trading_history = []
    datelist = [f.split('_')[0] for f in os.listdir('D:/Allen/bitcoin_python/test')]
    #print(datelist)
    #print(datelist[167:])
    profit_count = 0
    count = 0
    #for date in sorted(datelist[:]): #決定交易要從何時開始
    for date in range(1):

        table = pd.read_csv('D:/Allen/bitcoin_python/Crypto_Currency_Cointegration/tmp/20211102_table.csv', dtype = dtype)
        tickdata = pd.read_csv('D:/Allen/bitcoin_python/test/2021-11-02_daily_min_price.csv')
        tickdata = tickdata.iloc[:480]
        tickdata.index = np.arange(0,len(tickdata),1)  
        num = np.arange(0,len(table),1)
        strategy = {
                    "up_open_time" : open,
                    "down_open_time" : open,
                    "stop_loss_time" : loss,
                    "maxhold" : max_hold,
                    "cost_gate" : trading_cost_threshold,
                    "capital" : capital,
                    "tax_cost" : trading_cost
                }
        #print(date)
        normal_table = table[table["model"]<4]
        print(normal_table[:10])
        total_normal = 0
        for index, row in normal_table[:10].iterrows():
            s1_tick = tickdata[row["S1"]]
            s2_tick = tickdata[row["S2"]]
            _trade, _profit, _capital, _return, _trading_rule,_history = trade_normal(s1_tick, s2_tick, row.to_dict(), strategy)
            total_normal += _profit
            total_trade[0] += _trading_rule[0]
            total_trade[1] += _trading_rule[1]
            total_trade[2] += _trading_rule[2] 
            total_num += _trade
            print(_trading_rule)
            table.at[index,"_return"] = _return * 100
            table.at[index,"_profit"] = _profit
            trading_history.append({
                "s1" : row["S1"],
                "s2" : row["S2"],
                "profit" : _profit * 1000,
                "return" : _return * 100,
                "capital" : _capital * 1000,
                "trade" : _trade,
                "history" : _history
            })
            print(f'each_profit : {_profit}')
        profit_count += sum([p > 0 for p in table["_profit"]])
        
    print(f'利潤 : {total_normal} and 開倉次數 : {total_num} and 開倉有賺錢的次數/開倉次數 : {profit_count/total_num}')
    print(f'開倉有賺錢次數 : {profit_count}')
    print("正常平倉 停損平倉 強迫平倉 :",total_trade[0],total_trade[1],total_trade[2])
    print("正常平倉率 :",total_trade[0]/total_num)
    print('Time used: {} sec'.format(time.time()-start_time))
    """
    if loading_data :
        reward,return_reward,per_reward,max_cap ,datelist = MDD.reward_calculation(path_to_profit)
        sharp_ratio, per_sharpe_ratio, mdd = MDD.plot_performance_with_dd(path_to_profit, reward,return_reward,per_reward,datelist,total_num,total_trade[0],profit_count/total_num,max_cap )
        print(f'{total_reward:.2f}')
        win_rate = profit_count/total_num * 100
        normal_close_rate = total_trade[0]/total_num * 100
        print(f'{win_rate:.2f}%/{normal_close_rate:.2f}%')
        print(f'{total_trade[0]},{total_trade[1]},{total_trade[2]},{total_num}')
        print(f'{sharp_ratio[0]:.4f}')
        print(f'{per_sharpe_ratio[0]:.4f}')
        profit_per_open = total_reward / total_num
        print(f'{profit_per_open:.4f}/{max_cap:.2f}/{mdd:.2f}')
    """
if __name__ == '__main__':
    test_reward()