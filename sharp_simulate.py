import pandas as pd
import numpy as np
import sqlite3

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
입력 : 수익률 데이터
출력 : 시뮬레이션 결과 데이터
* 멀티프로세싱 가능하게 패치 예정입니다.
'''

def simulation(pf_list, data):

    ## set simulate time
    time = 2500
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
        print(temp_array)
        
        dataframe_array.append(temp_array)

    simulated_data = pd.DataFrame(dataframe_array, columns = columns_list)

    ## 데이터 리턴
    return simulated_data


'''
수익률 데이터 저장 함수
입력 : 수익률(list)
출력 : 시뮬레이션 결과 데이터
'''

def save_profit_data(result_array):
    profit_data = pd.DataFrame()
    load_date()

    for i in month_list():
        ## 해당 월 데이터 추출
        sim_raw_data = simulation(data)
        sim_max_data = get_max_result(sim_raw_data)
    

    