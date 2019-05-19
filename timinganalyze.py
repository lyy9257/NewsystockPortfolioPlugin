'''
Genport Buy and Sell Time Analyze
'''

## import Packages
import pandas as pd     # 엑셀처럼 행과 열을 가진 DATA를 이용할 수 있게 해주는 패키지
import numpy as np     # 수학과학 연산을 위한 패키지 
import matplotlib.pyplot as plt     #그래프를 그릴때 쓰는 패키지
import sqlite3

class Core():
    def __init__(self):
        self.filepath = "trade_history_daily_536928.csv" # 젠포트 일자별 거래내역 데이터 파일
        self.con = sqlite3.connect('trade_data.db')
        self.tradedata = pd.read_csv(filepath, header=0)

    def pick_data(self, stock_code):
        
    def load_data():

    def preprocess_data():

     
