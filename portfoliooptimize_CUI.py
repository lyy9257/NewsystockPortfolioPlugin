'''
샤프비 시뮬레이터 For command prompt
'''

# -*- coding: utf-8 -*-

## 패키지 불러오기
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from numba import jit

## 포트폴리오 최적화
class Opt_portfolio():

    ## 준비
    def __init__(self):
        ## 포트폴리오의 Number를 입력받아 Array Type로 저장
        self.pf_list = []


    ## 시뮬레이션 위한 포트폴리오 입력
    def read_portfolio(self, *portfolio_number):      
        self.pf_list = list(portfolio_number)[0].split()
        print("포트폴리오 갯수 : %d" %len(self.pf_list))


    ## 수익률 데이터 전처리
    def preprocess_tradedata(self):
        ## empty data to store preprocessd data
        temp= pd.DataFrame()
       
        ## store amount data to dataframe
        for i in range(len(self.pf_list)):
            portfolio_number = self.pf_list[i]
            filepath = "trade_history_daily_" + portfolio_number + '.csv'
            tradedata = pd.read_csv(filepath, header=0)
            temp['%s' %self.pf_list[i]] = tradedata['총자산'].astype(int)
        
        ## calculate profit data
        temp = np.log(temp/temp.shift(1))

        return temp
       

    ## 시뮬레이션
    @jit
    def random_portfolio_weight(self, data):
        ## set simulate time
        time = 2500
        columns_list = []

        for i in self.pf_list:
            columns_list.append('weights_%s' %i)

        columns_list.append('profit')
        columns_list.append('vollity')
        columns_list.append('Sharp_Ratio')

        '''
        포트폴리오 데이터셋이 N(1<N<6)이므로
        Array에 적재시켜 Dataframe에 저장시킨다.
        '''
      
        dataframe_array = []

        for p in range (time):

            temp_array = []

            '''
            weights_a[p] = weight[0]
            weights_b[p] = weight[1]
            '''

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

        simulated_data = pd.DataFrame(dataframe_array, columns = columns_list)

        ## 데이터 출력
        return simulated_data

    ## 그래프 작도
    @jit
    def draw_graph_sharp_ratio(self, data):
        data = simulated_data.sort_values(by='Sharp_Ratio', ascending=False)

        ## 출력 형식 : 시뮬레이션 순번, 비중 
        ## Max Sharp Ratio Top 5 출력
        print('- - - - - - - - -')
        print(data.head())
        print('- - - - - - - - -')

        ## 그래프 작도
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(13,6), sharex=True)
        data.plot(kind='scatter', ax=ax, x='vollity', y='profit', c='Sharp_Ratio', marker='+', cmap='plasma')
        
        ## 최대 Sharp Ratio에 따른 출력값 작성
        max_sharp_ratio_index = data['Sharp_Ratio'].idxmax()
        profit_max_SR = data.iloc[0].loc['profit']
        vol_max_SR = data.iloc[0].loc['vollity']
                  
        ## 최대 Sharp ratio일때 Vol, Profit 출력
        plt.scatter(vol_max_SR, profit_max_SR, c='Blue', marker='*', s=200)
        plt.title('[GenPort]Strategy Portfolio Simulation')

        ## 샤프비율 최대일때 수익률, 변동성 출력
        print("최대 샤프값 시뮬레이션 순번 : %d" %max_sharp_ratio_index)
        print('예상 수익률 : %.3f' % (profit_max_SR * 100))
        print('예상 변동성 : %.3f' % (vol_max_SR * 100))
        print('Sharp Ratio : %.3f' % data['Sharp_Ratio'].max())
        print(" ")
        for i in self.pf_list:
            temp_weight = data.iloc[0].loc['weights_%s' %i]
            print("%s 비중 : %.3f %%" %(i, temp_weight * 100))

        ## PNG로 출력 및 시현
        plt.savefig('sharp_simulate')
        plt.show()


