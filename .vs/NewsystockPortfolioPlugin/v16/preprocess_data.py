#-*- coding:utf-8 -*-

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


## 엑셀 데이터 엑세스
def excess_csv_data(pf_num):
    filepath = "trade_history_daily_" + pf_num + '.csv'    
    tradedata = pd.read_csv(filepath, header=0)
    
    return tradedata
    

## 수익률 데이터 호출 후 합병
def import_profit_data(pf_list):
    
    ## Make Empty DataFrame to store data
    temp = pd.DataFrame()
    tradedata = excess_csv_data(pf_list[0])
    temp['date'] = tradedata['날짜'].astype(int)
    temp['YearMonth'] = temp['date'].astype(str).str.slice(stop=6)

    ## store profit and amount data
    for pf_num in pf_list:
        tradedata = excess_csv_data(pf_num)
        temp['%s_profit' %pf_num] = tradedata['일일수익률'].astype(float)
           
    return temp
   

## 일별자산 데이터 호출 후 합병
def import_account_data(pf_list):
    
    ## Make Empty DataFrame to store data
    temp = pd.DataFrame()

    tradedata = excess_csv_data(pf_list[0])
    temp['date'] = tradedata['날짜'].astype(int)
    temp['YearMonth'] = temp['date'].astype(str).str.slice(stop=6)

    ## store profit and amount data
    for pf_num in pf_list:
        tradedata = excess_csv_data(pf_num)
        temp['%s_amount' %pf_num] = tradedata['총자산'].astype(int)
           
    return temp
   

## 월 데이터 호출
def get_month_data(pf_list):
    
    ## Make Empty DataFrame to store data
    temp = pd.Series()

    ## store month data
    tradedata = excess_csv_data(pf_list[0])
    temp = tradedata['날짜'].astype(str).str.slice(stop=6).drop_duplicates()
    
    temp = np.array(temp)

    return temp


## 수익률 데이터 로그화
def profit_to_log(pf_list):

    ## empty data to store preprocessd data
    temp= pd.DataFrame()
       
    ## store amount data to dataframe
    for num in pf_list:
        tradedata = excess_csv_data(num)
        temp['%s' %num] = tradedata['총자산'].astype(int)
        
    ## calculate profit data
    temp = np.log(temp/temp.shift(1))

    return temp


## 월별 수익률 배분
def trade_data_month(pf_list, month_list, weight_data):
    
    ## 여기서부터 
    profit_data = pd.DataFrame()

    raw_data = excess_csv_data(pf_list[0])
    profit_data['날짜'] = raw_data['날짜']
    profit_data['YearMonth'] = profit_data['날짜'].astype(str).str.slice(stop=6)
    
    temp = pd.DataFrame()

    ## 누적 수익 저장
    for num in pf_list:
        tradedata = excess_csv_data(num)
        profit_data['일일수익률_%s' %num] = tradedata['일일수익률'].div(100).astype(float)
    
    ## 여기까지 독립화 예정

    ## 전체 수익 저장
    for num in month_list:
        profit_temp = profit_data[profit_data.YearMonth == num].drop(columns=['날짜', 'YearMonth'], axis = 1)
        weight_temp = weight_data[weight_data.YearMonth == num].drop('YearMonth', axis = 1)
        multiply_temp = pd.DataFrame(profit_temp.values * weight_temp.values, columns = pf_list)
        temp = pd.concat([temp, multiply_temp.sum(axis=1)])

    profit_data['일일수익률_Opt'] = temp.reset_index(drop=True)
    profit_data['누적수익률'] = (np.cumprod(1 + profit_data['일일수익률_Opt'].values))
   
    profit_data['최고누적'] = profit_data['누적수익률'].rolling(min_periods = 1, window = len(profit_data.index)).max()
    profit_data['DD'] = profit_data['누적수익률'] / profit_data['최고누적'] - 1
    profit_data['MDD'] = profit_data['DD'].rolling(min_periods = 1, window = len(profit_data.index)).min()
    profit_data['cummax'] = profit_data['누적수익률_Opt'].cummax()
    profit_data['underwater'] = profit_data['누적수익률_Opt'] < profit_data['cummax']
    
    print(profit_data['cummax'])

    for num in pf_list:
        profit_data.drop(columns ='일일수익률_%s' %num)
 
    try:
        os.delete('weight_month.csv')
        os.delete('result_month.csv')

    except:
        pass        

    weight_data.to_csv('weight_month.csv', encoding='ms949') 
    profit_data.to_csv('result_month.csv', encoding='ms949')  
 
    return profit_data



## 수익률 데이터 전처리
def trade_data(pf_list, data):

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

    df['cummax'] = df['누적수익률'].cummax()
    df['underwater'] = df['누적수익률'] < df['cummax']

    ## csv 파일로 Export
    try:
        os.delete('result_onetime.csv')

    except:
        pass        

    df.to_csv('result_onetime.csv', encoding='ms949')  
 
    ## 수익률 데이터 반환
    return df


def count_max_underwater(df):
    temp = []

    for i in range(len(df.index)):
        if df["underwater"].iat[i] == "true":
            if(i = 0):
                temp.append(1)

            else:
                temp.append(temp(i-1))
        else:
            temp.append(0)

    df["underwater_count"] = temp
    
    return df

## SQLite3 Database 데이터로 저장
def store_data(profit_data, account_data):
    con = sqlite3.connect("profit_data.db")
    profit_data.to_sql('profit_data', con)
    account_data.to_sql('account_data', con)
    print("Store")         
    return True

