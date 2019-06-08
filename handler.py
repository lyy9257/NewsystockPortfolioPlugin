'''
인터페이스 Module
'''

import pandas as pd
import sqlite3
import multiprocessing

import preprocess_data as pdata
import sharp_simulate as sim
import draw_graph as draw
import get_result as get 
  

'''
단독 샤프비 시뮬레이션
1. 포트폴리오 읽기
2. 수익률 데이터 추출 및 전처리
3. 시뮬레이션
4. 포트폴리오별 자산배분
'''

class onetime_sharp_simulation():
    def __init__(self):
        self.pf_list = []
        
        ## 수익률 데이터, 자본금 데이터
        self.profit_data = pd.DataFrame()
        self.amount_data = pd.DataFrame()
        
        ## 로그수익률 데이터, 샤프비 데이터, 수익 데이텨
        self.log_profit_data = pd.DataFrame()
        self.sharp_data = pd.DataFrame()
        self.profit_data = pd.DataFrame()
        self.max_result_data = []
        self.cagr_data = []

        self.fee = 0.015
        

    def get_pf_list(self, pf_str):
        self.pf_list = pdata.read_pf_list(pf_str)
        return self.pf_list


    def preprocess_data(self):
        self.profit_data = pdata.import_profit_data(self.pf_list) 
        self.amount_data = pdata.import_account_data(self.pf_list)           
        self.log_profit_data = pdata.profit_to_log(self.pf_list)
        return True


    def simulate(self):
        self.sharp_data = sim.simulation_multi(self.pf_list, self.log_profit_data)
        return True
       

    def draw_graph(self):
        self.profit_data = pdata.preprocess_trade_data(self.pf_list, self.sharp_data)
        draw.sharp_ratio(self.sharp_data)
        draw.profit(self.profit_data)

        return True


    def get_sharp_result(self):
        self.max_result_data = get.max_sharp(self.pf_list, self.sharp_data)
        return self.max_result_data
    

    def get_cagr_result(self):
        self.cagr_data = get.cagr_mdd(self.profit_data)
        return self.cagr_data


'''
월별 샤프비 시뮬레이션
1. 포트폴리오 읽기
2. 수익률 데이터 추출 및 전처리
3. 시뮬레이션
4. 포트폴리오별 자산배분
'''

class month_sharp_simulation():
    def __init__(self):
        self.pf_list = []
        
        ## 수익률 데이터, 자본금 데이터
        self.profit_data = pd.DataFrame()
        self.amount_data = pd.DataFrame()
        
        ## 로그수익률 데이터, 샤프비 데이터, 수익 데이텨
        self.log_profit_data = pd.DataFrame()
        self.sharp_data = pd.DataFrame()
        self.profit_data = pd.DataFrame()
        self.max_result_data = []
        self.cagr_data = []

        self.fee = 0.015
        

    def get_pf_list(self, pf_str):
        self.pf_list = pdata.read_pf_list(pf_str)
        return self.pf_list


    def preprocess_data(self):
        self.profit_data = pdata.import_profit_data(self.pf_list) 
        self.amount_data = pdata.import_account_data(self.pf_list)           
        self.log_profit_data = pdata.profit_to_log(self.pf_list)
        return True


    def simulate(self):
        self.sharp_data = sim.simulation_multi(self.pf_list, self.log_profit_data)
        return True
       

    def draw_graph(self):
        self.profit_data = pdata.preprocess_trade_data(self.pf_list, self.sharp_data)
        draw.sharp_ratio(self.sharp_data)
        draw.profit(self.profit_data)

        return True


    def get_sharp_result(self):
        self.max_result_data = get.max_sharp(self.pf_list, self.sharp_data)
        return self.max_result_data
    

    def get_cagr_result(self):
        self.cagr_data = get.cagr_mdd(self.profit_data)
        return self.cagr_data