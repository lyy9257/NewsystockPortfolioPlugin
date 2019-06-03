# -*- coding: utf-8 -*-

import pandas as pd
import sqlite3

'''
데이터 전처리 class
Input : Portfolio list(str)
Output : Processed data(DB file for SQLite3)
'''

class preprocess_data():

    ## 준비
    def __init__(self):
        self.pf_list = []
        self.temp = pd.DataFrame()


    ## 포트폴리오 리스트로 변환
    def read_pf_list(self, *pf_number):      
        self.pf_list = list(pf_number)[0].split()
        return self.pf_list
    

    ## 수익률 데이터 호출 후 합병
    def import_data(self):
        
        ## store month data`
        filepath = "trade_history_daily_" + self.pf_list[0] + '.csv'    
        tradedata = pd.read_csv(filepath, header=0)
        self.temp['date'] = tradedata['날짜'].astype(int)
        self.temp['YearMonth'] = tradedata['날짜'].astype(str).str.slice(stop=6)

        ## store profit and amount data
        for pf_num in self.pf_list:
            tradedata = pd.read_csv(filepath, header=0)
            self.temp['%s_profit' %pf_num] = tradedata['일일수익률'].astype(float)
            self.temp['%s_amount' %pf_num] = tradedata['총자산'].astype(int)
           
        return self.temp
   

    ## SQLite3 Database 데이터로 저장
    def store_data(self):
        try:
            con = sqlite3.connect("profit_data.db")
            self.temp.to_sql('profit_data', con)
            print("Store")
        except:
            print("Already Stored")
            
        return True


'''
샤프비 시뮬레이션 class
Input : Portfolio list(str)
        Preprocessed data(SQLite3 DB File)
Output : weight(Dataframe)
'''
class sharp_simulation():
    
    def __init__(self):
        self.con = sqlite3.connect("/profit_data.db")3
        self.data = pd.read_sql("SELECT * FROM profit_data", self.con, index_col=None)
        self.pf_list = []
        self.month_list = []
        self.column_list = []
    

    '''
    포트폴리오 리딩 함수
    입력 : 포트폴리오 리스트(str)
    출력 : 포트폴리오 리스트(list)
    '''
    def read_pf_list(self, *pf_number):      
        self.pf_list = list(pf_number)[0].split()
        return self.pf_list
    

    '''
    데이터 로딩 함수
    입력 : 수익률 데이터
    출력 : 시뮬레이션 결과 데이터
    '''
    def load_data(self):
        self.month_list = self.data['date'].drop_duplicates()


    '''
    시뮬레이션 함수
    입력 : 수익률 데이터
    출력 : 시뮬레이션 결과 데이터
    '''
    def simulation(self, data):
        ## set simulate time
        time = 2500
        
        for i in self.pf_list:
            self.columns_list.append('weights_%s' %i)

        self.columns_list.append('profit')
        self.columns_list.append('vollity')
        self.columns_list.append('Sharp_Ratio')

        '''
        포트폴리오 데이터셋이 N(1<N<6)이므로
        Array에 적재시켜 Dataframe에 저장시킨다.
        '''
      
        dataframe_array = []

        ## 몬테카를로 시뮬레이션
        ## 비중, 수익, 변동성, 샤프비 저장
        for p in range (time):

            temp_array = []

            weight = np.array(np.random.random(len(self.pf_list))) 
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

        simulated_data = pd.DataFrame(dataframe_array, columns = self.columns_list)

        ## 데이터 리턴
        return simulated_data


    '''
    최대값 출력 함수
    입력 : 시뮬레이션 데이터(Dataframe)
    출력 : 시뮬레이션 최대값(list)
    ''''
    def get_max_result(self, data):
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
        for i in self.pf_list:
            temp_weight = data.iloc[0].loc['weights_%s' %i]
            result_array.append(temp_weight)  
            
        ## 어레이 리턴(수익률 - 변동성 - 샤프비 - 각 포트별 비중)
        return result_array


    '''
    수익률 데이터 저장 함수
    입력 : 수익률(list)
    출력 : 시뮬레이션 결과 데이터
    '''
    def save_profit_data(self, result_array):
        profit_data = pd.DataFrame()
        self.load_date()

        for i in self.month_list():
            ## 해당 월 데이터 추출
            sim_raw_data = self.simulation(data)
            
class draw_graph():

    def __init__(self):

        return 0
     
if __name__ == '__main__':
    pf_list = '536928 549289 556120 566420 586167'
    preprocess_data = preprocess_data()
    preprocess_data.read_pf_list(pf_list)
    preprocess_data.import_data()
    preprocess_data.store_data()


    