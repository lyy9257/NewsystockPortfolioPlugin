# -*- coding: utf-8 -*-

## 패키지 생성
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import dates
import matplotlib.font_manager as font_manager
import numpy as np
import pandas as pd
import seaborn as sns

'''
# 맑은고딕체
sns.set(style="whitegrid", font="Malgun Gothic", font_scale=1.0)
matplotlib.rcParams['figure.figsize'] = [12, 8]
fp = font_manager.FontProperties(fname="C:\\WINDOWS\\Fonts\\malgun.TTF", size=10)

'''

## 포트폴리오 최적화
class Opt_portfolio():

    ## 준비
    def __init__(self):
        ## 포트폴리오의 Number를 입력받아 Array Type로 저장
        self.portfolio_list = []


    ## 시뮬레이션 위한 포트폴리오 입력
    def read_portfolio(self, *portfolio_number):      
        self.portfolio_list = list(portfolio_number)[0].split()

        print("포트폴리오 갯수 : %d" %len(self.portfolio_list))


    ## 수익률 데이터 전처리
    def preprocess_tradedata(self):
        ## empty data to store preprocessd data
        temp= pd.DataFrame()
       
        ## store amount data to dataframe
        for i in range(len(self.portfolio_list)):
            portfolio_number = self.portfolio_list[i]
            filepath = "trade_history_daily_" + portfolio_number + '.csv'
            tradedata = pd.read_csv(filepath, header=0)
            temp['%s' %self.portfolio_list[i]] = tradedata['총자산'].astype(int)
        
        ## calculate profit data
        temp = np.log(temp/temp.shift(1))

        return temp
       

    ## 시뮬레이션
    def random_portfolio_weight(self, data):
        ## set simulate time
        time = 2500
        columns_list = []

        for i in range(len(self.portfolio_list)):
            columns_list.append('weights_%s' %self.portfolio_list[i])

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

            weight = np.array(np.random.random(len(self.portfolio_list))) 
            weight /= np.sum(weight)

            for i in range(len(weight)):
                temp_array.append(weight[i])
                
            profits = np.sum((data.mean() * weight) * 365)
            vols = np.sqrt(np.dot(weight.T, np.dot(data.cov() * 365, weight)))
            sharps = profits/vols

            temp_array.append(profits)
            temp_array.append(vols)
            temp_array.append(sharps)
            
            dataframe_array.append(temp_array)

        simulated_data = pd.DataFrame(dataframe_array, columns = columns_list)
        simulated_data = simulated_data.sort_values(by='Sharp_Ratio', ascending=False)

        print('- - - - - - - - -')
        print(simulated_data.head())
        print('- - - - - - - - -')

        return simulated_data

    ## 그래프 작도
    def draw_graph_sharp_ratio(self, data):

        ## 그래프 작도
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(13,6), sharex=True)
        data.plot(kind='scatter', ax=ax, x='vollity', y='profit', c='Sharp_Ratio', marker='X', cmap='plasma')
        plt.scatter(data['vollity'], data['profit'], c='red', s=5)

        ## 최대 Sharp Ratio에 따른 출력값 작성
        max_sharp_ratio_index = data['Sharp_Ratio'].idxmax()
        profit_max_SR = data.iloc[max_sharp_ratio_index].loc['profit']
        vol_max_SR = data.iloc[max_sharp_ratio_index].loc['vollity']
        
        '''
        max_weight_A = data.iloc[max_sharp_ratio].loc['weights_A']
        max_weight_B = data.iloc[max_sharp_ratio].loc['weights_B']
        '''
            
        plt.scatter(vol_max_SR, profit_max_SR, c='Blue', marker='*', s=200)

        ## 샤프비율 최대일때 수익률, 변동성 출력
        print("최대 샤프값 시뮬레이션 순번 : %d" %max_sharp_ratio_index)
        print('예상 수익률 : %.3f' % (profit_max_SR * 100))
        print('예상 변동성 : %.3f' % (vol_max_SR * 100))
        print('Sharp Ratio : %.3f' % data['Sharp_Ratio'].max())

        plt.savefig('sharp_simulate')
        plt.show()


## 시뮬레이션 기반으로 젠포트 포트폴리오별 자산배분
class run_backtest():

    ## 필요한 것들 준비
    def __init__(self):
        self.filepath_first = "trade_history_daily_536928.csv"
        self.filepath_second = "trade_history_daily_556120.csv"
        
        self.tradedata_first = pd.read_csv(self.filepath_first, header=0)
        self.tradedata_second = pd.read_csv(self.filepath_second, header=0)

        self.fee = 0.00015  # 수수료 0.015%

        self.count = 2 ## Asset 갯수


