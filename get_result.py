#-*- coding:utf-8 -*-

from datetime import datetime
import numpy as np
import pandas as pd

'''
투자 년수 산출 함수
입력 : 시뮬레이션 데이터(Dataframe)
출력 : period(int)
'''

def period(data):
    try:
        d1 = str(data['date'].iloc[0]) # 거래시작일
        d11 = datetime.strptime(d1, "%Y%m%d")
        d2 = str(data['date'].iloc[-1]) # 거래종료일
        d22 = datetime.strptime(d2, "%Y%m%d")
        delta = d22-d11
        delta_days = delta.days
        period = delta_days/252 # 투자기간(년)

    except:
        d1 = str(data['날짜'].iloc[0]) # 거래시작일
        d11 = datetime.strptime(d1, "%Y%m%d")
        d2 = str(data['날짜'].iloc[-1]) # 거래종료일
        d22 = datetime.strptime(d2, "%Y%m%d")
        delta = d22-d11
        delta_days = delta.days
        period = delta_days/252 # 투자기간(년)

    return period


'''
CAGR, MDD 출력 함수
입력 : 시뮬레이션 데이터(Dataframe)
출력 : CAGR, MDD(list)
'''

def cagr_mdd(data, period):

    ## CAGR, MDD 계산
    CAGR = round(data['누적수익률'].iloc[-1] ** (1/period) * 100 - 100, 2)
    MDD = round(data['MDD'].min() * 100, 2)
         
    ## 결과 저장용 어레이에 저장
    result_array = []
    result_array.append(CAGR)
    result_array.append(MDD)
        
    return result_array


'''
최대값 출력 함수
입력 : 시뮬레이션 데이터(Dataframe)
출력 : 시뮬레이션 최대값(list)
'''

def max_sharp(pf_list, data):
    data = data.sort_values(by='Sharp_Ratio', ascending=False)
    result_array = []

    ## 최대 Sharp Ratio에 따른 출력값 작성
    max_sharp_ratio_index = data['Sharp_Ratio'].idxmax() ## 최대값 시뮬레이션 순번
    profit_max_SR = round(data.iloc[0].loc['profit'], 3) ## 수익률
    vol_max_SR = round(data.iloc[0].loc['vollity'], 3) ## 변동성
    sharp_ratio = round(profit_max_SR/vol_max_SR, 3)  ## 샤프비

    ## 결과 어레이에 저장
    result_array.append(profit_max_SR)
    result_array.append(vol_max_SR)
    result_array.append(sharp_ratio)

    ## 결과 어레이에 비중 저장
    for i in pf_list:
        temp_weight = data.iloc[0].loc['weights_%s' %i]
        result_array.append(round(temp_weight, 5))  
            
    ## 어레이 리턴(수익률 - 변동성 - 샤프비 - 각 포트별 비중)
    return result_array


'''
언더워터 출력함수
입력 : 시뮬레이션 데이터(Dataframe)
출력 : 시뮬레이션 최대값(list)
'''

def underwater_period():
    df['cummax'] = df['A'].cummax()
    df['underwater'] = df['A'] < df['cummax']
    print(df)
    print('total:', df['underwater'].sum())