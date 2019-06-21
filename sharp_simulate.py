#-*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import sqlite3
import multiprocessing as multi
import time

import get_result as get
import preprocess_data as preprocess 

'''
포트폴리오 리딩 함수
입력 : 포트폴리오 리스트(str)
출력 : 포트폴리오 리스트(list)
'''

def read_pf_list(*pf_number):      
    pf_list = list(pf_number)[0].split()
    return pf_list


'''
시뮬레이션 함수
입력 : 포트폴리오 리스트, 로그수익률 데이터프레임
출력 : 시뮬레이션 결과 데이터
* 멀티프로세싱으로 500 * 4회 시뮬레이션 실시
'''

def simulation(multi_map):

    ## set simulate time
    time = 500
    pf_list = multi_map[0]
    data = multi_map[1]

    columns_list = []

    for i in pf_list:
        columns_list.append('weights_%s' %i)

    columns_list.append('profit')
    columns_list.append('vollity')
    columns_list.append('Sharp_Ratio')

    '''
    포트폴리오 데이터셋이 N(1 < N < 6)이므로
    Array에 적재시켜 Dataframe에 저장시킨다.
    '''
      
    dataframe_array = []

    ## 몬테카를로 시뮬레이션
    ## 비중, 수익, 변동성, 샤프비 저장
    for p in range (time):

        temp_array = []

        weight = np.array(np.random.random(len(pf_list))) 
        weight /= np.sum(weight)

        for i in range(len(weight)):
            temp_array.append(weight[i])
                
        profits = np.sum((data.mean() * weight) * 252)
        vols = np.sqrt(np.dot(weight.T, np.dot(data.cov() * 252, weight)))
        sharps = profits/vols

        temp_array.append(profits)
        temp_array.append(vols)
        temp_array.append(sharps)
        
        dataframe_array.append(temp_array)

    simulated_data = pd.DataFrame(dataframe_array, columns = columns_list)

    ## 데이터 리턴
    return simulated_data


'''
멀티프로세싱용 시뮬레이션 함수
입력 : 포트폴리오 리스트(list), 로그수익률 데이터(DataFrame)
출력 : 샤프비 비중 배분 데이터(DataFrame)
'''

def simulation_multi(pf_list, data):
    start_time = time.time()

    data_map = [[pf_list, data], [pf_list, data], [pf_list, data], [pf_list, data]]
    pool = multi.Pool(processes = 4) # 4개의 프로세스
    simulated_data = pd.concat(pool.map(simulation, data_map)) # 실시
    
    ## print("시뮬레이션 시간 : %.3f seconds" % (time.time() - start_time))
    return simulated_data


'''
월별 시뮬레이션 함수
입력 : 포트폴리오 리스트(list), 투자 월 리스트(list), 로그수익률 데이터(DataFrame)
출력 : 월별 샤프비 비중 배분 데이터(최대값, DataFrame)
'''

def simulation_month(pf_list, month_list, data):

    ## 월 데이터 추가
    filepath = "trade_history_daily_" + pf_list[0] + '.csv'
    tradedata = pd.read_csv(filepath, header=0)
    data['YearMonth'] = tradedata['날짜'].astype(str).str.slice(stop=6)
    data = data.dropna()

    ## 칼럼 리스트 제작    
    columns_list = []
    columns_list.append('YearMonth')

    for i in pf_list:
        columns_list.append('weights_%s' %i)
    
    ## 데이터 제작
    temp = []
    
    for i in month_list:
        temp_array = []

        ## 첫달은 균등 리밸런싱
        if i == month_list[0]:
            weight = round(1/len(pf_list), 3)
            temp_array.append(i)
            for i in range (len(pf_list)):
                temp_array.append(weight)

        ## 그 다음달부터 샤프비 리밸런싱
        else:
            in_data = data[data.YearMonth == i].drop('YearMonth', axis = 1)
            sim_data = simulation_multi(pf_list, in_data)
            max_data = get.max_sharp(pf_list, sim_data)[3:]    
            temp_array.append(i)
            
            for weight in max_data:
                temp_array.append(weight)
         
        temp.append(temp_array)
        
    final_data = pd.DataFrame(temp, columns = columns_list)
    
    return final_data


'''
모듈 테스트용
'''

'''
if __name__ == '__main__':
    import draw_graph as draw

    pf = '622324 615717 620241'

    ## 월별 샤프비 비중 계산
    pf_list = preprocess.read_pf_list(pf)
    month_list = preprocess.get_month_data(pf_list)
    log_profit_data = preprocess.profit_to_log(pf_list)
    
    ## 샤프비 비중 계산 후 시뮬레이션
    weight_data = simulation_month(pf_list, month_list, log_profit_data)
    profit_data = preprocess.trade_data_month(pf_list, month_list, weight_data)

    ## 그래프 작도
    draw.profit(profit_data)
'''