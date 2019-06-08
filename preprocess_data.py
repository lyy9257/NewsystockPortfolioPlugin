'''
데이터 전처리 모듈
'''

import numpy as np
import pandas as pd
import sqlite3

## 포트폴리오 리스트로 변환
def read_pf_list(*pf_number):      
    pf_list = list(pf_number)[0].split()
    return pf_list
    

## 수익률 데이터 호출 후 합병
def import_profit_data(pf_list):
    
    ## Make Empty DataFrame to store data
    temp = pd.DataFrame()

    ## store month data
    filepath = "trade_history_daily_" + pf_list[0] + '.csv'    
    tradedata = pd.read_csv(filepath, header=0)
    temp['date'] = tradedata['날짜'].astype(int)
    temp['YearMonth'] = tradedata['날짜'].astype(str).str.slice(stop=6)

    ## store profit and amount data
    for pf_num in pf_list:
        tradedata = pd.read_csv(filepath, header=0)
        temp['%s_profit' %pf_num] = tradedata['일일수익률'].astype(float)
           
    return temp
   

## 일별자산 데이터 호출 후 합병
def import_account_data(pf_list):
    
    ## Make Empty DataFrame to store data
    temp = pd.DataFrame()

    ## store month data
    filepath = "trade_history_daily_" + pf_list[0] + '.csv'    
    tradedata = pd.read_csv(filepath, header=0)
    temp['date'] = tradedata['날짜'].astype(int)
    temp['YearMonth'] = tradedata['날짜'].astype(str).str.slice(stop=6)

    ## store profit and amount data
    for pf_num in pf_list:
        tradedata = pd.read_csv(filepath, header=0)
        temp['%s_amount' %pf_num] = tradedata['총자산'].astype(int)
           
    return temp
   

## 월 데이터 호출
def get_month_data(pf_list):
    
    ## Make Empty DataFrame to store data
    temp = pd.Series()

    ## store month data
    filepath = "trade_history_daily_" + pf_list[0] + '.csv'    
    tradedata = pd.read_csv(filepath, header=0)
    temp = tradedata['날짜'].astype(str).str.slice(stop=6).drop_duplicates()
    
    temp = np.array(temp)

    return temp


## 수익률 데이터 로그화
def profit_to_log(pf_list):
    ## empty data to store preprocessd data
    temp= pd.DataFrame()
       
    ## store amount data to dataframe
    for i in range(len(pf_list)):
        pf_number = pf_list[i]
        filepath = "trade_history_daily_" + pf_number + '.csv'
        tradedata = pd.read_csv(filepath, header=0)
        temp['%s' %pf_list[i]] = tradedata['총자산'].astype(int)
        
    ## calculate profit data
    temp = np.log(temp/temp.shift(1))

    return temp


## 수익률 데이터 전처리
def preprocess_trade_data(pf_list, data):
    ## empty data to store preprocessd data
    ## 날짜 - 각 PF별 누적수익 - 비중조절후 합한 누적수익
    df = pd.DataFrame()
    max_sharp_ratio_area = data['Sharp_Ratio'].idxmax()

    filepath = "trade_history_daily_" + pf_list[0] + '.csv'
    raw_data = pd.read_csv(filepath, header=0)
    df['날짜'] = raw_data['날짜']
    df['누적수익률_Opt'] = 0.000
        
    ## 누적 수익 저장
    for i in pf_list:
        pf_number = i
        filepath = "trade_history_daily_" + pf_number + '.csv'
        tradedata = pd.read_csv(filepath, header=0)
        df['누적수익률_%s' %i] = tradedata['누적수익률'].astype(float)

    ## 전체 수익 저장
    for i in pf_list:
        weight_temp = data.iloc[max_sharp_ratio_area].loc['weights_%s' %i] 
        df['누적수익률_Opt'] = (df['누적수익률_%s' %i] * weight_temp) + df['누적수익률_Opt']

    df['누적수익률'] = df['누적수익률_Opt'].astype(float)/100+1.0
    df['최고누적'] = df['누적수익률'].rolling(min_periods=1, window=100).max()
    df['DD'] = df['누적수익률'] / df['최고누적'] -1
    df['MDD'] = df['DD'].rolling(min_periods=1, window=1000).min()
    df['HL'] = (df['DD'] < 0).astype(int)*-1
    df['HL'] = np.where(df['DD']<0,-1,1)
    df['HLcount'] = (df.groupby((df['HL'] != df['HL'].shift(1)).cumsum()).cumcount()+1) * df['HL']

    return df


## SQLite3 Database 데이터로 저장
def store_data(profit_data, account_data):
    con = sqlite3.connect("profit_data.db")
    profit_data.to_sql('profit_data', con)
    account_data.to_sql('account_data', con)
    print("Store")         
    return True


## Module Test
if __name__ == '__main__':
    pf = '536928 549289 556120 566420 586167'
    pf_list = read_pf_list(pf)
    get_month_data(pf_list)
