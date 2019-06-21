#-*- coding:utf-8 -*-

## 패키지 불러오기
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import os

'''
샤프비 그래프 작도
'''

def sharp_ratio(data):

    try:
        os.delete('sharp_simulate.png')

    except:
        pass

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
    plt.savefig('sharp_simulate.png')


'''
수익률 그래프 작도
'''

def profit(data, period):

    try:
        os.delete('Genport_Curve_and_MDD_Simulation.png')

    except:
        pass

    MDD = round(data['MDD'].min() * 100, 2)
    CAGR = round(data['누적수익률'].iloc[-1] ** (1/period) * 100 - 100, 2)

    ## 메모리 클리어링
    ## 2회이상 실시한 결과 그래프가 두번이상 작성되어 메모리클리어링
    plt.clf()

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


'''
비중 그래프 작도
'''

def weight(pf_list, data):  
    x = [1, 2, 3, 4, 5]
    y1 = [1, 1, 2, 3, 5]
    y2 = [0, 4, 2, 6, 8]
    y3 = [1, 3, 5, 7, 9]

    y = np.vstack([y1, y2, y3])

    labels = pf_list

    fig, ax = plt.subplots()
    ax.stackplot(x, y1, y2, y3, labels=labels)
    ax.legend(loc='best')
    plt.show()

    fig, ax = plt.subplots()
    ax.stackplot(x, y)
    plt.show()

    plt.stackplot()
    