## 시뮬레이션 기반으로 젠포트 포트폴리오별 자산배분
class run_backtest():

    ## 필요한 것들 준비
    ## 포트폴리오 넘버 리스트, 시뮬레이션 결과 데이터
    def __init__(self, pf_list, opt_data):
        self.pf_list = list(pf_list.split())
        self.count = len(pf_list)
        self.opt_data = opt_data 

        '''
        self.filepath_first = "trade_history_daily_536928.csv"
        self.filepath_second = "trade_history_daily_556120.csv"
        
        self.tradedata_first = pd.read_csv(self.filepath_first, header=0)
        self.tradedata_second = pd.read_csv(self.filepath_second, header=0)

        self.count = 2 ## Asset 갯수
        '''

        self.fee = 0.00015  # 수수료 0.015%

    ## 수익률 데이터 전처리
    @jit
    def preprocess_tradedata(self):
        ## empty data to store preprocessd data
        ## 날짜 - 각 PF별 누적수익 - 비중조절후 합한 누적수익
        temp_df = pd.DataFrame()
        max_sharp_ratio_area = self.opt_data['Sharp_Ratio'].idxmax()

        filepath = "trade_history_daily_" + self.pf_list[0] + '.csv'
        raw_data = pd.read_csv(filepath, header=0)
        temp_df['날짜'] = raw_data['날짜']
        temp_df['누적수익률_Opt'] = 0.000
        
        ## 누적 수익 저장
        for i in self.pf_list:
            pf_number = i
            filepath = "trade_history_daily_" + pf_number + '.csv'
            tradedata = pd.read_csv(filepath, header=0)
            temp_df['누적수익률_%s' %i] = tradedata['누적수익률'].astype(float)

        ## 전체 수익 저장
        for i in self.pf_list:
            weight_temp = self.opt_data.iloc[max_sharp_ratio_area].loc['weights_%s' %i] 
            temp_df['누적수익률_Opt'] = (temp_df['누적수익률_%s' %i] * weight_temp) + temp_df['누적수익률_Opt']

        temp_df['누적수익률'] = temp_df['누적수익률_Opt'].astype(float)/100+1.0
        temp_df['최고누적'] = temp_df['누적수익률'].rolling(min_periods=1, window=100).max()
        temp_df['DD'] = temp_df['누적수익률'] / temp_df['최고누적'] -1
        temp_df['MDD'] = temp_df['DD'].rolling(min_periods=1, window=1000).min()
        temp_df['HL'] = (temp_df['DD'] < 0).astype(int)*-1
        temp_df['HL'] = np.where(temp_df['DD']<0,-1,1)
        temp_df['HLcount'] = (temp_df.groupby((temp_df['HL'] != temp_df['HL'].shift(1)).cumsum()).cumcount()+1) * temp_df['HL']

        return temp_df            


	## matplotlib 이용 그래프 시현
    @jit
    def draw_graph(self, temp_df):
        d1 = str(temp_df['날짜'].iloc[0]) # 거래시작일
        d11 = datetime.strptime(d1, "%Y%m%d")
        d2 = str(temp_df['날짜'].iloc[-1]) # 거래종료일
        d22 = datetime.strptime(d2, "%Y%m%d")
        delta = d22-d11
        delta_days = delta.days
        period = delta_days/252 # 투자기간(년)

        MDD = round(temp_df['MDD'].min() * 100, 2)
        CAGR = round(temp_df['누적수익률'].iloc[-1] ** (1/period) * 100 - 100, 2)

        xtick_interval = 20 ## 20거래일 가로축
        plt.rcParams["figure.figsize"] = (14,7)
        png_ext = 'portfolio'
    
        plt.subplot(2,1,1) # row, column, index
        plt.yscale('log') # y-axis log scale
        plt.semilogy(temp_df['누적수익률'], color='#1F77B4')
        plt.semilogy(temp_df['최고누적'], color='#FF8D29')
        plt.xlabel('[Trading Day]')
        plt.ylabel('[Cumulative Return]')
        plt.legend(["Simulate CAGR : %.2f %%" %CAGR, "newHigh"])
        plt.xticks(np.arange(min(temp_df.index), max(temp_df.index) + 1, xtick_interval))
        plt.title('[GenPort]Strategy Portfolio Simulation - Cumulative Return')
        plt.grid(True)

        plt.subplot(2, 1, 2)
        plt.plot(temp_df['DD'], color='#FF8D29')
        plt.plot(temp_df['MDD'], color='#DA3F40')
        plt.xlabel('[Trading day]')
        plt.ylabel('[DrawDown]')
        plt.legend(["DD", "MDD : %.2f %%" %MDD])
        plt.xticks(np.arange(min(temp_df.index), max(temp_df.index) + 1, xtick_interval))
        plt.title('[GenPort]Strategy Portfolio Simulation - MDD')

        plt.tight_layout()
        plt.grid(True)
        plt.savefig('Genport_Curve_and_MDD_Simulation.png')

        plt.show()


    ## 성과 시현
    def show_result(self, temp_df):
        d1 = str(temp_df['날짜'].iloc[0]) # 거래시작일
        d11 = datetime.strptime(d1, "%Y%m%d")
        d2 = str(temp_df['날짜'].iloc[-1]) # 거래종료일
        d22 = datetime.strptime(d2, "%Y%m%d")
        delta = d22-d11
        delta_days = delta.days
        period = delta_days/252 # 투자기간(년)
        MDD = round(temp_df['MDD'].min() * 100, 2)
        CAGR = round(temp_df['누적수익률'].iloc[-1] ** (1/period) * 100 - 100, 2)
        
        print("- - - - - - - - - -")
        print("Predict CAGR : %.2f %%" %CAGR)
        print("Predict MDD : %.2f %%" %MDD)
        print("- - - - - - - - - -")


## 테스트
if __name__=="__main__":
    Opt_portfolio = Opt_portfolio()
    pf_list = input("포트폴리오 입력 :")
    
    Opt_portfolio.read_portfolio(pf_list)

    ## 최대 샤프비중 시뮬레이션
    processd_data = Opt_portfolio.preprocess_tradedata()
    simulated_data = Opt_portfolio.random_portfolio_weight(processd_data)
    Opt_portfolio.draw_graph_sharp_ratio(simulated_data)

    ## 포트폴리오 비중 배분 후 수익률 및 MDD Graph 시현
    Show_portfolio = run_backtest(pf_list, simulated_data)
    growth_data = Show_portfolio.preprocess_tradedata()
    Show_portfolio.draw_graph(growth_data)
    Show_portfolio.show_result(growth_data)
