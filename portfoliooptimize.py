'''
Genport Portfolio Optimize
'''

## import Packages
import pandas as pd     # 엑셀처럼 행과 열을 가진 DATA를 이용할 수 있게 해주는 패키지
import numpy as np     # 수학과학 연산을 위한 패키지 
import matplotlib.pyplot as plt     #그래프를 그릴때 쓰는 패키지

class Core():
	def __init__(self):
		self.filepath_first = "monthly_stat_566420.csv" # 젠포트 일자별 거래내역 데이터 파일
		self.filepath_second = "monthly_stat_586167.csv" # 젠포트 일자별 거래내역 데이터 파일
		
		self.fee = 0.00015  # 수수료 0.015%
		
		self.tradedata_first = pd.read_csv(self.filepath_first, header=0)
		self.tradedata_second = pd.read_csv(self.filepath_second, header=0)

	## preprocess trade data for analyze
	def preprocess_tradedata(self):

		## empty data to store preprocessd data
		process_df= pd.DataFrame() 
		
		## merge profit data to analyze 
		process_df['월수익률_Portfolio A'] = self.tradedata_first['수익률'].astype(float)	
		process_df['월수익률_Portfolio B'] = self.tradedata_second['수익률'].astype(float)
		
		## print(process_df)
		## print(process_df.corr(method = 'pearson')) 

	## optimize portfolio weight to get highest profit
	## 포트폴리오 이론에 기반하여 최적의 비중을 구한다.
	def optimize_portfolio_weight(self, process_df):
        np.random.seed(2)
        weights = np.random.random(2) ## 총 2개의 포트폴리오 자산이 들어갔으므로
        weights /= np.sum(weights)
        return weights

        '''
        prets = []
        pvols = []
        for p in range (2500):
            weights = np.random.random(2) ## 총 2개의 포트폴리오가 들어갔으므로
            weights /= np.sum(weights)
            prets.append(np.sum(rets.mean() * weights) * 252)
            pvols.append(np.sqrt(np.dot(weights.T, 
                                np.dot(rets.cov() * 252, weights))))
        prets = np.array(prets)
        pvols = np.array(pvols)			

        plt.scatter(pvols, prets, c=prets/pvols, marker='o', cmap=mpl.cm.jet)
        plt.grid(True)
        plt.xlabel('expected volatility')
        plt.ylabel('expected return')
        plt.colorbar(label='Sharpe ratio')
        plt.show()

    def show_graph(self, process_df)
        '''

if __name__=="__main__":
	data = Core()
	processd_data = data.preprocess_tradedata()
    print(data.optimize_portfolio_weight(processd_data))