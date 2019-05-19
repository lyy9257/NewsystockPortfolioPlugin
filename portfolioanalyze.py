'''
Genport Portfolio Optimize
'''

# -*- coding: utf-8 -*-

## import Packages
import pandas as pd     # 엑셀처럼 행과 열을 가진 DATA를 이용할 수 있게 해주는 패키지
import numpy as np     # 수학과학 연산을 위한 패키지 
import matplotlib.pyplot as plt     #그래프를 그릴때 쓰는 패키지
import scipy.optimize as sco
import scipy.interpolate as sci

## optimize portfolio weight to get highest profit
## 포트폴리오 이론에 기반하여 최적의 비중을 구한다.

class Core():
    def __init__(self):
        self.filepath_first = "trade_history_daily_549258.csv"
        self.filepath_second = "trade_history_daily_566420.csv"
        
        self.tradedata_first = pd.read_csv(self.filepath_first, header=0)
        self.tradedata_second = pd.read_csv(self.filepath_second, header=0)

        self.count = 2

    ## 수익률 데이터 전처리
    def preprocess_tradedata(self):
        ## empty data to store preprocessd data
        temp= pd.DataFrame()
        
        ## merge profit data to analyze 
        temp['A'] = self.tradedata_first['총자산'].astype(int)	
        temp['B'] = self.tradedata_second['총자산'].astype(int)

        return temp
    
    ## 포트폴리오 비중에 따른 기대수익률, 기대변동성 추출
    def random_portfolio_weight(self, rets, weights):

        for p in range (100):
            weights = np.random.random(self.count) 
            weights /= np.sum(weights)
            prets.append(np.sum(rets.mean() * weights) * 252)
            pvols.append(np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights))))
            ## print("%.3f / %.3f" %(prets[p], pvols[p]))

        prets = np.array(prets)
        pvols = np.array(pvols)

        return [prets, pvols]


    ## 포트폴리오 비중에 따른 기대수익률, 변동성, Sharp ratio 출력
    def statistics(weights):

        ''' 
        Return portfolio statistics.
    
        Parameters
        ==========
        weights : array-like
            포트폴리오 내의 증권 비중
    
        Returns
        =======
        pret : float
            포트폴리오 수익률의 기댓값
        pvol : float
            포트폴리오 변동성의 기댓값
        pret / pvol : float
            무위험 이자율이 0일 때의 포트폴리오 샤프 지수
        '''

        rets = np.log(processed_data / processed_data.shift(1))
        pret = np.sum(rets.mean() * weights) * 252
        pvol = np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))

        return np.array([pret, pvol, pret / pvol])

    ## Minimize 함수
    def minimize_max_sharpe(weights):
        return -Core.statistics(weights)[2]
            

    def minimize_min_vol(weights):
        return Core.statistics(weights)[1] ** 2


    def minimize_func_port(weights):
        return Core.statistics(weights)[1]


    ## 샤프지수 극대화
    def max_sharpe(self, weights):

        ## 샤프비율 최대
        cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
        bnds = tuple((0, 1) for x in range(self.count))
        opts = sco.minimize(Core.minimize_max_sharpe, self.count * [1. / self.count,], method='SLSQP', bounds=bnds, constraints=cons)

        ## print(opts)
        ## print(Core.statistics(opts['x']).round(3))
        return Core.statistics(opts['x']).round(3)


    ## 분산 최소화
    def min_var(self, weights):

        ## 데이터 전처리
        cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
        bnds = tuple((0, 1) for x in range(self.count))
        optv = sco.minimize(Core.minimize_min_vol, self.count * [1. / self.count,], method='SLSQP', bounds=bnds, constraints=cons)

        ## print(optv)
        ## print(Core.statistics(optv['x']).round(3))
        return Core.statistics(optv['x']).round(3)


    ## 효율적 투자선
    ## 시간 존나많이 걸림. 멀티코어 사용을 통한 최적화 필수
    ## 코딩 미스로 추정됨. 예제는 이거보다 속도 빠름
    def good_inv_line(self, weights):
        cons = ({'type': 'eq', 'fun': lambda x:  Core.statistics(x)[0] - tret}, {'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
        bnds = tuple((0, 1) for x in weights)
        trets = np.linspace(0.0, 0.25, 50) ## 리니어 스페이스 배열 : 0 ~ 0.25를 50등분한 변수 Array 
        tvols = []

        for tret in trets:
            cons = ({'type': 'eq', 'fun': lambda x:  Core.statistics(x)[0] - tret}, {'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
            res = sco.minimize(Core.minimize_func_port, self.count * [1. / self.count,], method='SLSQP', bounds=bnds, constraints=cons)
            tvols.append(res['fun'])
            print(tret)

        tvols = np.array(tvols)

        ind = np.argmin(tvols)
        evols = tvols[ind:]
        erets = trets[ind:]
        tck = sci.splrep(evols, erets)

        return [evols, erets, tck]

    def f(x, tck):
        ''' 효율적 투자선 함수 (스플라인 근사) '''
        return sci.splev(x, tck, der=0)

    def df(x, tck):
        ''' 효율적 투자선 함수의 1차 도함수 '''
        return sci.splev(x, tck, der=1)

    ## 포트폴리오 비중 최적화
    def optimize_portfolio_weight(self, processed_data):

        ## 무작위 함수 추출 → 포트폴리오 비중으로 사용됨
        weights = np.random.random(self.count) 
        weights /= np.sum(weights)

        ## 데이터 준비(로그 수익률, 예상 수익률, 예상 변동성)
        rets = np.log(processed_data / processed_data.shift(1))
        random_result = self.random_portfolio_weight(rets, weights)
        prets = random_result[0]
        pvols = random_result[1]

        pt_opts = self.max_sharpe(weights) ## 샤프지수 Max
        pt_optv = self.min_var(weights) ## 분산 Min
        pt_g_inv_line = self.good_inv_line(weights) ## 효율적 시장투자선 Array

        ## 그래프 출력   
        plt.scatter(pvols, prets, c=prets/pvols, marker='X')

        plt.grid(True)
        plt.xlabel('expected volatility')
        plt.ylabel('expected return')
        plt.colorbar(label='Sharpe ratio')

        plt.plot(pt_g_inv_line[0], Core.f(pt_g_inv_line[0], pt_g_inv_line[2]), lw=7, alpha=0.5)
        plt.scatter(pt_optv[1], pt_optv[0], marker="*", s=500, alpha=0.5)
        plt.scatter(pt_opts[1], pt_opts[0], marker="*", s=500, alpha=0.5)

        plt.show()
    
    ## 시각화(그래프 출력)
    def show_graph():
        plt.scatter(pvols, prets, c=prets/pvols, marker='X')

        plt.grid(True)
        plt.xlabel('expected volatility')
        plt.ylabel('expected return')
        plt.colorbar(label='Sharpe ratio')
        plt.scatter(pt_optv[1], pt_optv[0], marker="*", s=500, alpha=0.5)
        plt.scatter(pt_opts[1], pt_opts[0], marker="*", s=500, alpha=0.5)

        plt.show()
        
if __name__=="__main__":
    data = Core()
    processed_data = data.preprocess_tradedata()
    data.optimize_portfolio_weight(processed_data)
