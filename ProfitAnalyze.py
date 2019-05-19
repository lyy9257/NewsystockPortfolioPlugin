#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Apr  1 17:36:53 2019

@Main : 한손코딩
@author: 파릇
@edit by Hayman

"""

import pandas as pd
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt

class Core():
	def __init__(self):
		self.filepath = "trade_history_daily_536928.csv" # 젠포트 일자별 거래내역 데이터 파일
		self.fee = 0.00015  # 수수료 0.015%
		self.tradedata = pd.read_csv(filepath, header=0)

	## 거래 데이터 가공
	def process_trade_data(self):
		temp_df = self.tradedata

		temp_df['누적수익률'] = copydf['누적수익률'].astype(float)/100+1.0
		temp_df['최고누적'] = temp_df['누적수익률'].rolling(min_periods=1, window=100).max()
		temp_df['DD'] = temp_df['누적수익률'] / temp_df['최고누적'] -1
		temp_df['MDD'] = temp_df['DD'].rolling(min_periods=1, window=1000).min()
		temp_df['HL'] = (temp_df['DD'] < 0 ).astype(int)*-1
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
	def show_trade_data(self, temp_df):
		self.xtick_interval = 10  # x축 눈금 10 거래일
		plt.rcParams["figure.figsize"] = (14,7)
		split= filepath.split(".")
		split1 = split[0].split("_")
		png_ext = split1[3]
    
		plt.subplot(3,1,1) # row, column, index
		plt.yscale('log') # y-axis log scale
		plt.semilogy(copydf['누적수익률'], color='#1F77B4')
		plt.semilogy(copydf['최고누적'],color='#FF8D29')
		plt.xlabel('[trading day count]')
		plt.ylabel('[Cumulative Return]')
		plt.legend(["cumulative CAGR "+CAGR,"newHigh"])
		plt.xticks(np.arange(min(copydf.index),max(copydf.index)+1,xtick_interval))
		plt.title('[gen port] day_history Analsis_CUMULATIVE_RETURN')
		plt.grid(True)

		plt.subplot(3, 1, 2)
		plt.plot(copydf['DD'],color='#FF8D29')
		plt.plot(copydf['MDD'],color='#DA3F40')
		plt.xlabel('[trading day count]')
		plt.ylabel('[DrawDown]')
		plt.legend(["DD","MDD "+MDD])
		plt.xticks(np.arange(min(copydf.index),max(copydf.index)+1,xtick_interval))
		plt.title('[gen port] day_history Analsis_MDD')

		plt.subplot(3, 1, 3)
		plt.bar(copydf.index,copydf['HL'],width=1.0,color='#FF8D29')
		plt.xlabel('[trading day count]')
		plt.ylabel('[High Low]')
		plt.legend(["HL +"+str(MaxHigh)+" -"+str(MaxLow)])
		plt.xticks(np.arange(min(copydf.index),max(copydf.index)+1,xtick_interval))
		plt.title('[gen port] day_history Analsis_HIGH_LOW')

		plt.tight_layout()
		plt.grid(True)
		plt.savefig('genport2-'+png_ext+'-log.png')

		plt.show()

		print("CAGR : "+CAGR)
		print("MDD : "+MDD)
		print("C/M : "+CAGR/MDD)