## 거래 데이터 가공
    def process_trade_data(self, data):
        temp_df = pd.DataFrame()

        max_sharp_ratio = data['Sharp_Ratio'].idxmax()
        profit_max_SR = data.iloc[max_sharp_ratio].loc['Profit']
        vol_max_SR = data.iloc[max_sharp_ratio].loc['Vollity']
        max_weight_A = data.iloc[max_sharp_ratio].loc['weights_A']
        max_weight_B = data.iloc[max_sharp_ratio].loc['weights_B']

        weight_array = [max_weight_A, max_weight_B]

        temp_df['날짜'] = self.tradedata_first['날짜']
        temp_df['누적수익률_A'] = self.tradedata_first['누적수익률']
        temp_df['누적수익률_B'] = self.tradedata_second['누적수익률']
        temp_df['누적수익률_Opt'] = temp_df['누적수익률_A'] * weight_array[0] + temp_df['누적수익률_B'] * weight_array[1]

        temp_df['누적수익률'] = temp_df['누적수익률_Opt'].astype(float)/100+1.0
        temp_df['최고누적'] = temp_df['누적수익률'].rolling(min_periods=1, window=100).max()
        temp_df['DD'] = temp_df['누적수익률'] / temp_df['최고누적'] -1
        temp_df['MDD'] = temp_df['DD'].rolling(min_periods=1, window=1000).min()
        temp_df['HL'] = (temp_df['DD'] < 0).astype(int)*-1
        temp_df['HL'] = np.where(temp_df['DD']<0,-1,1)
        temp_df['HLcount'] = (temp_df.groupby((temp_df['HL'] != temp_df['HL'].shift(1)).cumsum()).cumcount()+1) * temp_df['HL']

        d1 = str(temp_df['날짜'].iloc[0]) # 거래시작일
        d11 = datetime.strptime(d1, "%Y%m%d")
        d2 = str(temp_df['날짜'].iloc[-1]) # 거래종료일
        d22 = datetime.strptime(d2, "%Y%m%d")
        delta = d22-d11
        delta_days = delta.days
        period = delta_days/365 # 투자기간(년)
        MDD = str(temp_df['MDD'].min()*100)[0:5]+"%"
        CAGR = str(temp_df['누적수익률'].iloc[-1]**(1/period)*100-100)[0:4]+"%"

        MaxHigh = temp_df['HLcount'].max() # 고점 갱신 연속일 수 
        MaxLow = temp_df['HLcount'].min() # 잠수 구간 일 수 
		
        return temp_df


	## matplotlib 이용 그래프 시현
    def draw_graph(self, temp_df):
        d1 = str(temp_df['날짜'].iloc[0]) # 거래시작일
        d11 = datetime.strptime(d1, "%Y%m%d")
        d2 = str(temp_df['날짜'].iloc[-1]) # 거래종료일
        d22 = datetime.strptime(d2, "%Y%m%d")
        delta = d22-d11
        delta_days = delta.days
        period = delta_days/365 # 투자기간(년)
        MDD = str(temp_df['MDD'].min()*100)[0:5]+"%"
        CAGR = str(temp_df['누적수익률'].iloc[-1]**(1/period)*100-100)[0:4]+"%"

        xtick_interval = 20 ## 20거래일 가로축
        plt.rcParams["figure.figsize"] = (14,7)
        split= self.filepath_first.split(".")
        split1 = split[0].split("_")
        png_ext = split1[3]
    
        plt.subplot(2,1,1) # row, column, index
        plt.yscale('log') # y-axis log scale
        plt.semilogy(temp_df['누적수익률'], color='#1F77B4')
        plt.semilogy(temp_df['최고누적'],color='#FF8D29')
        plt.xlabel('[trading day count]')
        plt.ylabel('[Cumulative Return]')
        plt.legend(["cumulative CAGR "+CAGR,"newHigh"])
        plt.xticks(np.arange(min(temp_df.index),max(temp_df.index)+1,xtick_interval))
        plt.title('[gen port] day_history Analsis_CUMULATIVE_RETURN')
        plt.grid(True)

        plt.subplot(2, 1, 2)
        plt.plot(temp_df['DD'],color='#FF8D29')
        plt.plot(temp_df['MDD'],color='#DA3F40')
        plt.xlabel('[trading day count]')
        plt.ylabel('[DrawDown]')
        plt.legend(["DD","MDD "+ MDD])
        plt.xticks(np.arange(min(temp_df.index),max(temp_df.index)+1,xtick_interval))
        plt.title('[GenPort] day_history Analsis_MDD')

        plt.tight_layout()
        plt.grid(True)
        plt.savefig('genport2-'+png_ext+'-log.png')

        plt.show()

        print("CAGR : "+ CAGR)
        print("MDD : "+ MDD)
        print("C/M : "+ CAGR/MDD)


    ## 성과 시현
    def show_result(self, temp_df):
        d1 = str(temp_df['날짜'].iloc[0]) # 거래시작일
        d11 = datetime.strptime(d1, "%Y%m%d")
        d2 = str(temp_df['날짜'].iloc[-1]) # 거래종료일
        d22 = datetime.strptime(d2, "%Y%m%d")
        delta = d22-d11
        delta_days = delta.days
        period = delta_days/252 # 투자기간(년)
        MDD = str(temp_df['MDD'].min()*100)[0:5]+"%"
        CAGR = str(temp_df['누적수익률'].iloc[-2]**(1/period)*100-100)[0:4]+"%"


## 테스트
if __name__=="__main__":
    Opt_portfolio = Opt_portfolio()
    portfolio_list = input("포트폴리오 입력 :")
    
    Opt_portfolio.read_portfolio(portfolio_list)

    processd_data = Opt_portfolio.preprocess_tradedata()
    simulated_data = Opt_portfolio.random_portfolio_weight(processd_data)
    Opt_portfolio.draw_graph_sharp_ratio(simulated_data)

    '''
    Show_portfolio = run_backtest()
    growth_data = Show_portfolio.process_trade_data(simulated_data)
    Show_portfolio.draw_graph(growth_data)
    '''
    '''
    현재 
    '''
