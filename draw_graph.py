## 패키지 불러오기
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

'''
샤프비 그래프 작도
'''
def sharp_ratio(data):
    data = data.sort_values(by='Sharp_Ratio', ascending=False)

    ## 그래프 작도
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(13,6), sharex=True)
    data.plot(kind='scatter', ax=ax, x='vollity', y='profit', c='Sharp_Ratio', marker='+', cmap='plasma')
        
    ## 최대 Sharp Ratio에 따른 출력값 작성
    max_sharp_ratio_index = data['Sharp_Ratio'].idxmax()
    profit_max_SR = data.iloc[0].loc['profit']
    vol_max_SR = data.iloc[0].loc['vollity']
                  
    ## 최대 Sharp ratio일때 Vol, Profit 출력
    plt.scatter(vol_max_SR, profit_max_SR, c='Blue', marker='*', s=200)

    ## PNG로 출력
    plt.savefig('sharp_simulate')


'''
수익률 그래프 작도
'''
def profit(data):
    d1 = str(data['날짜'].iloc[0]) # 거래시작일
    d11 = datetime.strptime(d1, "%Y%m%d")
    d2 = str(data['날짜'].iloc[-1]) # 거래종료일
    d22 = datetime.strptime(d2, "%Y%m%d")
    delta = d22-d11
    delta_days = delta.days
    period = delta_days/252 # 투자기간(년)

    MDD = round(data['MDD'].min() * 100, 2)
    CAGR = round(data['누적수익률'].iloc[-1] ** (1/period) * 100 - 100, 2)

    xtick_interval = 20 ## 20거래일 가로축
    plt.rcParams["figure.figsize"] = (14,7)
    png_ext = 'pf'
    
    plt.subplot(2,1,1) # row, column, index
    plt.yscale('log') # y-axis log scale
    plt.semilogy(data['누적수익률'], color='#1F77B4')
    plt.semilogy(data['최고누적'], color='#FF8D29')
    plt.xlabel('[Trading Day]')
    plt.ylabel('[Cumulative Return]')
    plt.legend(["Simulate CAGR : %.2f %%" %CAGR, "newHigh"])
    plt.xticks(np.arange(min(data.index), max(data.index) + 1, xtick_interval))
    plt.title('[GenPort]Strategy pf Simulation - Cumulative Return')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(data['DD'], color='#FF8D29')
    plt.plot(data['MDD'], color='#DA3F40')
    plt.xlabel('[Trading day]')
    plt.ylabel('[DrawDown]')
    plt.legend(["DD", "MDD : %.2f %%" %MDD])
    plt.xticks(np.arange(min(data.index), max(data.index) + 1, xtick_interval))
    plt.title('[GenPort]Strategy pf Simulation - MDD')

    plt.tight_layout()
    plt.grid(True)
    plt.savefig('Genport_Curve_and_MDD_Simulation.png')

