# -*- coding: utf-8 -*-

%matplotlib notebook
import pandas as pd
from pandas import DataFrame
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import dates
import matplotlib.font_manager as font_manager
import seaborn as sns


# 맑은고딕체
sns.set(style="whitegrid", font="Malgun Gothic", font_scale=1.0)
matplotlib.rcParams['figure.figsize'] = [12, 8]
fp = font_manager.FontProperties(fname="C:\\WINDOWS\\Fonts\\malgun.TTF", size=10)

class Core():
    def __init__(self):
        self.filepath_first =    "trade_history_daily_549258.csv"
        self.filepath_second = "trade_history_daily_566420.csv"
        
        self.tradedata_first = pd.read_csv(self.filepath_first, header=0)
        self.tradedata_second = pd.read_csv(self.filepath_second, header=0)

        self.count = 2 ## Asset 갯수
        self.simulated_data = pd .DataFrame(columns = ['Profit', 'Vollity', 'Sharp Ratio'])

        
    ## 수익률 데이터 전처리
    def preprocess_tradedata(self):
        ## empty data to store preprocessd data
        temp= pd.DataFrame()
        
        ## merge profit data to analyze 
        temp['A'] = self.tradedata_first['총자산'].astype(int)	
        temp['B'] = self.tradedata_second['총자산'].astype(int)
        temp = np.log(temp/temp.shift(1))

        return temp
       
    ## 시뮬레이션
    def random_portfolio_weight(self, data):
        
        for p in range (100):
            weights = np.random.random(self.count) 
            weights /= np.sum(weights)
            prets.append(np.sum(rets.mean() * weights) * 252)
            pvols.append(np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights))))
            ## print("%.3f / %.3f" %(prets[p], pvols[p]))

        prets = np.array(prets)
        pvols = np.array(pvols)

        return [prets, pvols]    
   


