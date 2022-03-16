#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 18:50:19 2021

@author: allen
"""
import os 
import zipfile
import pandas as pd
from utility import download_file, get_all_symbols, get_parser, get_start_end_date_objects, convert_to_date_object
import sys
from datetime import *
from enums import *
from pathlib import Path

def zip_list(file_path,bitcoin):
    zf = zipfile.ZipFile(os.path.join(file_path,bitcoin),'r')
    print(zf.namelist()[0])
    zf.extract(zf.namelist()[0],file_path)
    #os.remove(os.path.join(file_path,bitcoin))

def read_csv_file(file):
    
    head_list = ["Open time","Open","High","Low","Close","Volume","Close time",
                  "Quote asset volume","Number of trades","Taker buy base asset volume",
                  "Taker buy quote asset volume","ignore"]
    df = pd.read_csv(file,names = head_list)
    print(df.columns)
    return df


def caculate_price(df):
    
    print(df[["Open","High","Low","Close"]])
    #new_df = df[['Open','High','Low','Close']].mean(axis = 1)
    
    return df["Close"].tolist()
    

def create_file():
    
    pass
    
def combine_bitcoin(start_date,end_date,intervals,root,test,choose):
    if start_date and end_date:
        date_range = start_date + " " + end_date

    if not start_date:
          start_date = START_DATE
    else:
         start_date = convert_to_date_object(start_date)

    if not end_date:
         end_date = END_DATE
    else:
        end_date = convert_to_date_object(end_date)
    if not os.path.exists(test):
         os.makedirs(test)
    for date in dates:
        bitcoin_frame = pd.DataFrame()
        current_date = convert_to_date_object(date)
        if current_date >= start_date and current_date <= end_date:
            """
            path = "{}_daily_min_price".format(date)
            saving_path = os.path.join(test,path)
            if not os.path.exists(saving_path) :
                os.makedirs(saving_path)
            """
            for file in sorted(all_bitcoin) :
                if count == 1 :
                    break
                file_root = os.path.join(root+file,intervals[0])
                print(file_root)
                bitcoin = "{}-{}-{}.zip".format(file,intervals[0],date)
                bitcoin_csv = "{}-{}-{}.csv".format(file,intervals[0],date)
                
                print(bitcoin)
                if choose == 0 :
                    if os.path.isfile(os.path.join(file_root,bitcoin)):
                        print("File exist")
                        zip_list(file_root, bitcoin)
                    else :
                        print("zip file is not exist")
                        continue
                # 做crpytocurrency的資料合併
                if bitcoin :
                    bitcoin_file = read_csv_file(os.path.join(file_root,bitcoin_csv))
                    print(bitcoin_file)
                    bitcoin_price = caculate_price(bitcoin_file)
                    print(bitcoin_price)
                    print(bitcoin_csv)
                    #if len(bitcoin_price) == 288 :                                             
                    bitcoin_frame[bitcoin_csv.split('-',2)[0]] = pd.Series(bitcoin_price)
            bitcoin_frame.fillna(method='ffill')   
            print(bitcoin_frame.empty)
            bitcoin_frame.to_csv(test+"{}_daily_min_price.csv".format(date), index = False)
if __name__ == "__main__" :
    #zip_list('./data/BTCTUSD/1m/BTCTUSD-1m-2021-07-01.zip')
    parser = get_parser('combine')
    args = parser.parse_args(sys.argv[1:])
    test = './BTC_ETH_Table_1min/'
    root = './BTC_ETH/'
    all_bitcoin = sorted(os.listdir(root))
    print(all_bitcoin)
    count = 0
    choose = 0
    dates =['2021-11-02','2021-11-03']
    intervals = ['1m']
    """
    if args.dates:
      dates = args.dates
    else:
    """
    dates = pd.date_range(end = datetime.today(), periods = MAX_DAYS).to_pydatetime().tolist()
    dates = [date.strftime("%Y-%m-%d") for date in dates]
    combine_bitcoin(args.startDate, args.endDate,intervals,root,test,choose)
    
        #bitcoin_frame.to_csv(test+"{}_daily_min_price.csv".format(date), index = False)
        

        
        
            
